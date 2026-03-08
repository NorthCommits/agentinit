# agentinit

A CLI tool to scaffold production-ready LLM agent projects in seconds.

Stop copy-pasting boilerplate. Run one command and get a fully structured, framework-specific agent project ready to run.

## Install

```bash
pip install agentinit
```

## Usage

```bash
agentinit init my-project --framework langgraph --llm openai
```

## Supported Frameworks

| Framework | Description |
|---|---|
| `langgraph` | LangChain's graph-based agent framework |
| `crewai` | Multi-agent role-based framework |
| `autogen` | Microsoft's conversational agent framework |
| `google_adk` | Google's Agent Development Kit |
| `openai_agents` | OpenAI's official agents SDK |
| `smolagents` | HuggingFace's lightweight agent framework |

## Supported LLM Providers

| Provider | Env Variable |
|---|---|
| `openai` | `OPENAI_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `groq` | `GROQ_API_KEY` |
| `azure` | `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` |
| `bedrock` | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |
| `gemini` | `GOOGLE_API_KEY` |

## Generated Project Structure

```
my-project/
├── agents/
│   └── base_agent.py    # framework-specific agent logic
├── tools/
│   └── sample_tool.py   # sample tool stub
├── config/
│   └── config.yaml      # llm and project config
├── Dockerfile           # ready to containerize
├── main.py              # entry point
├── .env.example         # environment variable template
└── requirements.txt     # dependencies for chosen framework
```

## Commands

### Scaffold a new project
```bash
agentinit init <project-name> --framework <framework> --llm <provider>
```

### Add a new agent to an existing project
```bash
cd my-project
agentinit add-agent researcher --framework langgraph
```

### List all supported frameworks and providers
```bash
agentinit list-frameworks
```

## Examples

```bash
# LangGraph with OpenAI
agentinit init my-agent --framework langgraph --llm openai

# CrewAI with Anthropic
agentinit init my-crew --framework crewai --llm anthropic

# AutoGen with Groq
agentinit init my-autogen --framework autogen --llm groq

# Google ADK with Gemini
agentinit init my-adk --framework google_adk --llm gemini

# OpenAI Agents SDK with Azure
agentinit init my-openai-agent --framework openai_agents --llm azure

# Smolagents with Bedrock
agentinit init my-smol --framework smolagents --llm bedrock
```

## Getting Started After Scaffolding

```bash
cd my-project
cp .env.example .env       # add your API keys
pip install -r requirements.txt
python main.py
```

## License

MIT