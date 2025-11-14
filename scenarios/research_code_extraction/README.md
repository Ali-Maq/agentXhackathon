# Research Code Extraction Benchmark

**Based on Paper2Agent's Tutorial Discovery Methodology**

## Overview

This benchmark evaluates an AI agent's ability to automatically extract functional code from research repositories, following the [Paper2Agent](https://github.com/jmiao24/Paper2Agent) approach for discovering and extracting tutorials from academic codebases.

### Paper2Agent Methodology

Paper2Agent automatically transforms research papers into interactive AI agents through:
1. **Tutorial Discovery**: Scanning repositories to identify relevant tutorials/notebooks
2. **Code Extraction**: Extracting functional code and key functions
3. **Signature Preservation**: Maintaining function signatures accurately
4. **Documentation Generation**: Creating comprehensive documentation

## Evaluation Criteria

This benchmark tests four key capabilities:

### 1. Tutorial Discovery (30%)
- Ability to identify notebooks and tutorial files
- Recognition of tutorial naming patterns
- Precision and recall in discovery

### 2. Function Extraction (30%)
- Extraction of key functions from tutorials
- Identification of core functionality
- Completeness of extraction

### 3. Signature Accuracy (20%)
- Preservation of parameter names
- Return type identification
- Type annotation accuracy

### 4. Documentation Quality (20%)
- Extraction of docstrings
- Generation of meaningful descriptions
- Code comprehension

## Running the Benchmark

### Quick Start

```bash
# From project root
uv run python src/agentbeats/run_scenario.py \
  scenarios/research_code_extraction/scenario.toml \
  --show-logs
```

### Manual Mode

Terminal 1 - Green Agent:
```bash
uv run python scenarios/research_code_extraction/green_agent.py
```

Terminal 2 - Purple Agent:
```bash
uv run python scenarios/research_code_extraction/purple_agent.py
```

## Configuration

Edit `scenario.toml` to customize:

```toml
[assessment.config]
repository_url = "https://github.com/your-repo/research-code"
expected_tutorials = ["tutorial1.ipynb", "tutorial2.ipynb"]

[[assessment.config.expected_functions]]
name = "process_data"
parameters = ["input", "config"]
return_type = "DataFrame"
```

## Scoring

```
Final Score = (
    Tutorial Discovery × 0.30 +
    Function Extraction × 0.30 +
    Signature Accuracy × 0.20 +
    Documentation Quality × 0.20
)
```

### Performance Levels

- **90-100%**: Excellent - Production-ready extraction
- **80-89%**: Good - Minor improvements needed
- **70-79%**: Fair - Significant gaps in extraction
- **<70%**: Poor - Major issues with discovery/extraction

## Example Output

```json
{
  "tutorial_recall": 0.95,
  "function_recall": 0.88,
  "signature_accuracy": 0.92,
  "documentation_quality": 0.85,
  "final_score": 0.90
}
```

## Paper2Agent Context

This benchmark directly implements Paper2Agent's first pipeline stage:
- **Step 1**: Repository structure analysis
- **Step 2**: Tutorial/notebook identification
- **Step 3**: Function extraction and cataloging

The evaluation mirrors the quality metrics Paper2Agent uses to determine which tutorials to include as tools.

## Benchmark Examples

### Example 1: Bioinformatics Repository
- **Expected**: 3 tutorials on sequence analysis
- **Functions**: `load_sequences`, `align`, `calculate_scores`
- **Challenge**: Domain-specific naming conventions

### Example 2: Machine Learning Repository
- **Expected**: 5 tutorials on model training
- **Functions**: `prepare_data`, `train`, `evaluate`, `predict`
- **Challenge**: Multiple implementations of similar functions

### Example 3: Data Analysis Repository
- **Expected**: 4 tutorials on statistical analysis
- **Functions**: `load_data`, `clean`, `analyze`, `visualize`
- **Challenge**: Nested function definitions

## Extending the Benchmark

### Add More Repositories

```toml
[[scenarios]]
repository_url = "https://github.com/new-research/code"
expected_tutorials = [...]
```

### Custom Evaluation Metrics

Modify `green_agent.py`:

```python
def _evaluate_extraction(self, ...):
    # Add custom metrics
    domain_specific_score = ...
    return {**existing_metrics, "domain_score": domain_specific_score}
```

## Competition Submission

### Requirements for Phase 1

✅ A2A protocol compliance
✅ Automated scoring based on Paper2Agent methodology
✅ Multiple difficulty levels
✅ Comprehensive documentation
✅ Baseline purple agent included

### Judging Criteria

1. **Innovation**: Novel approaches to code extraction
2. **Coverage**: Variety of repository types
3. **Accuracy**: Precision in extraction
4. **Reproducibility**: Consistent results

## References

- **Paper2Agent**: https://github.com/jmiao24/Paper2Agent
- **AgentBeats Tutorial**: https://github.com/agentbeats/tutorial
- **Competition**: https://agentbeats.org

## Future Enhancements

- [ ] Multi-language support (beyond Python)
- [ ] Dependency graph extraction
- [ ] Class hierarchy analysis
- [ ] Cross-reference detection
- [ ] API endpoint identification
- [ ] Configuration file parsing

---

**Track**: Research Agent
**Based on**: Paper2Agent tutorial discovery
**Difficulty**: Medium
**Estimated Time**: 10-30 minutes per assessment
