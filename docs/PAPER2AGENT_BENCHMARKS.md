# Paper2Agent-Based Research Benchmarks

## Overview

This suite implements three comprehensive benchmarks for the **Research Agent** track of the AgentX-AgentBeats Competition, based on the methodology from [Paper2Agent](https://github.com/jmiao24/Paper2Agent).

### What is Paper2Agent?

Paper2Agent is an automated system that transforms research paper codebases into functional AI agents. It:
- Discovers tutorials in research repositories
- Executes notebooks to validate functionality
- Extracts reusable tools from research code
- Generates MCP (Model Context Protocol) servers
- Ensures quality through pytest-cov and pylint

Our benchmarks evaluate these exact capabilities.

## Three Benchmark Suite

### 1. Research Code Extraction 🔍

**Evaluates**: Tutorial discovery and code extraction from research repositories

**Based on**: Paper2Agent Steps 1-2 (Discovery & Extraction)

**Key Metrics**:
- Tutorial discovery recall/precision
- Function extraction accuracy
- Signature preservation
- Documentation quality

**Port**: 9020 (Green Agent)

**Difficulty**: Medium

**Directory**: `scenarios/research_code_extraction/`

[📖 Full Documentation](../scenarios/research_code_extraction/README.md)

---

### 2. Tutorial Understanding 📓

**Evaluates**: Notebook execution and tool generation capabilities

**Based on**: Paper2Agent Steps 2-3 (Execution & Tool Generation)

**Key Metrics**:
- Notebook execution success
- Output accuracy
- Tool extraction quality
- Visualization capture
- Error handling

**Port**: 9021 (Green Agent)

**Difficulty**: Medium-High

**Directory**: `scenarios/tutorial_understanding/`

[📖 Full Documentation](../scenarios/tutorial_understanding/README.md)

---

### 3. Research Reproducibility ✓

**Evaluates**: Result reproduction with comprehensive QA

**Based on**: Paper2Agent Steps 4-5 (QA & MCP Generation)

**Key Metrics**:
- Test suite quality
- Code coverage (pytest-cov, target 80%+)
- Code quality (pylint, target 7.0+)
- Result reproducibility
- MCP server generation

**Port**: 9022 (Green Agent)

**Difficulty**: High

**Directory**: `scenarios/research_reproducibility/`

[📖 Full Documentation](../scenarios/research_reproducibility/README.md)

## Quick Start

### Run All Benchmarks

```bash
# Benchmark 1: Code Extraction
uv run python src/agentbeats/run_scenario.py \
  scenarios/research_code_extraction/scenario.toml \
  --show-logs

# Benchmark 2: Tutorial Understanding
uv run python src/agentbeats/run_scenario.py \
  scenarios/tutorial_understanding/scenario.toml \
  --show-logs

# Benchmark 3: Reproducibility
uv run python src/agentbeats/run_scenario.py \
  scenarios/research_reproducibility/scenario.toml \
  --show-logs
```

### Run Individual Green Agents

```bash
# Code Extraction (port 9020)
uv run python scenarios/research_code_extraction/green_agent.py

# Tutorial Understanding (port 9021)
uv run python scenarios/tutorial_understanding/green_agent.py

# Reproducibility (port 9022)
uv run python scenarios/research_reproducibility/green_agent.py
```

### Unified Purple Agent

All three benchmarks share a single purple agent:

```bash
# Research Purple Agent (port 9023)
uv run python scenarios/research_code_extraction/purple_agent.py
```

## Paper2Agent Pipeline Mapping

```
Paper2Agent Full Pipeline          Our Benchmark Suite
================================   ===================================

Step 1: Repository Analysis    →   Benchmark 1: Code Extraction
  - Scan repository structure       - Tutorial discovery
  - Identify tutorials              - Function extraction
  - Analyze code structure          - Signature preservation

Step 2: Notebook Execution     →   Benchmark 2: Tutorial Understanding
  - Execute notebooks               - Execution success
  - Capture outputs                 - Output validation
  - Handle errors                   - Error handling

Step 3: Tool Extraction        →   Benchmark 2: Tutorial Understanding
  - Extract functions               - Tool generation
  - Generate interfaces             - Tool quality
  - Create documentation            - Documentation

Step 4: Quality Analysis       →   Benchmark 3: Reproducibility
  - Run pytest-cov                  - Test generation
  - Execute pylint                  - Coverage metrics
  - Generate reports                - Quality scores

Step 5: MCP Server Creation    →   Benchmark 3: Reproducibility
  - Build MCP server                - MCP validation
  - Define tool interfaces          - Server structure
  - Deploy to platform              - Integration ready
```

## Comprehensive Evaluation

### Combined Scoring

An agent's overall Paper2Agent capability score:

```python
Overall Score = (
    Code Extraction Score × 0.30 +
    Tutorial Understanding × 0.35 +
    Reproducibility Score × 0.35
)
```

### Performance Tiers

| Tier | Score Range | Description |
|------|-------------|-------------|
| **Excellent** | 90-100% | Production-ready research agent |
| **Good** | 80-89% | Solid capabilities, minor gaps |
| **Fair** | 70-79% | Functional but needs improvement |
| **Poor** | <70% | Significant capability gaps |

## Competition Strategy

### Phase 1 Submission (Dec 19, 2025)

Submit all three benchmarks as a comprehensive suite:

**Strengths**:
- ✅ Based on proven methodology (Paper2Agent)
- ✅ Covers complete research workflow
- ✅ Real-world applicability
- ✅ Measurable quality metrics
- ✅ Multiple difficulty levels

**Differentiators**:
- Complete research pipeline coverage
- Integration of industry-standard tools (pytest, pylint)
- MCP protocol alignment
- Reproducibility focus (critical for research)

### Building a Winning Purple Agent

To excel across all three benchmarks:

1. **Code Extraction**
   - Implement robust AST parsing
   - Use heuristics for tutorial identification
   - Leverage LLM for semantic understanding

2. **Tutorial Understanding**
   - Build notebook execution engine
   - Capture all output types
   - Generate comprehensive tools

3. **Reproducibility**
   - Create sophisticated test generator
   - Integrate pytest-cov properly
   - Meet quality thresholds consistently

## Architecture

### Project Structure

```
scenarios/
├── research_code_extraction/
│   ├── green_agent.py          # Evaluator (port 9020)
│   ├── purple_agent.py         # Shared agent (port 9023)
│   ├── scenario.toml           # Configuration
│   └── README.md               # Documentation
│
├── tutorial_understanding/
│   ├── green_agent.py          # Evaluator (port 9021)
│   ├── purple_agent.py         # Symlink to shared
│   ├── scenario.toml
│   └── README.md
│
└── research_reproducibility/
    ├── green_agent.py          # Evaluator (port 9022)
    ├── purple_agent.py         # Symlink to shared
    ├── scenario.toml
    └── README.md
```

### Shared Components

All benchmarks use:
- Same purple agent implementation
- Common AgentBeats SDK
- Unified A2A protocol
- Consistent evaluation framework

## Research Domains Covered

The benchmarks work across multiple research domains:

### Bioinformatics
- Sequence analysis
- Genomic variant interpretation
- Spatial transcriptomics

### Machine Learning
- Model training pipelines
- Hyperparameter tuning
- Result visualization

### Data Science
- Statistical analysis
- Data preprocessing
- Exploratory data analysis

### Computational Science
- Numerical simulations
- Scientific computing
- Algorithm implementation

## Quality Standards

Following Paper2Agent's production requirements:

### Code Coverage
- **Minimum**: 80%
- **Target**: 85%+
- **Excellent**: 90%+

### Code Quality (pylint)
- **Minimum**: 7.0/10
- **Target**: 8.0/10
- **Excellent**: 8.5/10

### Reproducibility
- **Numerical Tolerance**: 1%
- **Statistical Significance**: p < 0.05
- **Result Matching**: 95%+

## Extending the Benchmarks

### Add New Research Domains

```toml
# In scenario.toml
[assessment.config]
research_domain = "physics"
domain_specific_metrics = ["simulation_accuracy", "convergence_rate"]
```

### Custom Quality Metrics

```python
# In green_agent.py
def _evaluate_domain_specific(self, results):
    domain_score = calculate_physics_accuracy(results)
    return domain_score
```

### Multi-Repository Evaluation

```toml
[[assessment.repositories]]
url = "https://github.com/org/repo1"
expected_tutorials = [...]

[[assessment.repositories]]
url = "https://github.com/org/repo2"
expected_tutorials = [...]
```

## Best Practices

### For Benchmark Development
1. Use real research repositories
2. Validate with actual papers
3. Test across domains
4. Maintain quality thresholds

### For Agent Development
1. Study Paper2Agent codebase
2. Implement incrementally
3. Test each capability separately
4. Optimize for quality metrics

## Troubleshooting

### Common Issues

**Import Errors**:
```bash
uv run python your_script.py
```

**Port Conflicts**:
```bash
# Kill processes
lsof -ti:9020 | xargs kill -9
lsof -ti:9021 | xargs kill -9
lsof -ti:9022 | xargs kill -9
lsof -ti:9023 | xargs kill -9
```

**API Rate Limits**:
- Use local LLMs (Ollama)
- Implement caching
- Batch requests

## Testing

### Validate Green Agents

```bash
# Test each green agent
uv run python scenarios/research_code_extraction/green_agent.py
uv run python scenarios/tutorial_understanding/green_agent.py
uv run python scenarios/research_reproducibility/green_agent.py
```

### Validate Purple Agent

```bash
# Test shared purple agent
uv run python scenarios/research_code_extraction/purple_agent.py
```

### Run Full Assessments

```bash
# Test complete workflows
for scenario in research_code_extraction tutorial_understanding research_reproducibility; do
  uv run python src/agentbeats/run_scenario.py \
    scenarios/$scenario/scenario.toml \
    --show-logs
done
```

## Metrics Dashboard

Example consolidated results:

```
╔═══════════════════════════════════════════════════════════════╗
║ Paper2Agent Benchmark Suite Results                          ║
╠═══════════════════════════════════════════════════════════════╣
║ Code Extraction                                               ║
║   Tutorial Recall:        92.3%                              ║
║   Function Extraction:    88.5%                              ║
║   Overall Score:          90.2%  ✅                          ║
╠═══════════════════════════════════════════════════════════════╣
║ Tutorial Understanding                                        ║
║   Execution Success:      100%                               ║
║   Output Accuracy:        87.0%                              ║
║   Overall Score:          91.5%  ✅                          ║
╠═══════════════════════════════════════════════════════════════╣
║ Research Reproducibility                                      ║
║   Coverage:               86.0%                              ║
║   Pylint Score:           8.2/10                             ║
║   Reproducibility:        95.0%                              ║
║   Overall Score:          88.7%  ✅                          ║
╠═══════════════════════════════════════════════════════════════╣
║ COMBINED SCORE:           90.1%  ✅ EXCELLENT                ║
╚═══════════════════════════════════════════════════════════════╝
```

## Resources

### Paper2Agent
- **Repository**: https://github.com/jmiao24/Paper2Agent
- **Documentation**: See repo README
- **Examples**: AlphaGenome, TISSUE, Scanpy

### Competition
- **Website**: https://agentbeats.org
- **Track**: Research Agent
- **Deadline**: December 19, 2025

### Related Papers
- CORE-Bench (Computational Reproducibility)
- SciCode (Scientific Coding)
- Research agent benchmarks (see PAPERS_INDEX.md)

## Future Roadmap

### Planned Enhancements
- [ ] Multi-language support (R, Julia)
- [ ] Container-based execution
- [ ] Distributed testing
- [ ] Real-time monitoring
- [ ] Advanced error recovery
- [ ] Incremental execution
- [ ] GPU support

### Research Opportunities
- Novel tool extraction methods
- Better reproducibility metrics
- Cross-paper validation
- Meta-research capabilities

## Contributing

Contributions welcome! Areas of interest:
- Additional research domains
- New quality metrics
- Enhanced purple agents
- Documentation improvements

## Citation

If you use these benchmarks:

```bibtex
@misc{agentx_paper2agent_benchmarks,
  title={Paper2Agent-Based Research Benchmarks for AgentBeats},
  author={AgentX Hackathon Team},
  year={2025},
  howpublished={AgentX-AgentBeats Competition},
  note={Based on Paper2Agent methodology}
}
```

---

**Competition Track**: Research Agent
**Based on**: Paper2Agent (https://github.com/jmiao24/Paper2Agent)
**Benchmarks**: 3 comprehensive evaluations
**Total Coverage**: Complete research workflow pipeline
**Difficulty**: Medium to High
**Estimated Assessment Time**: 15-60 minutes per benchmark

**Built for AgentX-AgentBeats Competition Phase 1** 🏆
