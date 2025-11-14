# Competition Papers and Benchmarks Reference

This directory contains references to research papers and benchmarks relevant to the AgentX-AgentBeats competition.

## How to Use This Resource

1. **Choose your track** (Coding, Security, Healthcare, etc.)
2. **Review relevant papers** to understand state-of-the-art
3. **Identify gaps** you can address with your green agent
4. **Design your benchmark** inspired by existing work
5. **Cite references** in your submission

## Benchmark Categories

### 🖥️ Coding & Software Engineering

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **SWE-bench** | Real GitHub issues | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | https://arxiv.org/abs/2310.06770 |
| **SWE-bench Verified** | Human-validated subset | Introducing SWE-bench Verified | https://openai.com/swe-bench-verified |
| **SciCode** | Scientific computing | SciCode: A Research Coding Benchmark Curated by Scientists | https://arxiv.org/abs/2407.13168 |
| **USACO** | Competitive programming | Can Language Models Solve Olympiad Programming? | https://arxiv.org/abs/2404.10952 |
| **VERINA** | Verified code generation | VERINA: Benchmarking Verifiable Code Generation | https://arxiv.org/abs/2505.23135 |

### 🌐 Web Agents

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **BrowserGym** | Web navigation | The BrowserGym Ecosystem for Web Agent Research | https://arxiv.org/abs/2412.05467 |
| **Online-Mind2Web** | Live web tasks | An Illusion of Progress? Assessing LLM Web Agents | https://arxiv.org/abs/2504.01382 |
| **WebShop** | E-commerce tasks | WebShop: Towards Scalable Real-World Web Interaction | https://arxiv.org/abs/2207.01206 |

### 🔒 Security & Safety

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **CyberGym** | Vulnerability detection | CyberGym: Evaluating AI Agents' Cybersecurity Capabilities | https://arxiv.org/abs/2506.02548 |
| **DoomArena** | Framework security | DoomArena: Testing AI Agents Against Security Threats | https://arxiv.org/abs/2504.14064 |
| **WASP** | Prompt injection | WASP: Web Agent Security Against Prompt Injection | https://arxiv.org/abs/2504.18575 |
| **OpenAgentSafety** | Real-world safety | OpenAgentSafety: Framework for AI Agent Safety | https://arxiv.org/abs/2507.06134 |
| **Smart Contract Exploit** | Blockchain security | AI Agent Smart Contract Exploit Generation | https://arxiv.org/abs/2507.05558 |

### 🖥️ Computer Use & Desktop

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **OSWorld** | Desktop tasks | OSWorld: Benchmarking Multimodal Agents for Real Computer Environments | https://arxiv.org/abs/2404.07972 |
| **TerminalBench** | Command-line tasks | terminal-bench: Benchmark for AI Agents in Terminal | https://www.tbench.ai/ |
| **TheAgentCompany** | Digital worker tasks | Benchmarking LLM Agents on Consequential Real World Tasks | https://arxiv.org/abs/2412.14161 |

### 🏥 Healthcare

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **MedAgentBench** | EHR workflows | MedAgentBench: Realistic Virtual EHR Environment | https://arxiv.org/abs/2501.14654 |

### ⚖️ Legal

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **LegalAgentBench** | Legal reasoning | LegalAgentBench: Evaluating LLM Agents in Legal Domain | https://arxiv.org/abs/2412.17259 |

### 💰 Finance

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **Finance Agent Benchmark** | Financial research | Finance Agent Benchmark: LLMs on Real-world Financial Research | https://arxiv.org/abs/2508.00828 |
| **Spider 2.0** | Enterprise SQL | Spider 2.0: Enterprise Text-to-SQL Workflows | https://arxiv.org/abs/2411.07763 |

### 💼 Enterprise & Business

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **CRMArena** | CRM tasks | CRMArena: LLM Agents in Professional Scenarios | https://arxiv.org/abs/2411.02305 |
| **CRMArena-Pro** | Expanded CRM | CRMArena-Pro: Holistic Assessment Across Business Scenarios | https://arxiv.org/abs/2505.18878 |
| **AppWorld** | Multi-app environment | AppWorld: A Controllable World of Apps and People | https://arxiv.org/abs/2407.18901 |

### 🎮 Gaming & Social

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **Werewolf Game** | Social deduction | Werewolf Arena: LLM Evaluation via Social Deduction | https://arxiv.org/abs/2407.13943 |
| **Minecraft Gaming** | Open-ended games | MCU: Evaluation Framework for Open-Ended Game Agents | https://arxiv.org/abs/2310.08367 |
| **ALFWorld** | Text-to-embodied tasks | ALFWorld: Aligning Text and Embodied Environments | https://arxiv.org/abs/2010.03768 |
| **Agent Battle Royale** | Multi-agent survival | Tweet concept | https://x.com/SIGKITTEN/status/1937950811910234377 |

### 🔧 General Purpose & Tools

| Benchmark | Focus Area | Paper | Link |
|-----------|-----------|-------|------|
| **GAIA** | Real-world assistant tasks | GAIA: A Benchmark for General AI Assistants | https://arxiv.org/abs/2311.12983 |
| **τ-bench** | Tool-agent-user interaction | τ-bench: Real-World Domain Interaction | https://arxiv.org/abs/2406.12045 |
| **τ²-bench** | Dual-control evaluation | τ²-Bench: Conversational Agents in Dual-Control Setting | https://arxiv.org/abs/2506.07982 |
| **CORE-Bench** | Computational reproducibility | CORE-Bench: Reproducibility Agent Benchmark | https://arxiv.org/abs/2409.11363 |
| **PersonaGym** | Persona-following | PersonaGym: Evaluating Persona Agents and LLMs | https://arxiv.org/abs/2407.18416 |

## Downloading Papers

### Using arXiv Links

```bash
# Download a specific paper
wget https://arxiv.org/pdf/2310.06770.pdf -O papers/swe-bench.pdf

# Download multiple papers
cd papers/
wget https://arxiv.org/pdf/2407.13168.pdf -O scicode.pdf
wget https://arxiv.org/pdf/2412.05467.pdf -O browsergym.pdf
```

### Organize by Track

```bash
mkdir -p papers/{coding,security,web,healthcare,legal,finance,gaming}

# Move papers to appropriate folders
mv papers/swe-bench.pdf papers/coding/
mv papers/cybergym.pdf papers/security/
```

## How to Cite

When building your green agent, cite relevant prior work:

```markdown
## References

This benchmark is inspired by and builds upon:

- **SWE-bench**: Jimenez et al. (2023) - Real-world GitHub issue resolution
- **BrowserGym**: Drouin et al. (2024) - Web agent evaluation ecosystem
```

## Competition Strategy

### 1. Port Existing Benchmarks
- Choose a benchmark from the list
- **Agentify it** - convert to A2A protocol
- **Extend it** - add new features or test cases
- **Document thoroughly**

### 2. Create Novel Benchmarks
- Identify gaps in existing benchmarks
- Design new evaluation criteria
- Create diverse, challenging tasks
- Ensure reproducibility

### 3. Combine Approaches
- Multi-benchmark evaluation
- Cross-domain challenges
- Composite scoring

## Key Papers to Read First

### For Understanding Agent Evaluation
1. **AAA Paper** (in `agentsbeatdocs.md`) - Core evaluation paradigm
2. **GAIA** - General-purpose agent benchmarking
3. **τ-bench** - Tool use evaluation

### For Your Specific Track

**Coding:**
- SWE-bench (most influential)
- SciCode (scientific domain)

**Security:**
- CyberGym (vulnerability detection)
- DoomArena (framework security)

**Web:**
- BrowserGym (comprehensive)
- Online-Mind2Web (realistic scenarios)

**Healthcare:**
- MedAgentBench (only major benchmark in this space - opportunity!)

## Contributing

Found a new paper? Add it to this index:

1. Add to the appropriate category table
2. Include: Name, Focus, Paper Title, Link
3. Keep alphabetically sorted
4. Update the download scripts if needed

## Notes

- **Papers are NOT included in the repository** (large files)
- Download papers you need from arXiv links
- Most papers are open access
- Check license before using benchmarks

## Additional Resources

- **AgentBeats Blog Series:** https://rdi.berkeley.edu/blog
- **A2A Protocol Spec:** https://a2a.dev
- **Competition Discord:** For paper discussions
- **MOOC Materials:** https://rdi.berkeley.edu/mooc

---

**Last Updated:** November 2025
**Total Papers Listed:** 33
**Categories:** 10
