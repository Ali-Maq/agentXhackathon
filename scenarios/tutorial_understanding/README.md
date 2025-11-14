# Tutorial Understanding Benchmark

**Based on Paper2Agent's Notebook Execution Pipeline**

## Overview

This benchmark evaluates an AI agent's ability to understand and execute research tutorials, following the [Paper2Agent](https://github.com/jmiao24/Paper2Agent) approach for executing notebooks and generating functional tools from research code.

### Paper2Agent Methodology

Paper2Agent's execution pipeline:
1. **Notebook Execution**: Running tutorials in isolated environments
2. **Output Capture**: Recording cell outputs and visualizations
3. **Error Handling**: Managing execution failures gracefully
4. **Tool Generation**: Extracting reusable functions
5. **Documentation**: Creating comprehensive tool descriptions

## Evaluation Criteria

This benchmark tests five key capabilities:

### 1. Execution Success (25%)
- Successful execution of all notebook cells
- Proper environment setup
- Dependency management

### 2. Output Accuracy (25%)
- Correctness of cell outputs
- Numerical precision
- String formatting

### 3. Tool Quality (25%)
- Generation of reusable functions
- Complete function signatures
- Proper documentation

### 4. Visualization Capture (15%)
- Detection of generated plots
- Saving of visualization outputs
- Image metadata extraction

### 5. Error Handling (10%)
- Graceful error recovery
- Informative error messages
- Continuation after failures

## Running the Benchmark

### Quick Start

```bash
# From project root
uv run python src/agentbeats/run_scenario.py \
  scenarios/tutorial_understanding/scenario.toml \
  --show-logs
```

### Manual Mode

Terminal 1 - Green Agent:
```bash
uv run python scenarios/tutorial_understanding/green_agent.py
```

Terminal 2 - Purple Agent:
```bash
uv run python scenarios/tutorial_understanding/purple_agent.py
```

## Configuration

Edit `scenario.toml` to customize:

```toml
[assessment.config]
notebook_content = """
# Your research tutorial here
import numpy as np
...
"""

[assessment.config.expected_outputs]
"1" = "Expected output from cell 1"
"2" = "Expected output from cell 2"

expected_tools = ["function1", "function2"]
```

## Scoring

```
Final Score = (
    Execution Success × 0.25 +
    Output Accuracy × 0.25 +
    Tool Quality × 0.25 +
    Visualization Score × 0.15 +
    Error Handling × 0.10
)
```

### Performance Levels

- **90-100%**: Excellent - Perfect execution and tool generation
- **80-89%**: Good - Minor output mismatches
- **70-79%**: Fair - Some execution issues
- **<70%**: Poor - Major execution or extraction failures

## Example Output

```json
{
  "execution_success": true,
  "cells_executed": 12,
  "tools_generated": 5,
  "visualizations_created": 3,
  "errors_encountered": 0,
  "execution_score": 1.0,
  "output_accuracy": 0.92,
  "tool_quality": 0.88,
  "visualization_score": 1.0,
  "error_handling_score": 1.0,
  "final_score": 0.92
}
```

## Paper2Agent Context

This benchmark implements Paper2Agent's core execution pipeline:

**Step 2**: Notebook Execution
- Execute tutorials in clean environments
- Capture all outputs systematically
- Handle errors without complete failure

**Step 3**: Tool Extraction
- Convert tutorial code to reusable functions
- Generate proper tool interfaces
- Create comprehensive documentation

The evaluation criteria mirror Paper2Agent's quality checks before including extracted tools in the final MCP server.

## Benchmark Scenarios

### Scenario 1: Data Analysis Tutorial
**Domain**: Statistical analysis
**Cells**: 8 code cells
**Expected Tools**: `load_data`, `preprocess`, `analyze`, `visualize`
**Visualizations**: 2 plots

### Scenario 2: Machine Learning Tutorial
**Domain**: Model training
**Cells**: 15 code cells
**Expected Tools**: `prepare_dataset`, `train_model`, `evaluate`, `predict`
**Visualizations**: 4 plots (loss curves, confusion matrix)

### Scenario 3: Bioinformatics Tutorial
**Domain**: Sequence analysis
**Cells**: 10 code cells
**Expected Tools**: `load_sequences`, `align`, `score`, `visualize_alignment`
**Visualizations**: 3 plots

## Extending the Benchmark

### Add Custom Tutorials

```python
[assessment.config]
notebook_content = """
# Your custom research tutorial
import your_library

# Tutorial content...
"""
```

### Custom Output Validation

Modify `green_agent.py`:

```python
def _compare_outputs(self, actual, expected):
    # Add custom comparison logic
    if is_image(expected):
        return compare_images(actual, expected)
    # ... existing logic
```

## Best Practices

### For Green Agent Developers
1. Provide diverse tutorial types
2. Include both successful and error-prone notebooks
3. Test with real research code
4. Validate visualization capture

### For Purple Agent Developers
1. Implement robust notebook parsing
2. Handle various output formats
3. Capture all visualization types
4. Generate comprehensive documentation
5. Manage dependencies properly

## Competition Submission

### Phase 1 Requirements

✅ Multiple tutorial types (data analysis, ML, domain-specific)
✅ Varying difficulty levels
✅ Realistic research scenarios
✅ Comprehensive error handling tests
✅ Visualization capture evaluation

### Innovation Opportunities

- Multi-language notebook support (R, Julia)
- Interactive widget handling
- Large output management
- Incremental execution
- Checkpoint/resume functionality

## Debugging

### Common Issues

**Execution Failures:**
```bash
# Check dependencies
pip install -r requirements.txt

# Test notebook manually
jupyter nbconvert --execute tutorial.ipynb
```

**Output Mismatches:**
- Normalize whitespace
- Allow numerical tolerance
- Handle different output formats

**Tool Extraction:**
- Verify function definitions
- Check indentation
- Validate signatures

## Metrics Deep Dive

### Tool Quality Calculation

```python
tool_quality = (
    tool_recall +        # Did we extract all expected tools?
    tool_completeness    # Are tools fully documented?
) / 2
```

### Output Accuracy

```python
output_accuracy = (
    matching_outputs / total_expected_outputs
)
```

## References

- **Paper2Agent**: https://github.com/jmiao24/Paper2Agent
- **Jupyter Notebooks**: https://jupyter.org
- **nbconvert**: https://nbconvert.readthedocs.io

## Future Enhancements

- [ ] Jupyter widget support
- [ ] R kernel notebooks
- [ ] GPU execution handling
- [ ] Long-running cell management
- [ ] Interactive debugging
- [ ] Checkpoint creation
- [ ] Incremental execution

---

**Track**: Research Agent
**Based on**: Paper2Agent notebook execution
**Difficulty**: Medium-High
**Estimated Time**: 15-45 minutes per assessment
