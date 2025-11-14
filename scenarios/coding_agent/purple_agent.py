#!/usr/bin/env python3
"""
Coding Purple Agent - Solves programming challenges using LLM.

This agent receives coding tasks and generates solutions.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agentbeats import A2AServer, AgentCard
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()


class CodingPurpleAgent(A2AServer):
    """Purple agent that solves coding challenges."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9019):
        url = f"http://{host}:{port}"
        super().__init__(
            name="CodingPurpleAgent",
            url=url,
            description="An AI coding agent that solves programming challenges"
        )
        self.host = host
        self.port = port

        # Initialize LLM client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set in environment")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"

    def get_card(self) -> AgentCard:
        """Return agent card with capabilities."""
        return AgentCard(
            name=self.name,
            url=self.url,
            description=self.description,
            capabilities=["coding", "python", "problem_solving"],
            roles=["coder"]
        )

    async def handle_task(self, task_id: str, payload: Dict[str, Any]) -> Any:
        """Handle incoming coding tasks."""
        task_type = payload.get("type")

        if task_type == "coding_task":
            return await self._solve_coding_task(task_id, payload)

        return {"error": f"Unknown task type: {task_type}"}

    async def _solve_coding_task(self, task_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Solve a coding challenge."""
        description = payload.get("description", "")
        language = payload.get("language", "python")
        test_cases = payload.get("test_cases", [])

        # Build prompt
        prompt = self._build_coding_prompt(description, language, test_cases)

        try:
            # Generate solution using LLM
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            code = self._extract_code(response.text)

            return {
                "task_id": task_id,
                "status": "completed",
                "code": code,
                "language": language,
                "explanation": response.text
            }

        except Exception as e:
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }

    def _build_coding_prompt(
        self,
        description: str,
        language: str,
        test_cases: list
    ) -> str:
        """Build prompt for LLM."""
        prompt = f"""You are an expert {language} programmer. Solve the following coding challenge.

**Task:**
{description}

**Test Cases:**
"""
        for i, test in enumerate(test_cases, 1):
            input_data = test.get("input", "")
            expected = test.get("expected", "")
            prompt += f"\nTest {i}:\n"
            prompt += f"  Input: {input_data}\n"
            prompt += f"  Expected Output: {expected}\n"

        prompt += """

**Requirements:**
1. Write complete, working code
2. Handle all test cases correctly
3. Use proper error handling
4. Write clean, readable code

Provide ONLY the code in a code block, no additional explanation before or after.
"""
        return prompt

    def _extract_code(self, response: str) -> str:
        """Extract code from LLM response."""
        # Look for code blocks
        if "```python" in response:
            start = response.find("```python") + len("```python")
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()

        if "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()

        # If no code blocks, try to extract from response
        lines = response.split("\n")
        code_lines = []
        in_code = False

        for line in lines:
            if line.strip().startswith("def ") or line.strip().startswith("class "):
                in_code = True

            if in_code:
                code_lines.append(line)

        if code_lines:
            return "\n".join(code_lines).strip()

        # Last resort: return entire response
        return response.strip()


async def main():
    """Run the purple agent server."""
    import argparse

    parser = argparse.ArgumentParser(description="Coding Purple Agent")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9019, help="Port to bind to")
    args = parser.parse_args()

    agent = CodingPurpleAgent(host=args.host, port=args.port)

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  Coding Purple Agent                                     ║
║  Running at: {agent.url:40s} ║
║  Model: {agent.model:45s} ║
╚═══════════════════════════════════════════════════════════╝
    """)

    print("Ready to receive coding tasks!")

    # Keep server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    asyncio.run(main())
