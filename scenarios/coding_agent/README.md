# Coding Agent Benchmark

A green agent benchmark for evaluating coding capabilities of AI agents.

## Overview

This benchmark tests an agent's ability to:
- Understand programming task descriptions
- Generate syntactically correct code
- Pass test cases with correct logic
- Handle edge cases

## Components

### Green Agent (Evaluator)
- **File:** `green_agent.py`
- **Port:** 9018
- **Role:** Evaluates coding submissions by running test cases

### Purple Agent (Coder)
- **File:** `purple_agent.py`
- **Port:** 9019
- **Role:** Solves programming challenges using LLM

## Running the Benchmark

### 1. Setup Environment

```bash
# Install dependencies
uv sync

# Configure API keys
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run Scenario

```bash
# From project root
uv run python src/agentbeats/run_scenario.py scenarios/coding_agent/scenario.toml --show-logs
```

### 3. Run Manually (separate terminals)

Terminal 1 - Green Agent:
```bash
uv run python scenarios/coding_agent/green_agent.py
```

Terminal 2 - Purple Agent:
```bash
uv run python scenarios/coding_agent/purple_agent.py
```

Terminal 3 - Trigger Assessment:
```bash
# TODO: Implement assessment trigger client
```

## Evaluation Criteria

The benchmark evaluates:
1. **Correctness:** Does the code pass all test cases?
2. **Completeness:** Is the solution fully implemented?
3. **Efficiency:** Does it handle all inputs within time limits?

## Score Calculation

```
Score = (Passed Tests / Total Tests) * 100%
```

- **100%:** Perfect solution
- **80-99%:** Good solution with minor issues
- **50-79%:** Partial solution
- **<50%:** Incomplete or incorrect

## Extending the Benchmark

### Add More Test Cases

Edit `scenario.toml` and add test cases:

```toml
[[assessment.config.test_cases]]
input = "20"
expected = "6765"
description = "F(20) = 6765"
```

### Support More Languages

Modify `green_agent.py` to add language support:

```python
if language == "javascript":
    # Run with node
    result = subprocess.run(["node", temp_file], ...)
elif language == "java":
    # Compile and run Java
    ...
```

### Create New Challenges

1. Copy `scenario.toml` to `scenario_challenge2.toml`
2. Update task description and test cases
3. Run with new config file

## Competition Track

This benchmark is designed for the **Coding Agent** track (Nebius sponsored) in the AgentX-AgentBeats Competition Phase 1.

### Submission Requirements

- A2A protocol compliance
- Automated scoring
- Multiple difficulty levels
- Comprehensive test coverage
- Clear documentation

## Future Improvements

- [ ] Support multiple programming languages
- [ ] Add complexity analysis
- [ ] Memory usage tracking
- [ ] Code quality metrics (style, comments)
- [ ] Security vulnerability detection
- [ ] Performance benchmarking
- [ ] Multi-file projects
- [ ] Debugging challenges

## References

Inspired by:
- **SWE-bench:** Real-world GitHub issues
- **USACO:** Competitive programming challenges
- **LeetCode:** Algorithm problems
- **HumanEval:** Code generation benchmarks
