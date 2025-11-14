#!/usr/bin/env python3
"""
Research Code Extraction Green Agent

Evaluates an agent's ability to extract functional code from research repositories.
Inspired by Paper2Agent's tutorial discovery and extraction methodology.

This benchmark tests:
1. Repository analysis and structure understanding
2. Notebook/tutorial identification
3. Code extraction accuracy
4. Function signature preservation
5. Documentation quality
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import Dict, Any, AsyncIterator, List
import tempfile
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agentbeats import (
    GreenAgentExecutor,
    TaskUpdate,
    AssessmentResult,
    Artifact,
)
from dotenv import load_dotenv

load_dotenv()


class ResearchCodeExtractionEvaluator(GreenAgentExecutor):
    """
    Green agent that evaluates research code extraction capabilities.

    Based on Paper2Agent's methodology for discovering and extracting
    tutorials from research codebases.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9020):
        url = f"http://{host}:{port}"
        super().__init__(
            name="ResearchCodeExtractionEvaluator",
            url=url,
            description="Evaluates agents on extracting code from research repositories"
        )
        self.host = host
        self.port = port
        self.extraction_results = []

    async def setup_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> None:
        """Setup the research code extraction challenge."""
        self.extraction_results = []

        # Validate config
        required_fields = ["repository_url", "expected_tutorials", "expected_functions"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")

    async def run_assessment(
        self,
        task_id: str,
        participants: Dict[str, str],
        config: Dict[str, Any]
    ) -> AsyncIterator[TaskUpdate]:
        """Execute the code extraction assessment."""
        researcher_url = participants.get("researcher")
        if not researcher_url:
            yield TaskUpdate(
                task_id=task_id,
                status="failed",
                message="No researcher participant found"
            )
            return

        repo_url = config.get("repository_url")
        expected_tutorials = config.get("expected_tutorials", [])
        expected_functions = config.get("expected_functions", [])
        time_limit = config.get("time_limit", 600)

        yield TaskUpdate(
            task_id=task_id,
            status="in_progress",
            message=f"Requesting code extraction from repository: {repo_url}",
            progress=0.2
        )

        try:
            # Send extraction task to purple agent
            response = await self.send_to_participant(
                agent_url=researcher_url,
                task_id=task_id,
                payload={
                    "type": "code_extraction",
                    "repository_url": repo_url,
                    "task": "Extract all tutorials/notebooks and their key functions",
                    "time_limit": time_limit,
                    "extraction_criteria": {
                        "find_notebooks": True,
                        "extract_functions": True,
                        "preserve_signatures": True,
                        "include_documentation": True
                    }
                }
            )

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message="Agent completed extraction, evaluating results...",
                progress=0.6
            )

            # Extract results
            extracted_tutorials = response.get("tutorials", [])
            extracted_functions = response.get("functions", [])

            # Evaluate extraction quality
            evaluation = self._evaluate_extraction(
                extracted_tutorials=extracted_tutorials,
                extracted_functions=extracted_functions,
                expected_tutorials=expected_tutorials,
                expected_functions=expected_functions
            )

            self.extraction_results.append(evaluation)

            yield TaskUpdate(
                task_id=task_id,
                status="in_progress",
                message=f"Evaluation complete: {evaluation['tutorial_recall']:.1%} tutorial recall",
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
        """Evaluate the code extraction assessment."""
        if not self.extraction_results:
            return AssessmentResult(
                task_id=task_id,
                status="failed",
                details={"error": "No extraction results found"}
            )

        evaluation = self.extraction_results[0]

        # Calculate composite score
        tutorial_score = evaluation.get("tutorial_recall", 0)
        function_score = evaluation.get("function_recall", 0)
        accuracy_score = evaluation.get("signature_accuracy", 0)
        doc_score = evaluation.get("documentation_quality", 0)

        # Weighted average (following Paper2Agent priorities)
        final_score = (
            tutorial_score * 0.3 +      # Tutorial discovery
            function_score * 0.3 +       # Function extraction
            accuracy_score * 0.2 +       # Signature accuracy
            doc_score * 0.2              # Documentation
        )

        # Generate detailed report
        report = self._generate_report(evaluation)

        artifacts = [
            Artifact(
                name="extraction_results.json",
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
                "tutorial_recall": f"{tutorial_score:.1%}",
                "function_recall": f"{function_score:.1%}",
                "signature_accuracy": f"{accuracy_score:.1%}",
                "documentation_quality": f"{doc_score:.1%}",
                "final_score": f"{final_score:.1%}"
            },
            artifacts=artifacts
        )

    def _evaluate_extraction(
        self,
        extracted_tutorials: List[Dict],
        extracted_functions: List[Dict],
        expected_tutorials: List[str],
        expected_functions: List[Dict]
    ) -> Dict[str, Any]:
        """Evaluate extraction quality following Paper2Agent methodology."""

        # Tutorial discovery evaluation
        extracted_tutorial_names = {t.get("name", "") for t in extracted_tutorials}
        expected_tutorial_set = set(expected_tutorials)

        tutorial_hits = len(extracted_tutorial_names & expected_tutorial_set)
        tutorial_recall = tutorial_hits / len(expected_tutorial_set) if expected_tutorial_set else 0
        tutorial_precision = tutorial_hits / len(extracted_tutorial_names) if extracted_tutorial_names else 0

        # Function extraction evaluation
        extracted_func_names = {f.get("name", "") for f in extracted_functions}
        expected_func_names = {f.get("name", "") for f in expected_functions}

        function_hits = len(extracted_func_names & expected_func_names)
        function_recall = function_hits / len(expected_func_names) if expected_func_names else 0
        function_precision = function_hits / len(extracted_func_names) if extracted_func_names else 0

        # Signature accuracy (for matched functions)
        signature_matches = 0
        for extracted_func in extracted_functions:
            for expected_func in expected_functions:
                if extracted_func.get("name") == expected_func.get("name"):
                    if self._compare_signatures(extracted_func, expected_func):
                        signature_matches += 1
                    break

        signature_accuracy = signature_matches / function_hits if function_hits > 0 else 0

        # Documentation quality
        documented_functions = sum(
            1 for f in extracted_functions
            if f.get("documentation") and len(f.get("documentation", "")) > 20
        )
        doc_quality = documented_functions / len(extracted_functions) if extracted_functions else 0

        return {
            "tutorial_recall": tutorial_recall,
            "tutorial_precision": tutorial_precision,
            "function_recall": function_recall,
            "function_precision": function_precision,
            "signature_accuracy": signature_accuracy,
            "documentation_quality": doc_quality,
            "extracted_tutorials": len(extracted_tutorials),
            "extracted_functions": len(extracted_functions),
            "expected_tutorials": len(expected_tutorials),
            "expected_functions": len(expected_functions),
            "tutorial_details": list(extracted_tutorial_names),
            "function_details": list(extracted_func_names)
        }

    def _compare_signatures(self, extracted: Dict, expected: Dict) -> bool:
        """Compare function signatures for accuracy."""
        # Compare parameter names
        extracted_params = set(extracted.get("parameters", []))
        expected_params = set(expected.get("parameters", []))

        param_match = extracted_params == expected_params

        # Compare return type if specified
        return_match = True
        if "return_type" in expected:
            return_match = extracted.get("return_type") == expected.get("return_type")

        return param_match and return_match

    def _generate_report(self, evaluation: Dict) -> str:
        """Generate Paper2Agent-style evaluation report."""
        tutorial_recall = evaluation.get("tutorial_recall", 0)
        function_recall = evaluation.get("function_recall", 0)
        signature_acc = evaluation.get("signature_accuracy", 0)
        doc_quality = evaluation.get("documentation_quality", 0)

        report = f"""# Research Code Extraction Assessment Report

## Executive Summary

This assessment evaluates an agent's ability to extract functional code from research
repositories, following the Paper2Agent methodology for tutorial discovery and tool extraction.

## Performance Metrics

### Tutorial Discovery
- **Recall:** {tutorial_recall:.1%}
- **Precision:** {evaluation.get('tutorial_precision', 0):.1%}
- **Extracted:** {evaluation.get('extracted_tutorials', 0)}
- **Expected:** {evaluation.get('expected_tutorials', 0)}

### Function Extraction
- **Recall:** {function_recall:.1%}
- **Precision:** {evaluation.get('function_precision', 0):.1%}
- **Extracted:** {evaluation.get('extracted_functions', 0)}
- **Expected:** {evaluation.get('expected_functions', 0)}

### Code Quality
- **Signature Accuracy:** {signature_acc:.1%}
- **Documentation Quality:** {doc_quality:.1%}

## Detailed Results

### Tutorials Identified
{chr(10).join(f"- {t}" for t in evaluation.get('tutorial_details', []))}

### Functions Extracted
{chr(10).join(f"- {f}" for f in evaluation.get('function_details', []))}

## Paper2Agent Alignment

This assessment follows Paper2Agent's core capabilities:
1. ✓ Automated tutorial discovery
2. ✓ Code extraction from notebooks
3. ✓ Function signature preservation
4. ✓ Documentation generation

## Scoring Breakdown

| Metric | Weight | Score | Contribution |
|--------|--------|-------|--------------|
| Tutorial Discovery | 30% | {tutorial_recall:.1%} | {tutorial_recall * 0.3:.1%} |
| Function Extraction | 30% | {function_recall:.1%} | {function_recall * 0.3:.1%} |
| Signature Accuracy | 20% | {signature_acc:.1%} | {signature_acc * 0.2:.1%} |
| Documentation | 20% | {doc_quality:.1%} | {doc_quality * 0.2:.1%} |

## Recommendations

{"✅ Excellent extraction capabilities!" if tutorial_recall > 0.8 else "⚠️ Needs improvement in tutorial discovery"}
{"✅ Strong function extraction!" if function_recall > 0.8 else "⚠️ Missing key functions"}
{"✅ Accurate signatures!" if signature_acc > 0.8 else "⚠️ Signature preservation issues"}
{"✅ Well documented!" if doc_quality > 0.7 else "⚠️ Improve documentation"}

---
*Based on Paper2Agent methodology for automated research code extraction*
"""
        return report


async def main():
    """Run the green agent server."""
    import argparse

    parser = argparse.ArgumentParser(description="Research Code Extraction Evaluator")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9020, help="Port to bind to")
    args = parser.parse_args()

    evaluator = ResearchCodeExtractionEvaluator(host=args.host, port=args.port)

    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║  Research Code Extraction Evaluator (Green Agent)                ║
║  Based on Paper2Agent methodology                                 ║
║  Running at: {evaluator.url:48s} ║
╚═══════════════════════════════════════════════════════════════════╝

Evaluates agents on:
  • Tutorial/notebook discovery
  • Function extraction accuracy
  • Signature preservation
  • Documentation quality

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
