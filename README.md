# AgentX-AgentBeats Competition Project

> Building innovative Green Agents (benchmarks) and Purple Agents (competitors) for the AgentX-AgentBeats Competition

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 📋 Competition Overview

This project is developed for the **AgentX-AgentBeats Competition** hosted by Berkeley RDI, featuring:

- **$1M+ in prizes and resources**
- **Two-phase competition structure**
- Focus on advancing standardized, reproducible agent evaluation

### Competition Phases

#### 🟢 Phase 1: Green Agent Development (Oct 16 - Dec 20, 2025)
Build green agents (evaluators) that define assessments and automate scoring. Choose from tracks including:
- Agent Safety (Lambda sponsored)
- Coding Agent (Nebius sponsored)
- Healthcare, Web, Research, Security, and more

#### 🟣 Phase 2: Purple Agent Competition (Jan 12 - Feb 23, 2026)
Build purple agents to excel on top Phase 1 benchmarks and compete on public leaderboards.

## 🎯 Core Concepts

### Green Agents (Evaluators)
- Orchestrate and manage evaluations
- Provide evaluation harness and environments
- Define rules, host assessments, and compute scores
- Built using the A2A protocol

### Purple Agents (Competitors)
- Agents being evaluated
- Demonstrate skills (coding, research, security, etc.)
- Tested against green agent benchmarks
- Must comply with A2A and MCP standards

### AAA (Agentified Agent Assessment)
A new paradigm for open, standardized, and reproducible agent evaluation:
- **Standardization**: A2A protocol for task management, MCP for tool access
- **Reproducibility**: Clean state for each assessment run
- **Interoperability**: Any compliant agent works with any benchmark

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv (package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd agentXhackathon
```

2. **Install dependencies**
```bash
uv sync
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Get your API keys**
- Google Gemini: https://aistudio.google.com/apikey
- OpenAI (optional): https://platform.openai.com/api-keys
- Anthropic (optional): https://console.anthropic.com/

### Running Your First Assessment

```bash
# Start the green agent server
uv run python scenarios/your_scenario/green_agent.py

# In another terminal, start the purple agent
uv run python scenarios/your_scenario/purple_agent.py

# Run the assessment
uv run agentbeats-run scenarios/your_scenario/scenario.toml
```

## 📂 Project Structure

```
agentXhackathon/
├── src/
│   └── agentbeats/          # Core AgentBeats SDK components
│       ├── green_executor.py # Base A2A green agent executor
│       ├── models.py         # Pydantic models for agent IO
│       ├── client.py         # A2A messaging helpers
│       └── run_scenario.py   # Scenario orchestration
├── scenarios/               # Green agent implementations
│   └── [your_track]/       # Your green agent track
│       ├── green_agent.py   # Green agent implementation
│       ├── purple_agent.py  # Test purple agent
│       └── scenario.toml    # Configuration file
├── papers/                  # Research papers and references
├── docs/                    # Additional documentation
├── tests/                   # Unit and integration tests
├── pyproject.toml          # Project dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## 🎨 Available Competition Tracks

Choose one or create your own:

1. **Agent Safety** - Red-teaming and security testing
2. **Coding Agent** - Software development tasks
3. **Healthcare Agent** - Medical workflow automation
4. **Web Agent** - Browser-based task completion
5. **Computer Use Agent** - Desktop automation
6. **Research Agent** - Academic research tasks
7. **Cybersecurity Agent** - Security operations
8. **Finance Agent** - Financial analysis tasks
9. **Game Agent** - Gaming and strategy
10. **Multi-agent Evaluation** - Collaborative assessments

## 📚 Key Resources

### Official Documentation
- [Competition Website](https://agentbeats.org)
- [Tutorial Repository](https://github.com/agentbeats/tutorial)
- [A2A Protocol Documentation](https://a2a.dev)
- [Competition Blog Series](https://rdi.berkeley.edu)

### Papers and Benchmarks
See `papers/` directory for research papers on:
- SWE-bench, GAIA, BrowserGym, OSWorld
- CyberGym, DoomArena, WASP (security)
- MedAgentBench, LegalAgentBench, Finance Agent Benchmark
- And 30+ more benchmarks with papers

### Community
- [Discord Community](https://discord.gg/agentbeats)
- [Agentic AI MOOC](https://rdi.berkeley.edu/mooc) - 32K+ learners

## 🏗️ Development Workflow

### 1. Design Your Green Agent
```python
# Define your benchmark tasks
# Implement evaluation logic
# Create scoring mechanisms
```

### 2. Build Test Purple Agents
```python
# Create baseline agents for testing
# Ensure A2A protocol compliance
```

### 3. Local Testing
```bash
# Test assessments locally
uv run agentbeats-run scenarios/your_track/scenario.toml --show-logs
```

### 4. Deploy to Platform
```bash
# Expose agent with Cloudflare Tunnel
cloudflared tunnel --url http://127.0.0.1:9019

# Register on agentbeats.org
```

## 💡 Best Practices

### Security & Cost Management
- **Use BYOK model** - Bring Your Own Keys
- **Set spending limits** on API accounts
- **Never commit API keys** to version control
- **Use environment variables** for sensitive data

### Efficient Assessments
- **Minimize network chattiness** between agents
- **Set appropriate timeouts** for operations
- **Process data locally** when possible
- **Emit traces** for observability

### Reproducibility
- **Start each assessment fresh** - no state carryover
- **Isolate contexts** using task_id namespacing
- **Reset state** between runs
- **Use A2A artifacts** for output storage

## 🏆 Prizes & Sponsors

- **DeepMind**: Up to $50K in GCP/Gemini credits
- **Lambda**: $750 per winning team + $400 credits for all
- **Nebius**: Up to $50K in inference credits + $50 for all
- **Amazon**: Up to $10K in AWS credits
- **Snowflake**: 6-month access + $240 credits for students

## 📊 Submission Guidelines

### Phase 1 (Green Agents)
- **Deadline**: December 19, 2025
- **Requirements**:
  - A2A protocol compliance
  - Complete documentation
  - Test purple agents included
  - GitHub repository

### Phase 2 (Purple Agents)
- **Deadline**: February 22, 2026
- **Requirements**:
  - Works with Phase 1 green agents
  - A2A + MCP compliance
  - Leaderboard submission

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Important Links

- **Competition Website**: https://agentbeats.org
- **Berkeley RDI**: https://rdi.berkeley.edu
- **Tutorial**: https://github.com/agentbeats/tutorial
- **A2A Protocol**: https://a2a.dev
- **Discord**: Join for support and community

## 📧 Contact & Support

- Join the [Discord community](https://discord.gg/agentbeats)
- Enroll in the [Agentic AI MOOC](https://rdi.berkeley.edu/mooc)
- Check the [competition website](https://agentbeats.org) for updates

---

**Built for AgentX-AgentBeats Competition 2025**
*Advancing the state of the art in agentic AI through benchmarks and evaluation*
