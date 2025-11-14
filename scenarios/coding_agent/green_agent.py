#!/usr/bin/env python3
"""
Coding Agent Green Agent - Evaluates coding capabilities.

This green agent provides programming challenges and evaluates solutions.
Tracks inspired by SWE-bench, USACO, and other coding benchmarks.
"""

import os
import sys
import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, AsyncIterator
import json

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agentbeats import (
    GreenAgentExecutor,
    TaskUpdate,
    AssessmentResult,
    Artifact,
    CodingTaskConfig,
)
from dotenv import load_dotenv

load_dotenv()


class CodingAgentEvaluator(GreenAgentExecutor):
    """Green agent that evaluates coding task completion."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9018):
        url = f"http://{host}:{port}"
        super().__init__(
            name="CodingAgentEvaluator",
            url=url,
            description="Evaluates coding agents on programming challenges"
        )
        self.host = host
        self.port = port
        self.test_cases = []

    async def setup_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> None:
        """Setup coding challenge environment."""
        self.test_cases = config.get("test_cases", [])

    async def run_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> AsyncIterator[TaskUpdate]:
        """Run coding assessment."""
        # Get the coding agent URL
        coder_url = participants.get("coder")
        if not coder_url:
            yield TaskUpdate(
                task_id=task_id,
                status="failed",
                message="No coder participant found"
            )
            return

        task_description = config.get("task_description", "")
        language = config.get("language", "python")
        time_limit = config.get("time_limit", 300)

        yield TaskUpdate(
            task_id=task_id,
            status="in_progress",
            message=f"Sending coding task to agent: {task_description[:50]}...",
            progress=0.3
        )

        # Send coding task to purple agent
        try:
            response = await self.send_to_participant(
                agent_url=coder_url,
                task_id=task_id,
                payload={
                    "type": "coding_task",
                    "description": task_description,
                    "language": language,
                    "time_limit": time_limit,
                    "test_cases": config.get("test_cases", [])
                }
            )

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Received solution from agent, running tests...",
                progress=0.6
            )

            # Extract code from response
            code = response.get("code", "")
            if not code:
                yield TaskUpdate(
                    task_id=task_id,
                    status="failed",
                    message="Agent did not provide code solution"
                )
                return

            # Test the code
            results = await self._run_tests(code, config)

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message=f"Tests complete: {results['passed']}/{results['total']} passed",
                progress=0.9,
                metadata=results
            )

        except Exception as e:
            yield TaskUpdate(
                task_id=task_id,
                status="failed",
                message=f"Error during assessment: {str(e)}"
            )

    async def evaluate_results(
        self,
        task_id: str,
        collected_data: Any
    ) -> AssessmentResult:
        """Evaluate coding assessment results."""
        # Extract test results from collected updates
        test_results = None
        for item in collected_data:
            if isinstance(item, TaskUpdate) and item.metadata:
                test_results = item.metadata
                break

        if not test_results:
            return AssessmentResult(
                task_id=task_id,
                status="failed",
                details={"error": "No test results found"}
            )

        passed = test_results.get("passed", 0)
        total = test_results.get("total", 0)
        score = (passed / total) if total > 0 else 0.0

        # Create detailed report
        report = self._generate_report(test_results)

        artifacts = [
            Artifact(
                name="test_results.json",
                content=json.dumps(test_results, indent=2),
                content_type="application/json"
            ),
            Artifact(
                name="evaluation_report.md",
                content=report,
                content_type="text/markdown"
            )
        ]

        return AssessmentResult(
            task_id=task_id,
            status="completed",
            score=score,
            details={
                "tests_passed": passed,
                "tests_total": total,
                "pass_rate": f"{score*100:.1f}%"
            },
            artifacts=artifacts
        )

    async def _run_tests(self, code: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute test cases against submitted code."""
        language = config.get("language", "python")
        test_cases = config.get("test_cases", [])

        if language != "python":
            return {
                "passed": 0,
                "total": len(test_cases),
                "error": f"Language {language} not yet supported"
            }

        passed = 0
        failed = 0
        test_details = []

        for i, test_case in enumerate(test_cases):
            try:
                # Create temp file with code
                with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.py',
                    delete=False
                ) as f:
                    f.write(code)
                    temp_file = f.name

                # Run test case
                input_data = test_case.get("input", "")
                expected_output = test_case.get("expected", "")

                result = subprocess.run(
                    ["python3", temp_file],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                actual_output = result.stdout.strip()
                expected_clean = expected_output.strip()

                if actual_output == expected_clean:
                    passed += 1
                    test_details.append({
                        "test": i + 1,
                        "status": "passed",
                        "input": input_data,
                        "expected": expected_clean,
                        "actual": actual_output
                    })
                else:
                    failed += 1
                    test_details.append({
                        "test": i + 1,
                        "status": "failed",
                        "input": input_data,
                        "expected": expected_clean,
                        "actual": actual_output
                    })

                # Clean up temp file
                os.unlink(temp_file)

            except subprocess.TimeoutExpired:
                failed += 1
                test_details.append({
                    "test": i + 1,
                    "status": "timeout",
                    "input": input_data
                })
            except Exception as e:
                failed += 1
                test_details.append({
                    "test": i + 1,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "passed": passed,
            "failed": failed,
            "total": len(test_cases),
            "details": test_details
        }

    def _generate_report(self, test_results: Dict[str, Any]) -> str:
        """Generate markdown evaluation report."""
        passed = test_results.get("passed", 0)
        total = test_results.get("total", 0)
        score = (passed / total * 100) if total > 0 else 0

        report = f"""# Coding Assessment Report

## Summary
- **Tests Passed:** {passed}/{total}
- **Score:** {score:.1f}%
- **Status:** {"✅ PASS" if passed == total else "❌ FAIL"}

## Test Details

"""
        for detail in test_results.get("details", []):
            test_num = detail.get("test", "?")
            status = detail.get("status", "unknown")
            status_emoji = "✅" if status == "passed" else "❌"

            report += f"### Test {test_num} {status_emoji}\n"
            report += f"- **Status:** {status}\n"

            if "input" in detail:
                report += f"- **Input:** `{detail['input']}`\n"
            if "expected" in detail:
                report += f"- **Expected:** `{detail['expected']}`\n"
            if "actual" in detail:
                report += f"- **Actual:** `{detail['actual']}`\n"
            if "error" in detail:
                report += f"- **Error:** {detail['error']}\n"

            report += "\n"

        return report


async def main():
    """Run the green agent server."""
    import argparse

    parser = argparse.ArgumentParser(description="Coding Agent Evaluator (Green Agent)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9018, help="Port to bind to")
    args = parser.parse_args()

    evaluator = CodingAgentEvaluator(host=args.host, port=args.port)

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  Coding Agent Evaluator (Green Agent)                    ║
║  Running at: {evaluator.url:40s} ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Keep server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        await evaluator.close()


if __name__ == "__main__":
    asyncio.run(main())
