# Quick Reference - AgentX-AgentBeats

## Essential Commands

### Setup
```bash
# Install dependencies
uv sync

# Configure API key
cp .env.example .env
nano .env  # Add GOOGLE_API_KEY
```

### Run Assessment
```bash
# Automated (recommended)
uv run python src/agentbeats/run_scenario.py scenarios/coding_agent/scenario.toml --show-logs

# Manual mode
# Terminal 1:
uv run python scenarios/coding_agent/green_agent.py

# Terminal 2:
uv run python scenarios/coding_agent/purple_agent.py
```

### Development
```bash
# Run tests
uv run pytest

# Format code
uv run black src/ scenarios/

# Lint
uv run ruff check src/ scenarios/
```

## Important Dates

- **Phase 1 Submission:** December 19, 2025
- **Phase 2 Start:** January 12, 2026
- **Phase 2 Submission:** February 22, 2026

## Key URLs

- **Competition:** https://agentbeats.org
- **Tutorial:** https://github.com/agentbeats/tutorial
- **A2A Protocol:** https://a2a.dev
- **Get Gemini Key:** https://aistudio.google.com/apikey
- **Discord:** Join via competition website

## Project Structure

```
agentXhackathon/
├── src/agentbeats/        # SDK
├── scenarios/             # Your agents
│   └── coding_agent/     # Example
├── papers/               # Research refs
└── docs/                 # Documentation
```

## Core Concepts

| Term | Definition |
|------|------------|
| **Green Agent** | Evaluator - provides benchmarks |
| **Purple Agent** | Competitor - being evaluated |
| **A2A** | Agent-to-Agent protocol |
| **MCP** | Model Context Protocol |
| **AAA** | Agentified Agent Assessment |

## Competition Tracks

1. Agent Safety (Lambda)
2. Coding Agent (Nebius)
3. Healthcare Agent
4. Web Agent
5. Computer Use
6. Research Agent
7. Cybersecurity
8. Finance Agent
9. Legal Agent
10. Multi-agent

## Scoring Criteria

Green agents should provide:
- Clear evaluation metrics
- Automated scoring
- Reproducible results
- A2A compliance
- Documentation

## File Templates

### Green Agent
```python
from agentbeats import GreenAgentExecutor

class MyEvaluator(GreenAgentExecutor):
    async def setup_assessment(self, task_id, participants, config):
        # Setup
        pass

    async def run_assessment(self, task_id, participants, config):
        # Run and yield updates
        yield TaskUpdate(...)

    async def evaluate_results(self, task_id, collected_data):
        # Score
        return AssessmentResult(...)
```

### Purple Agent
```python
from agentbeats import A2AServer

class MyAgent(A2AServer):
    async def handle_task(self, task_id, payload):
        # Process task
        return {"result": ...}
```

### Scenario Config
```toml
[metadata]
name = "My Benchmark"

[agents.green]
command = "python scenarios/my_track/green_agent.py"
url = "http://127.0.0.1:9018"

[agents.purple]
command = "python scenarios/my_track/purple_agent.py"
url = "http://127.0.0.1:9019"

[assessment]
participants = ["purple"]

[assessment.config]
# Your config here
```

## Common Issues

### Import Error
```bash
# Use uv run
uv run python your_script.py
```

### API Key Not Found
```bash
# Check .env file exists
ls -la .env

# Verify key loaded
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', os.getenv('GOOGLE_API_KEY')[:10])"
```

### Port In Use
```bash
# Kill process
lsof -ti:9018 | xargs kill -9

# Or use different port
--port 9020
```

## Cost Tips

- Start with Gemini free tier
- Set API spending limits
- Use Ollama for local testing
- Monitor usage in API dashboard

## Next Steps

1. ✅ Setup complete
2. 📖 Read `GETTING_STARTED.md`
3. 🎯 Choose your track
4. 🏗️ Build your green agent
5. 🧪 Test locally
6. 📤 Submit by Dec 19

## Help

- Docs: `docs/GETTING_STARTED.md`
- Examples: `scenarios/coding_agent/`
- Papers: `papers/PAPERS_INDEX.md`
- Issues: GitHub Issues
- Community: Discord

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-green-agent

# Commit changes
git add .
git commit -m "Add my green agent"

# Push
git push -u origin feature/my-green-agent
```

---

**Quick Links:**
- 📖 [Getting Started](GETTING_STARTED.md)
- 📚 [Papers Index](../papers/PAPERS_INDEX.md)
- 🎯 [Main README](../README.md)
- 💻 [Coding Agent Example](../scenarios/coding_agent/README.md)
