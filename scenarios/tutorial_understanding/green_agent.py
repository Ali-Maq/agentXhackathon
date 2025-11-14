#!/usr/bin/env python3
"""
Tutorial Understanding Green Agent

Evaluates an agent's ability to understand and execute research tutorials/notebooks.
Inspired by Paper2Agent's notebook execution and tool generation pipeline.

This benchmark tests:
1. Notebook execution capability
2. Error handling and debugging
3. Output interpretation
4. Visualization analysis
5. Tool generation from executed code
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, AsyncIterator, List
import hashlib

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agentbeats import (
    GreenAgentExecutor,
    TaskUpdate,
    AssessmentResult,
    Artifact,
)
from dotenv import load_dotenv

load_dotenv()


class TutorialUnderstandingEvaluator(GreenAgentExecutor):
    """
    Green agent that evaluates tutorial understanding and execution.

    Based on Paper2Agent's methodology for executing notebooks and
    generating functional tools from research tutorials.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9021):
        url = f"http://{host}:{port}"
        super().__init__(
            name="TutorialUnderstandingEvaluator",
            url=url,
            description="Evaluates agents on understanding and executing research tutorials"
        )
        self.host = host
        self.port = port
        self.execution_results = []

    async def setup_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> None:
        """Setup the tutorial understanding challenge."""
        self.execution_results = []

    async def run_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> AsyncIterator[TaskUpdate]:
        """Execute the tutorial understanding assessment."""
        researcher_url = participants.get("researcher")
        if not researcher_url:
            yield TaskUpdate(
                task_id=task_id,
                status="failed",
                message="No researcher participant found"
            )
            return

        notebook_content = config.get("notebook_content", "")
        expected_outputs = config.get("expected_outputs", {})
        expected_tools = config.get("expected_tools", [])
        allow_errors = config.get("allow_errors", True)

        yield TaskUpdate(
            task_id=task_id,
            status="in_progress",
            message="Requesting tutorial execution and tool generation",
            progress=0.2
        )

        try:
            # Send tutorial execution task
            response = await self.send_to_participant(
                agent_url=researcher_url,
                task_id=task_id,
                payload={
                    "type": "tutorial_execution",
                    "notebook_content": notebook_content,
                    "task": "Execute this research tutorial and generate reusable tools",
                    "requirements": {
                        "execute_all_cells": True,
                        "handle_errors": allow_errors,
                        "extract_functions": True,
                        "generate_documentation": True,
                        "capture_visualizations": True
                    }
                }
            )

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Tutorial executed, evaluating results...",
                progress=0.6
            )

            # Extract execution results
            execution_success = response.get("execution_success", False)
            cell_outputs = response.get("cell_outputs", [])
            generated_tools = response.get("generated_tools", [])
            visualizations = response.get("visualizations", [])
            errors_encountered = response.get("errors", [])

            # Evaluate execution quality
            evaluation = self._evaluate_execution(
                execution_success=execution_success,
                cell_outputs=cell_outputs,
                generated_tools=generated_tools,
                visualizations=visualizations,
                errors=errors_encountered,
                expected_outputs=expected_outputs,
                expected_tools=expected_tools
            )

            self.execution_results.append(evaluation)

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message=f"Evaluation complete: {evaluation['execution_score']:.1%} success rate",
                progress=0.9,
                metadata=evaluation
            )

        except Exception as e:
            yield TaskUpdate(
                task_id=task_id,
                status="failed",
                message=f"Assessment error: {str(e)}"
            )

    async def evaluate_results(
        self,
        task_id: str,
        collected_data: Any
    ) -> AssessmentResult:
        """Evaluate the tutorial understanding assessment."""
        if not self.execution_results:
            return AssessmentResult(
                task_id=task_id,
                status="failed",
                details={"error": "No execution results found"}
            )

        evaluation = self.execution_results[0]

        # Calculate composite score (Paper2Agent methodology)
        execution_score = evaluation.get("execution_score", 0)
        output_accuracy = evaluation.get("output_accuracy", 0)
        tool_quality = evaluation.get("tool_quality", 0)
        viz_score = evaluation.get("visualization_score", 0)
        error_handling = evaluation.get("error_handling_score", 0)

        # Weighted average
        final_score = (
            execution_score * 0.25 +     # Successful execution
            output_accuracy * 0.25 +     # Correct outputs
            tool_quality * 0.25 +        # Tool generation
            viz_score * 0.15 +           # Visualizations
            error_handling * 0.10        # Error handling
        )

        # Generate detailed report
        report = self._generate_report(evaluation)

        artifacts = [
            Artifact(
                name="execution_results.json",
                content=json.dumps(evaluation, indent=2),
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
            score=final_score,
            details={
                "execution_success": f"{execution_score:.1%}",
                "output_accuracy": f"{output_accuracy:.1%}",
                "tool_quality": f"{tool_quality:.1%}",
                "visualization_score": f"{viz_score:.1%}",
                "error_handling": f"{error_handling:.1%}",
                "final_score": f"{final_score:.1%}"
            },
            artifacts=artifacts
        )

    def _evaluate_execution(
        self,
        execution_success: bool,
        cell_outputs: List[Dict],
        generated_tools: List[Dict],
        visualizations: List[str],
        errors: List[str],
        expected_outputs: Dict,
        expected_tools: List[str]
    ) -> Dict[str, Any]:
        """Evaluate tutorial execution following Paper2Agent methodology."""

        # Execution success score
        execution_score = 1.0 if execution_success else 0.0

        # Output accuracy
        output_matches = 0
        total_expected = len(expected_outputs)

        for cell_idx, expected_output in expected_outputs.items():
            if cell_idx < len(cell_outputs):
                actual_output = cell_outputs[cell_idx].get("output", "")
                if self._compare_outputs(actual_output, expected_output):
                    output_matches += 1

        output_accuracy = output_matches / total_expected if total_expected > 0 else 0

        # Tool generation quality
        generated_tool_names = {t.get("name", "") for t in generated_tools}
        expected_tool_set = set(expected_tools)

        tool_matches = len(generated_tool_names & expected_tool_set)
        tool_recall = tool_matches / len(expected_tool_set) if expected_tool_set else 0

        # Check tool completeness
        complete_tools = sum(
            1 for t in generated_tools
            if t.get("name") and t.get("parameters") and t.get("documentation")
        )
        tool_completeness = complete_tools / len(generated_tools) if generated_tools else 0

        tool_quality = (tool_recall + tool_completeness) / 2

        # Visualization score
        viz_score = min(len(visualizations) / max(len(expected_tools), 1), 1.0)

        # Error handling score
        error_handling_score = 1.0 if (execution_success or len(errors) == 0) else 0.5

        return {
            "execution_score": execution_score,
            "output_accuracy": output_accuracy,
            "tool_quality": tool_quality,
            "visualization_score": viz_score,
            "error_handling_score": error_handling_score,
            "cells_executed": len(cell_outputs),
            "tools_generated": len(generated_tools),
            "visualizations_created": len(visualizations),
            "errors_encountered": len(errors),
            "tool_names": list(generated_tool_names),
            "error_details": errors[:5]  # First 5 errors
        }

    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """Compare outputs allowing for minor variations."""
        # Normalize whitespace
        actual_norm = " ".join(str(actual).split())
        expected_norm = " ".join(str(expected).split())

        # Exact match
        if actual_norm == expected_norm:
            return True

        # Check if expected is substring of actual
        if expected_norm in actual_norm:
            return True

        # Fuzzy match for numerical outputs
        try:
            actual_num = float(actual_norm)
            expected_num = float(expected_norm)
            return abs(actual_num - expected_num) < 0.01
        except (ValueError, TypeError):
            pass

        return False

    def _generate_report(self, evaluation: Dict) -> str:
        """Generate Paper2Agent-style execution report."""
        exec_score = evaluation.get("execution_score", 0)
        output_acc = evaluation.get("output_accuracy", 0)
        tool_quality = evaluation.get("tool_quality", 0)
        viz_score = evaluation.get("visualization_score", 0)
        error_handling = evaluation.get("error_handling_score", 0)

        report = f"""# Tutorial Understanding Assessment Report

## Executive Summary

This assessment evaluates an agent's ability to understand and execute research tutorials,
following Paper2Agent's notebook execution and tool generation methodology.

## Performance Metrics

### Execution Quality
- **Execution Success:** {"✅ Passed" if exec_score == 1.0 else "❌ Failed"}
- **Output Accuracy:** {output_acc:.1%}
- **Cells Executed:** {evaluation.get('cells_executed', 0)}

### Tool Generation
- **Tool Quality Score:** {tool_quality:.1%}
- **Tools Generated:** {evaluation.get('tools_generated', 0)}
- **Tools Expected:** Match rate {tool_quality:.1%}

### Visualization & Error Handling
- **Visualization Score:** {viz_score:.1%}
- **Visualizations Created:** {evaluation.get('visualizations_created', 0)}
- **Error Handling:** {error_handling:.1%}
- **Errors Encountered:** {evaluation.get('errors_encountered', 0)}

## Generated Tools

{chr(10).join(f"- {tool}" for tool in evaluation.get('tool_names', []))}

## Error Analysis

{chr(10).join(f"- {error}" for error in evaluation.get('error_details', [])) if evaluation.get('error_details') else "No errors encountered"}

## Paper2Agent Pipeline Alignment

This assessment mirrors Paper2Agent's execution pipeline:
1. {'✓' if exec_score > 0.8 else '✗'} Notebook execution
2. {'✓' if output_acc > 0.8 else '✗'} Output validation
3. {'✓' if tool_quality > 0.7 else '✗'} Tool extraction
4. {'✓' if viz_score > 0.5 else '✗'} Visualization capture
5. {'✓' if error_handling > 0.8 else '✗'} Error handling

## Scoring Breakdown

| Component | Weight | Score | Contribution |
|-----------|--------|-------|--------------|
| Execution Success | 25% | {exec_score:.1%} | {exec_score * 0.25:.1%} |
| Output Accuracy | 25% | {output_acc:.1%} | {output_acc * 0.25:.1%} |
| Tool Quality | 25% | {tool_quality:.1%} | {tool_quality * 0.25:.1%} |
| Visualizations | 15% | {viz_score:.1%} | {viz_score * 0.15:.1%} |
| Error Handling | 10% | {error_handling:.1%} | {error_handling * 0.10:.1%} |

## Quality Assessment

{"✅ Excellent tutorial execution!" if exec_score > 0.9 else "⚠️ Execution issues detected"}
{"✅ Accurate output generation!" if output_acc > 0.8 else "⚠️ Output mismatches found"}
{"✅ High-quality tool extraction!" if tool_quality > 0.8 else "⚠️ Improve tool generation"}
{"✅ Good visualization capture!" if viz_score > 0.7 else "⚠️ Missing visualizations"}

---
*Based on Paper2Agent's notebook execution and tool generation pipeline*
"""
        return report


async def main():
    """Run the green agent server."""
    import argparse

    parser = argparse.ArgumentParser(description="Tutorial Understanding Evaluator")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9021, help="Port to bind to")
    args = parser.parse_args()

    evaluator = TutorialUnderstandingEvaluator(host=args.host, port=args.port)

    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║  Tutorial Understanding Evaluator (Green Agent)                  ║
║  Based on Paper2Agent notebook execution pipeline                ║
║  Running at: {evaluator.url:48s} ║
╚═══════════════════════════════════════════════════════════════════╝

Evaluates agents on:
  • Notebook execution
  • Output accuracy
  • Tool generation
  • Visualization capture
  • Error handling

Press Ctrl+C to stop...
    """)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        await evaluator.close()


if __name__ == "__main__":
    asyncio.run(main())
