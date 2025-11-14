#!/usr/bin/env python3
"""
Research Reproducibility Green Agent

Evaluates an agent's ability to reproduce research results and ensure code quality.
Inspired by Paper2Agent's quality assurance with pytest-cov and pylint analysis.

This benchmark tests:
1. Test suite generation
2. Code coverage achievement
3. Code quality metrics (pylint)
4. Result reproducibility
5. MCP server generation
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, AsyncIterator, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agentbeats import (
    GreenAgentExecutor,
    TaskUpdate,
    AssessmentResult,
    Artifact,
)
from dotenv import load_dotenv

load_dotenv()


class ResearchReproducibilityEvaluator(GreenAgentExecutor):
    """
    Green agent that evaluates research reproducibility capabilities.

    Based on Paper2Agent's methodology for quality assurance through
    automated testing, code coverage, and style analysis.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9022):
        url = f"http://{host}:{port}"
        super().__init__(
            name="ResearchReproducibilityEvaluator",
            url=url,
            description="Evaluates agents on research result reproducibility and code quality"
        )
        self.host = host
        self.port = port
        self.reproducibility_results = []

    async def setup_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> None:
        """Setup the reproducibility challenge."""
        self.reproducibility_results = []

    async def run_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> AsyncIterator[TaskUpdate]:
        """Execute the reproducibility assessment."""
        researcher_url = participants.get("researcher")
        if not researcher_url:
            yield TaskUpdate(
                task_id=task_id,
                status="failed",
                message="No researcher participant found"
            )
            return

        research_code = config.get("research_code", "")
        paper_results = config.get("paper_results", {})
        target_coverage = config.get("target_coverage", 80)
        target_pylint_score = config.get("target_pylint_score", 7.0)

        yield TaskUpdate(
            task_id=task_id,
            status="in_progress",
            message="Requesting reproducibility implementation with quality assurance",
            progress=0.2
        )

        try:
            # Send reproducibility task
            response = await self.send_to_participant(
                agent_url=researcher_url,
                task_id=task_id,
                payload={
                    "type": "reproducibility_task",
                    "research_code": research_code,
                    "paper_results": paper_results,
                    "task": "Reproduce research results with comprehensive testing and quality checks",
                    "requirements": {
                        "generate_tests": True,
                        "achieve_coverage": target_coverage,
                        "code_quality": target_pylint_score,
                        "generate_mcp_server": True,
                        "reproduce_results": True
                    }
                }
            )

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Implementation complete, evaluating reproducibility...",
                progress=0.6
            )

            # Extract results
            test_results = response.get("test_results", {})
            coverage_report = response.get("coverage_report", {})
            quality_metrics = response.get("quality_metrics", {})
            reproduced_results = response.get("reproduced_results", {})
            mcp_server = response.get("mcp_server", None)

            # Evaluate reproducibility
            evaluation = self._evaluate_reproducibility(
                test_results=test_results,
                coverage_report=coverage_report,
                quality_metrics=quality_metrics,
                reproduced_results=reproduced_results,
                mcp_server=mcp_server,
                paper_results=paper_results,
                target_coverage=target_coverage,
                target_quality=target_pylint_score
            )

            self.reproducibility_results.append(evaluation)

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message=f"Evaluation complete: {evaluation['reproducibility_score']:.1%} reproducibility",
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
        """Evaluate the reproducibility assessment."""
        if not self.reproducibility_results:
            return AssessmentResult(
                task_id=task_id,
                status="failed",
                details={"error": "No reproducibility results found"}
            )

        evaluation = self.reproducibility_results[0]

        # Calculate composite score (Paper2Agent QA methodology)
        test_score = evaluation.get("test_score", 0)
        coverage_score = evaluation.get("coverage_score", 0)
        quality_score = evaluation.get("quality_score", 0)
        reproducibility_score = evaluation.get("reproducibility_score", 0)
        mcp_score = evaluation.get("mcp_score", 0)

        # Weighted average (following Paper2Agent priorities)
        final_score = (
            test_score * 0.20 +           # Test suite quality
            coverage_score * 0.20 +       # Code coverage
            quality_score * 0.20 +        # Code quality (pylint)
            reproducibility_score * 0.30 + # Result reproduction
            mcp_score * 0.10              # MCP server generation
        )

        # Generate detailed report
        report = self._generate_report(evaluation)

        artifacts = [
            Artifact(
                name="reproducibility_results.json",
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
                "test_score": f"{test_score:.1%}",
                "coverage_score": f"{coverage_score:.1%}",
                "quality_score": f"{quality_score:.1%}",
                "reproducibility_score": f"{reproducibility_score:.1%}",
                "mcp_score": f"{mcp_score:.1%}",
                "final_score": f"{final_score:.1%}"
            },
            artifacts=artifacts
        )

    def _evaluate_reproducibility(
        self,
        test_results: Dict,
        coverage_report: Dict,
        quality_metrics: Dict,
        reproduced_results: Dict,
        mcp_server: Any,
        paper_results: Dict,
        target_coverage: float,
        target_quality: float
    ) -> Dict[str, Any]:
        """Evaluate reproducibility following Paper2Agent QA methodology."""

        # Test suite evaluation
        tests_passed = test_results.get("passed", 0)
        tests_total = test_results.get("total", 0)
        test_score = tests_passed / tests_total if tests_total > 0 else 0

        # Coverage evaluation
        actual_coverage = coverage_report.get("coverage_percent", 0)
        coverage_score = min(actual_coverage / target_coverage, 1.0) if target_coverage > 0 else 0

        # Quality evaluation (pylint score)
        pylint_score = quality_metrics.get("pylint_score", 0)
        quality_score = min(pylint_score / target_quality, 1.0) if target_quality > 0 else 0

        # Result reproduction evaluation
        result_matches = 0
        total_results = len(paper_results)

        for key, expected_value in paper_results.items():
            actual_value = reproduced_results.get(key)
            if self._compare_results(actual_value, expected_value):
                result_matches += 1

        reproducibility_score = result_matches / total_results if total_results > 0 else 0

        # MCP server evaluation
        mcp_score = 1.0 if mcp_server and self._validate_mcp_server(mcp_server) else 0.0

        return {
            "test_score": test_score,
            "coverage_score": coverage_score,
            "quality_score": quality_score,
            "reproducibility_score": reproducibility_score,
            "mcp_score": mcp_score,
            "tests_passed": tests_passed,
            "tests_total": tests_total,
            "coverage_percent": actual_coverage,
            "pylint_score": pylint_score,
            "results_matched": result_matches,
            "results_total": total_results,
            "has_mcp_server": bool(mcp_server),
            "quality_details": quality_metrics,
            "coverage_details": coverage_report
        }

    def _compare_results(self, actual: Any, expected: Any) -> bool:
        """Compare research results allowing for numerical precision differences."""
        if actual is None:
            return False

        # Type matching
        if type(actual) != type(expected):
            try:
                actual = type(expected)(actual)
            except (ValueError, TypeError):
                return False

        # Numerical comparison with tolerance
        if isinstance(expected, (int, float)):
            tolerance = abs(expected) * 0.01  # 1% tolerance
            return abs(actual - expected) <= tolerance

        # String comparison
        if isinstance(expected, str):
            return actual.strip() == expected.strip()

        # List/Dict comparison
        if isinstance(expected, (list, dict)):
            return actual == expected

        return actual == expected

    def _validate_mcp_server(self, mcp_server: Dict) -> bool:
        """Validate MCP server structure."""
        required_fields = ["name", "tools"]
        return all(field in mcp_server for field in required_fields)

    def _generate_report(self, evaluation: Dict) -> str:
        """Generate Paper2Agent-style reproducibility report."""
        test_score = evaluation.get("test_score", 0)
        coverage_score = evaluation.get("coverage_score", 0)
        quality_score = evaluation.get("quality_score", 0)
        repro_score = evaluation.get("reproducibility_score", 0)
        mcp_score = evaluation.get("mcp_score", 0)

        report = f"""# Research Reproducibility Assessment Report

## Executive Summary

This assessment evaluates an agent's ability to reproduce research results with
comprehensive quality assurance, following Paper2Agent's testing and QA methodology.

## Performance Metrics

### Test Suite Quality
- **Test Pass Rate:** {test_score:.1%}
- **Tests Passed:** {evaluation.get('tests_passed', 0)}/{evaluation.get('tests_total', 0)}
- **Status:** {"✅ All tests passing" if test_score == 1.0 else "⚠️ Some tests failing"}

### Code Coverage (pytest-cov)
- **Coverage Score:** {coverage_score:.1%}
- **Actual Coverage:** {evaluation.get('coverage_percent', 0):.1f}%
- **Status:** {"✅ Meets target" if coverage_score >= 0.8 else "⚠️ Below target"}

### Code Quality (pylint)
- **Quality Score:** {quality_score:.1%}
- **Pylint Score:** {evaluation.get('pylint_score', 0):.2f}/10
- **Status:** {"✅ High quality" if quality_score >= 0.8 else "⚠️ Needs improvement"}

### Result Reproducibility
- **Reproducibility:** {repro_score:.1%}
- **Results Matched:** {evaluation.get('results_matched', 0)}/{evaluation.get('results_total', 0)}
- **Status:** {"✅ Fully reproducible" if repro_score == 1.0 else "⚠️ Partial reproduction"}

### MCP Server Generation
- **MCP Server:** {"✅ Generated" if evaluation.get('has_mcp_server') else "❌ Not generated"}
- **Validation:** {"✅ Valid structure" if mcp_score == 1.0 else "❌ Invalid"}

## Paper2Agent Quality Pipeline Alignment

This assessment mirrors Paper2Agent's QA pipeline:

1. {'✓' if test_score > 0.9 else '✗'} **Test Suite Generation** (pytest)
2. {'✓' if coverage_score > 0.8 else '✗'} **Code Coverage Analysis** (pytest-cov)
3. {'✓' if quality_score > 0.7 else '✗'} **Style Analysis** (pylint)
4. {'✓' if repro_score > 0.9 else '✗'} **Result Reproduction**
5. {'✓' if mcp_score == 1.0 else '✗'} **MCP Server Generation**

## Detailed Quality Metrics

### Coverage Details
```json
{json.dumps(evaluation.get('coverage_details', {}), indent=2)}
```

### Quality Details
```json
{json.dumps(evaluation.get('quality_details', {}), indent=2)}
```

## Scoring Breakdown

| Component | Weight | Score | Contribution |
|-----------|--------|-------|--------------|
| Test Suite | 20% | {test_score:.1%} | {test_score * 0.20:.1%} |
| Code Coverage | 20% | {coverage_score:.1%} | {coverage_score * 0.20:.1%} |
| Code Quality | 20% | {quality_score:.1%} | {quality_score * 0.20:.1%} |
| Reproducibility | 30% | {repro_score:.1%} | {repro_score * 0.30:.1%} |
| MCP Server | 10% | {mcp_score:.1%} | {mcp_score * 0.10:.1%} |

## Assessment Summary

{"✅ Excellent test coverage!" if test_score > 0.9 else "⚠️ Improve test suite"}
{"✅ Strong code coverage!" if coverage_score > 0.8 else "⚠️ Increase coverage"}
{"✅ High code quality!" if quality_score > 0.8 else "⚠️ Address quality issues"}
{"✅ Results fully reproducible!" if repro_score > 0.95 else "⚠️ Reproducibility concerns"}
{"✅ MCP server ready!" if mcp_score == 1.0 else "⚠️ MCP server issues"}

## Recommendations

{"This implementation demonstrates production-ready research code with excellent quality assurance." if all(s > 0.8 for s in [test_score, coverage_score, quality_score, repro_score]) else "Focus on improving test coverage, code quality, and reproducibility to meet Paper2Agent standards."}

---
*Based on Paper2Agent's quality assurance methodology with pytest-cov and pylint*
"""
        return report


async def main():
    """Run the green agent server."""
    import argparse

    parser = argparse.ArgumentParser(description="Research Reproducibility Evaluator")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9022, help="Port to bind to")
    args = parser.parse_args()

    evaluator = ResearchReproducibilityEvaluator(host=args.host, port=args.port)

    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║  Research Reproducibility Evaluator (Green Agent)                ║
║  Based on Paper2Agent QA pipeline                                 ║
║  Running at: {evaluator.url:48s} ║
╚═══════════════════════════════════════════════════════════════════╝

Evaluates agents on:
  • Test suite generation
  • Code coverage (pytest-cov)
  • Code quality (pylint)
  • Result reproducibility
  • MCP server generation

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
