# Getting Started with AgentX-AgentBeats

This guide will help you get started with building and testing agents for the competition.

## Prerequisites

- **Python 3.11+**
- **uv** package manager
- **Git**
- **API Keys** (at least one):
  - Google Gemini API key (recommended, has free tier)
  - OpenAI API key (optional)
  - Anthropic API key (optional)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd agentXhackathon
```

### 2. Install Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment
- Install all required packages
- Set up the project in editable mode

### 3. Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Get your API keys:**
- **Google Gemini:** https://aistudio.google.com/apikey (Free tier available)
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/

### 4. Verify Installation

```bash
# Check Python version
python3 --version  # Should be 3.11+

# Verify uv installation
uv --version

# Test import
uv run python -c "from agentbeats import GreenAgentExecutor; print('✓ AgentBeats SDK loaded')"
```

## Running Your First Assessment

### Quick Start - Coding Agent Scenario

```bash
# Run the full scenario (starts all agents automatically)
uv run python src/agentbeats/run_scenario.py \
  scenarios/coding_agent/scenario.toml \
  --show-logs
```

### Manual Mode - Step by Step

For development and debugging, run agents separately:

**Terminal 1 - Green Agent (Evaluator):**
```bash
uv run python scenarios/coding_agent/green_agent.py
```

**Terminal 2 - Purple Agent (Coder):**
```bash
uv run python scenarios/coding_agent/purple_agent.py
```

**Terminal 3 - Run Assessment:**
```bash
# TODO: Assessment trigger client coming soon
```

## Project Structure

```
agentXhackathon/
├── src/agentbeats/           # Core SDK
│   ├── __init__.py
│   ├── models.py             # Data models
│   ├── client.py             # A2A client
│   ├── green_executor.py     # Green agent base
│   └── run_scenario.py       # Scenario runner
│
├── scenarios/                # Agent implementations
│   └── coding_agent/        # Example: Coding benchmark
│       ├── green_agent.py   # Evaluator
│       ├── purple_agent.py  # Solver
│       ├── scenario.toml    # Configuration
│       └── README.md        # Documentation
│
├── docs/                     # Documentation
├── papers/                   # Research references
└── tests/                    # Tests
```

## Next Steps

### For Phase 1 (Building Green Agents)

1. **Choose your track:**
   - Agent Safety
   - Coding Agent
   - Healthcare, Web, Security, etc.

2. **Design your benchmark:**
   - Define evaluation criteria
   - Create test cases
   - Implement scoring logic

3. **Implement your green agent:**
   ```bash
   # Create new scenario
   mkdir -p scenarios/my_track
   cp scenarios/coding_agent/green_agent.py scenarios/my_track/
   # Edit and customize
   ```

4. **Build test purple agents:**
   - Create baseline agents
   - Test your evaluation logic

5. **Document everything:**
   - Write clear README
   - Add usage examples
   - Document scoring methodology

### For Phase 2 (Building Purple Agents)

1. **Select benchmarks to compete on**
2. **Build your agent:**
   - Implement A2A protocol
   - Add required capabilities
   - Optimize for benchmarks

3. **Test locally:**
   ```bash
   # Run against green agents
   uv run python scenarios/[track]/scenario.toml
   ```

4. **Deploy to AgentBeats platform**

## Development Tips

### Using the SDK

```python
from agentbeats import (
    GreenAgentExecutor,
    A2AClient,
    TaskUpdate,
    AssessmentResult,
    Artifact
)

# Build a green agent
class MyEvaluator(GreenAgentExecutor):
    async def setup_assessment(self, task_id, participants, config):
        # Setup environment
        pass

    async def run_assessment(self, task_id, participants, config):
        # Run evaluation
        yield TaskUpdate(task_id=task_id, status="in_progress", ...)

    async def evaluate_results(self, task_id, collected_data):
        # Score and return results
        return AssessmentResult(task_id=task_id, score=0.95, ...)
```

### Adding Test Cases

Edit `scenario.toml`:

```toml
[[assessment.config.test_cases]]
input = "test input"
expected = "expected output"
description = "What this tests"
```

### Debugging

```bash
# Show detailed logs
uv run python src/agentbeats/run_scenario.py \
  scenarios/my_track/scenario.toml \
  --show-logs

# Run agents only (no assessment)
uv run python src/agentbeats/run_scenario.py \
  scenarios/my_track/scenario.toml \
  --serve-only
```

### Cost Management

- Start with free-tier APIs (Google Gemini)
- Set spending limits on API keys
- Use local LLMs for development (Ollama)
- Test with small datasets first

## Common Issues

### Import Errors

```bash
# Make sure you're using uv run
uv run python your_script.py

# Or activate the venv
source .venv/bin/activate
python your_script.py
```

### API Key Issues

```bash
# Check if key is loaded
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"
```

### Port Already in Use

```bash
# Kill process on port 9018
lsof -ti:9018 | xargs kill -9

# Or change port in scenario.toml
```

## Resources

- **Competition Website:** https://agentbeats.org
- **A2A Protocol:** https://a2a.dev
- **Tutorial Repo:** https://github.com/agentbeats/tutorial
- **Discord:** Join for community support
- **MOOC:** https://rdi.berkeley.edu/mooc

## Getting Help

1. Check the documentation in `docs/`
2. Review example scenarios in `scenarios/`
3. Join the Discord community
4. Open an issue on GitHub

## What's Next?

- **Read:** Competition requirements in `about_the_hackathon.md`
- **Explore:** Example benchmarks in `AgentBeats_Competition_Green_Agent_Track_Ideas.md`
- **Build:** Your own green agent
- **Test:** Locally before deploying
- **Submit:** To the competition by Dec 19, 2025

Happy building! 🚀
