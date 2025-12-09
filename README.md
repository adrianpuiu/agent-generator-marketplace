# Agent Generator Marketplace

Production-ready Claude Code plugin for generating DeepAgents with planning.

## What's This?

A Claude Code plugin marketplace containing the **DeepAgent Architect** plugin - a specialized skill for generating powerful, planning-focused agents from natural language.

## Quick Start

```bash
# In Claude Code
/plugin marketplace add https://github.com/adrianpuiu/agent-generator-marketplace
/plugin install agent-generator

# Then use it
/generate-agent "research emerging AI companies and analyze funding"
```

## DeepAgent Architect Plugin

### What It Does
Transforms natural language into production-ready DeepAgents with:

✅ **Built-In Planning Tools** - Every agent includes planning, decomposition, evaluation  
✅ **Iterative Reasoning** - Multi-step problem solving with refinement cycles  
✅ **Complex Analysis** - Research automation and adaptive workflows  
✅ **Production-Ready Code** - 600+ lines, fully functional immediately  
✅ **Memory Persistence** - Redis/Postgres for long-running sessions  

### Example

```bash
/generate-agent "Research quantum computing startups - identify technology, funding, and competitive positioning"
```

Generates agent that:
1. Plans research approach
2. Searches for companies
3. Gathers funding data
4. Analyzes technology
5. Evaluates competitive position
6. Refines thesis iteratively

With planning tools included automatically.

### Commands

- `/generate-agent "description"` - Create custom DeepAgent
- `/generate-agent "description" --memory redis` - Add Redis memory
- `/list-planning-tools` - Show planning tools and integrations

### What You Get

1. **generated_agent.py** (600+ lines)
   - Complete DeepAgent implementation
   - All planning tools included
   - Error handling and logging
   - Ready to run

2. **requirements.txt**
   - Auto-extracted dependencies
   - Memory backend libraries

3. **setup_instructions.md**
   - Environment setup
   - API key configuration
   - Deployment options

## Use Cases

### Research Automation
```
/generate-agent "Deep dive into AI healthcare: find companies, funding, technology"
```

### Market Analysis
```
/generate-agent "Analyze 100 stocks for unusual patterns and rank top performers"
```

### Problem Solving
```
/generate-agent "Identify system bottlenecks and propose optimization solutions"
```

### Data Analysis
```
/generate-agent "Explore dataset: find correlations, outliers, and patterns"
```

## Key Features

- **Planning-First** - Every agent plans before acting
- **Iterative** - Built-in refinement loops
- **Complex** - Multi-step reasoning, not simple tasks
- **Production** - Complete error handling and logging
- **Instant** - Works immediately, no manual editing

## Technology

- **Framework**: LangGraph DeepAgent
- **Model**: Claude Sonnet 4
- **Memory**: Redis/Postgres/In-Memory
- **Tools**: Web search, finance data, custom APIs

## Plugin Structure

```
agent-generator-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── agent-generator-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/
│   │   ├── generate-agent.md
│   │   └── list-tools.md
│   ├── skills/
│   │   └── agent-generator/
│   │       ├── SKILL.md
│   │       ├── scripts/
│   │       │   ├── generate_agent.py
│   │       │   └── validate_code.py
│   │       └── references/
│   └── README.md
└── README.md
```

## Installation

### Via GitHub (Recommended)

```bash
/plugin marketplace add https://github.com/adrianpuiu/agent-generator-marketplace
/plugin install agent-generator
```

### Via Local Path (Development)

```bash
/plugin marketplace add ./path/to/agent-generator-marketplace
/plugin install agent-generator
```

## Usage

### Basic
```bash
/generate-agent "analyze something"
```

### With Memory
```bash
/generate-agent "long research task" --memory redis
```

### View Tools
```bash
/list-planning-tools
```

## After Installation

```bash
# 1. Generate agent
/generate-agent "your description"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
export FINNHUB_API_KEY="your_key"

# 4. Run
python generated_agent.py "your query"
```

## Customization

Generated agents are fully customizable:
- Implement tool logic with real API calls
- Adjust planning prompts
- Add domain-specific tools
- Integrate with your systems
- Deploy to production

## Documentation

- **Plugin README** - Features and examples
- **SKILL.md** - Detailed skill documentation
- **Generated setup_instructions.md** - Deployment guide

## Technical Details

### DeepAgent vs ReAct

| Aspect | ReAct | DeepAgent |
|--------|-------|-----------|
| **Best For** | Simple tasks | Complex tasks |
| **Planning** | No | Yes (built-in) |
| **Reasoning** | Direct | Iterative |
| **Iterations** | Single | Multiple |
| **Memory** | Simple | Full state |
| **Use Case** | Quick queries | Deep analysis |

This plugin **generates DeepAgents only** - optimized for complex reasoning.

## Phase 1 Implementation ✅

- ✅ DeepAgent-only (removed ReAct fallback)
- ✅ Built-in planning tools (automatic)
- ✅ Updated skill triggers (research, analysis, planning)
- ✅ Improved documentation (clear examples)
- ✅ Simplified parameters (--deep-agent removed)

## Future Phases

Phase 2:
- Specialized commands (/research-agent, /analysis-agent, etc.)
- Config presets (fast, thorough, collaborative)

Phase 3:
- Full sub-agent support
- Advanced memory patterns
- Iteration refinement commands

## Questions?

Check the generated `setup_instructions.md` for deployment help.

---

**Create DeepAgents now**: 
```
/generate-agent "what you want to research or analyze"
```

Made for complex, reasoning-heavy tasks. 🚀
