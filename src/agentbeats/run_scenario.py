"""
Scenario orchestration utilities.
"""

import asyncio
import toml
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from .client import A2AClient
from .models import AssessmentRequest

console = Console()


class ScenarioRunner:
    """Orchestrates scenario execution with multiple agents."""

    def __init__(self, scenario_path: str):
        self.scenario_path = Path(scenario_path)
        self.config = self._load_config()
        self.processes: List[subprocess.Popen] = []
        self.client = A2AClient()

    def _load_config(self) -> Dict[str, Any]:
        """Load scenario configuration from TOML file."""
        with open(self.scenario_path, 'r') as f:
            return toml.load(f)

    def start_agent(self, agent_config: Dict[str, Any]) -> subprocess.Popen:
        """Start an agent process."""
        command = agent_config.get("command")
        if not command:
            raise ValueError(f"No command specified for agent")

        console.print(f"[green]Starting agent:[/green] {command}")

        process = subprocess.Popen(
            command,
            shell=True,
            cwd=self.scenario_path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.processes.append(process)
        return process

    async def wait_for_agents(self, timeout: int = 30):
        """Wait for all agents to be ready."""
        console.print("[yellow]Waiting for agents to start...[/yellow]")

        start_time = time.time()
        agents = self.config.get("agents", {})

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Checking agent health...", total=len(agents))

            for agent_name, agent_config in agents.items():
                url = agent_config.get("url")
                while time.time() - start_time < timeout:
                    try:
                        card = await self.client.get_agent_card(url)
                        console.print(f"[green]✓[/green] {agent_name} ready at {url}")
                        progress.advance(task)
                        break
                    except Exception:
                        await asyncio.sleep(1)
                else:
                    raise TimeoutError(f"Agent {agent_name} failed to start within {timeout}s")

    async def run_assessment(
        self,
        show_logs: bool = False,
        serve_only: bool = False
    ):
        """Run the assessment scenario."""
        try:
            # Start all agent processes
            agents = self.config.get("agents", {})
            for agent_name, agent_config in agents.items():
                self.start_agent(agent_config)

            # Wait for agents to be ready
            await self.wait_for_agents()

            if serve_only:
                console.print("[blue]Agents are running. Press Ctrl+C to stop.[/blue]")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    pass
                return

            # Prepare assessment request
            assessment_config = self.config.get("assessment", {})
            participants = {
                name: agents[name]["url"]
                for name in assessment_config.get("participants", [])
            }

            green_agent_url = agents.get("green", {}).get("url")
            if not green_agent_url:
                raise ValueError("No green agent URL specified")

            request = AssessmentRequest(
                task_id=f"scenario_{int(time.time())}",
                participants=participants,
                config=assessment_config.get("config", {}),
                metadata=self.config.get("metadata", {})
            )

            # Send assessment request and stream results
            console.print("\n[bold cyan]Starting Assessment[/bold cyan]\n")

            async for update in self.client.stream_task(
                agent_url=green_agent_url,
                task_id=request.task_id,
                payload=request.model_dump()
            ):
                if show_logs:
                    self._print_update(update)

            console.print("\n[bold green]Assessment Complete[/bold green]")

        finally:
            await self.cleanup()

    def _print_update(self, update: Dict[str, Any]):
        """Pretty print assessment updates."""
        update_type = update.get("type", "unknown")

        if update_type == "task_update":
            status = update.get("status", "")
            message = update.get("message", "")
            progress = update.get("progress", 0)

            console.print(
                f"[blue]Status:[/blue] {status} "
                f"[dim]({progress*100:.0f}%)[/dim] - {message}"
            )
        elif update_type == "artifact":
            name = update.get("name", "")
            console.print(f"[green]Artifact:[/green] {name}")
        else:
            console.print(update)

    async def cleanup(self):
        """Clean up all running processes."""
        console.print("\n[yellow]Stopping agents...[/yellow]")

        for process in self.processes:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        await self.client.close()
        console.print("[green]Cleanup complete[/green]")


async def run_scenario_file(
    scenario_path: str,
    show_logs: bool = False,
    serve_only: bool = False
):
    """Run a scenario from a TOML configuration file."""
    runner = ScenarioRunner(scenario_path)
    await runner.run_assessment(show_logs=show_logs, serve_only=serve_only)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        console.print("[red]Usage: python run_scenario.py <scenario.toml> [--show-logs] [--serve-only][/red]")
        sys.exit(1)

    scenario_path = sys.argv[1]
    show_logs = "--show-logs" in sys.argv
    serve_only = "--serve-only" in sys.argv

    asyncio.run(run_scenario_file(scenario_path, show_logs, serve_only))
