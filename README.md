# Agent Generator Marketplace

Transform natural language descriptions into production-ready LangGraph agents instantly through Claude Code.

## Installation

```bash
/plugin marketplace add https://github.com/adrianpuiu/agent-generator-marketplace
/plugin install agent-generator
```

## Available Plugins

### agent-generator
Generate production-ready LangGraph agents from natural language.

```bash
/generate-agent "describe what your agent should do"
```

See [agent-generator-plugin/README.md](agent-generator-plugin/README.md) for details.

## Quick Start

```bash
# Generate an agent
/generate-agent "search the web and summarize results"

# Get list of available tools
/list-tools

# See the generated files
# - generated_agent.py (executable)
# - requirements.txt (dependencies)
# - setup_instructions.md (deployment guide)
```

## What You Get

When you run `/generate-agent`, you instantly receive:

1. **Python Script** (500+ lines)
   - Tool definitions
   - Error handling
   - Logging
   - Memory integration
   - Ready to run

2. **Requirements File**
   - Auto-extracted dependencies
   - Pinned versions

3. **Setup Guide**
   - Environment variables
   - Deployment options
   - Troubleshooting

## Learn More

- [Plugin Documentation](agent-generator-plugin/README.md)
- [Agent Generator Skill](agent-generator-plugin/skills/agent-generator/SKILL.md)
- [Generate Agent Command](agent-generator-plugin/commands/generate-agent.md)

## License

MIT License - See [LICENSE.md](agent-generator-plugin/LICENSE.md)
