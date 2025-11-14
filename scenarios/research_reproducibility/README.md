# Research Reproducibility Benchmark

**Based on Paper2Agent's Quality Assurance Pipeline**

## Overview

This benchmark evaluates an AI agent's ability to reproduce research results with comprehensive quality assurance, following [Paper2Agent](https://github.com/jmiao24/Paper2Agent)'s methodology using pytest-cov for coverage and pylint for code quality.

### Paper2Agent QA Methodology

Paper2Agent ensures quality through:
1. **Test Suite Generation**: Comprehensive pytest tests
2. **Code Coverage**: pytest-cov analysis (targeting 80%+)
3. **Style Analysis**: pylint quality scores (7.0/10+)
4. **Result Validation**: Reproducing published results
5. **MCP Server Generation**: Creating functional AI tool interfaces

## Evaluation Criteria

This benchmark tests five key capabilities:

### 1. Test Suite Quality (20%)
- Comprehensive test coverage
- Test pass rate
- Edge case handling

### 2. Code Coverage (20%)
- Overall coverage percentage
- Critical path coverage
- pytest-cov metrics

### 3. Code Quality (20%)
- Pylint score (0-10)
- Style compliance
- Documentation quality

### 4. Result Reproducibility (30%)
- Accuracy of reproduced results
- Numerical precision matching
- Statistical significance

### 5. MCP Server Generation (10%)
- Valid MCP server structure
- Tool interface completeness
- Integration readiness

## Running the Benchmark

### Quick Start

```bash
# From project root
uv run python src/agentbeats/run_scenario.py \
  scenarios/research_reproducibility/scenario.toml \
  --show-logs
```

### Manual Mode

Terminal 1 - Green Agent:
```bash
uv run python scenarios/research_reproducibility/green_agent.py
```

Terminal 2 - Purple Agent:
```bash
uv run python scenarios/research_reproducibility/purple_agent.py
```

## Configuration

Edit `scenario.toml` to customize:

```toml
[assessment.config]
research_code = """
# Research code to reproduce
def train_model(...):
    ...
"""

[assessment.config.paper_results]
accuracy = 0.945
f1_score = 0.932

target_coverage = 85  # %
target_pylint_score = 8.0  # /10
```

## Scoring

```
Final Score = (
    Test Suite Quality × 0.20 +
    Code Coverage × 0.20 +
    Code Quality (pylint) × 0.20 +
    Result Reproducibility × 0.30 +
    MCP Server × 0.10
)
```

### Performance Levels

- **90-100%**: Excellent - Production-ready reproducible research
- **80-89%**: Good - Meets Paper2Agent quality standards
- **70-79%**: Fair - Some quality/reproducibility issues
- **<70%**: Poor - Significant problems with reproduction

## Example Output

```json
{
  "test_score": 0.95,
  "coverage_score": 0.92,
  "quality_score": 0.85,
  "reproducibility_score": 0.98,
  "mcp_score": 1.0,
  "tests_passed": 48,
  "tests_total": 50,
  "coverage_percent": 88.5,
  "pylint_score": 8.5,
  "results_matched": 5,
  "results_total": 5,
  "final_score": 0.93
}
```

## Paper2Agent Context

This benchmark implements Paper2Agent's final quality assurance stages:

**Step 4**: Quality Analysis
- Run pytest with coverage tracking
- Execute pylint for code quality
- Generate comprehensive reports

**Step 5**: MCP Server Generation
- Create Model Context Protocol server
- Define tool interfaces
- Enable AI assistant integration

The benchmark uses the same quality thresholds Paper2Agent applies before deploying agents to Hugging Face.

## Quality Metrics

### Coverage Analysis (pytest-cov)

```python
# Paper2Agent targets
target_coverage = 80%  # Minimum
ideal_coverage = 90%   # Excellent

# Reports generated:
- coverage.xml     # XML format
- coverage.json    # JSON format
- htmlcov/         # HTML report
```

### Code Quality (pylint)

```python
# Paper2Agent standards
target_score = 7.0/10  # Minimum
ideal_score = 8.5/10   # Excellent

# Checks include:
- Style compliance (PEP 8)
- Documentation quality
- Code complexity
- Best practices
```

## Benchmark Scenarios

### Scenario 1: Machine Learning Reproduction
**Paper Result**: Accuracy 94.5%, F1 0.932
**Code**: Random Forest classifier
**Tests Required**: 20+ tests
**Target Coverage**: 85%
**Target Quality**: 8.0

### Scenario 2: Statistical Analysis
**Paper Result**: p-value 0.023, effect size 0.45
**Code**: Statistical tests and visualizations
**Tests Required**: 15+ tests
**Target Coverage**: 90%
**Target Quality**: 8.5

### Scenario 3: Computational Biology
**Paper Result**: Alignment score 0.87, sensitivity 0.92
**Code**: Sequence alignment algorithms
**Tests Required**: 25+ tests
**Target Coverage**: 88%
**Target Quality**: 7.5

## Extending the Benchmark

### Add Custom Research Code

```toml
[assessment.config]
research_code = """
# Your research implementation
import numpy as np

def your_method(...):
    ...
"""

[assessment.config.paper_results]
your_metric = 0.95
```

### Custom Quality Thresholds

```toml
target_coverage = 90      # Raise coverage bar
target_pylint_score = 9.0 # Stricter quality
```

## Best Practices

### For Green Agent Developers
1. Use realistic research code
2. Provide accurate paper results
3. Set appropriate quality thresholds
4. Test with various domains

### For Purple Agent Developers
1. Generate comprehensive test suites
2. Aim for high coverage
3. Follow coding standards
4. Document thoroughly
5. Validate numerical results

## Tools Integration

### pytest-cov

```bash
# Run coverage analysis
pytest --cov=module --cov-report=json tests/

# Generate HTML report
pytest --cov=module --cov-report=html tests/
```

### pylint

```bash
# Run quality analysis
pylint module/ --output-format=json > pylint_report.json

# Check specific score
pylint module/ --score=y
```

## Competition Submission

### Phase 1 Requirements

✅ Multiple research domains
✅ Realistic paper results
✅ Comprehensive quality metrics
✅ Automated pytest/pylint integration
✅ MCP server validation

### Innovation Opportunities

- Multi-domain reproducibility
- Statistical significance testing
- Confidence interval matching
- Publication bias detection
- Data availability checking
- Computational reproducibility

## Debugging

### Low Coverage Issues

```python
# Identify uncovered lines
coverage report --show-missing

# Focus on critical paths
pytest --cov=module --cov-report=term-missing
```

### Pylint Score Improvement

```python
# Check specific issues
pylint module/ --reports=y

# Disable specific checks (sparingly)
# pylint: disable=line-too-long
```

### Result Mismatches

```python
# Allow numerical tolerance
assert abs(actual - expected) < 0.01

# Check randomness
np.random.seed(42)  # Fix random state
```

## Metrics Deep Dive

### Coverage Score Calculation

```python
coverage_score = min(
    actual_coverage / target_coverage,
    1.0
)
```

### Quality Score Calculation

```python
quality_score = min(
    pylint_score / target_quality,
    1.0
)
```

### Reproducibility Score

```python
matches = sum(
    compare_result(actual, expected)
    for actual, expected in zip(reproduced, paper)
)
reproducibility_score = matches / total_results
```

## MCP Server Requirements

Valid MCP server structure:

```python
{
    "name": "research_tools",
    "tools": [
        {
            "name": "tool1",
            "description": "...",
            "parameters": [...]
        },
        ...
    ]
}
```

## References

- **Paper2Agent**: https://github.com/jmiao24/Paper2Agent
- **pytest-cov**: https://pytest-cov.readthedocs.io
- **pylint**: https://pylint.readthedocs.io
- **MCP**: Model Context Protocol

## Future Enhancements

- [ ] Statistical test validation
- [ ] Confidence interval checking
- [ ] Multi-run reproducibility
- [ ] Cross-platform testing
- [ ] Performance benchmarking
- [ ] Memory profiling
- [ ] Docker containerization

---

**Track**: Research Agent
**Based on**: Paper2Agent QA pipeline
**Difficulty**: High
**Estimated Time**: 20-60 minutes per assessment
**Quality Standards**: pytest-cov 80%+, pylint 7.0+
