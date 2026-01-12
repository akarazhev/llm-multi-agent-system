# Cursor Agent SDK Integration

This project uses the **cursor-agent-tools** SDK to power the multi-agent system with AI capabilities.

## What is cursor-agent-tools?

`cursor-agent-tools` is a Python SDK that replicates Cursor's coding assistant capabilities, enabling:
- Function calling and code generation
- Intelligent coding assistance
- Support for multiple LLM providers (Claude, OpenAI, Ollama)

## Setup

### 1. Install Dependencies

Already done if you ran the setup:
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys (Auto Model Selection)

The system uses **AUTO model selection** - just set your API key and it will automatically choose the best available model!

#### Option A: Anthropic Claude (Recommended)

1. Get API key from https://console.anthropic.com/
2. Add to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

That's it! The system will automatically use Claude 3.5 Sonnet.

#### Option B: OpenAI

1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

The system will automatically use GPT-4o.

#### Option C: Ollama (Local, Free)

1. Install Ollama from https://ollama.ai/
2. Pull a model: `ollama pull llama3.2`
3. Add to `.env`:
```bash
OLLAMA_HOST=http://localhost:11434
```

The system will automatically use available Ollama models.

### 3. Create .env File

```bash
cp .env.example .env
# Edit .env with your API key (just one line!)
```

### Auto Model Selection

The system automatically detects and uses the best available model:
- If `ANTHROPIC_API_KEY` is set → Uses Claude 3.5 Sonnet
- If `OPENAI_API_KEY` is set → Uses GPT-4o  
- If `OLLAMA_HOST` is set → Uses Llama 3.2
- You can override with `ANTHROPIC_API_MODEL` or `OPENAI_API_MODEL` if needed

## How It Works

Each agent in the system:
1. Receives a task with context
2. Uses its specialized system prompt
3. Calls the cursor-agent-tools SDK
4. Gets AI-generated response
5. Returns structured results

### Agent Flow

```
Task → Agent → cursor-agent-tools → LLM API → Response → Agent → Result
```

### Code Example

```python
from cursor_agent_tools import create_agent

# Create agent with system prompt
agent = create_agent(
    model='claude-3-5-sonnet-latest',
    system_prompt='You are an expert developer...'
)

# Execute task
response = await agent.chat('Create a REST API...')
```

## Supported Models

### Anthropic Claude
- `claude-3-5-sonnet-latest` (Recommended)
- `claude-3-opus-latest`
- `claude-3-sonnet-20240229`

### OpenAI
- `gpt-4o` (Recommended)
- `gpt-4-turbo`
- `gpt-3.5-turbo`

### Ollama (Local)
- `llama3.2`
- `codellama`
- `mistral`
- Any model available via Ollama

## Cost Estimates

### Per Task (approximate)

**Anthropic Claude:**
- Claude 3.5 Sonnet: $0.015 - $0.075
- Claude 3 Opus: $0.075 - $0.375

**OpenAI:**
- GPT-4o: $0.03 - $0.15
- GPT-3.5-turbo: $0.002 - $0.01

**Ollama:**
- Free (runs locally)

### Full Workflow (6 tasks)
- Claude 3.5 Sonnet: ~$0.10 - $0.50
- GPT-4o: ~$0.20 - $1.00
- Ollama: Free

## Testing Your Setup

### Quick Test

```bash
source venv/bin/activate

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-your-key

# Test import
python -c "from cursor_agent_tools import create_agent; print('✓ SDK installed')"
```

### Run Simple Example

```bash
source venv/bin/activate
python examples/simple_workflow.py
```

## Troubleshooting

### "No API keys configured"
- Ensure you've set at least one API key in `.env`
- Load environment: `source .env` or use `python-dotenv`

### "Module not found: cursor_agent_tools"
```bash
pip install cursor-agent-tools
```

### "Invalid API key"
- Check your API key is correct
- Verify it's active in your provider's dashboard
- Ensure no extra spaces in `.env`

### "Rate limit exceeded"
- Wait a few minutes
- Upgrade your API plan
- Use a different provider

### Ollama connection error
```bash
# Start Ollama
ollama serve

# Pull a model
ollama pull llama3.2
```

## Advanced Configuration

### Custom System Prompts

Each agent has a specialized system prompt defined in its class:

```python
class DeveloperAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are an expert Software Developer...
        - Write clean, maintainable code
        - Follow SOLID principles
        ..."""
```

### Timeout Configuration

Adjust in `config.yaml`:
```yaml
cursor_timeout: 300  # seconds
task_timeout: 600
```

### Model Selection

Priority order:
1. Anthropic (if `ANTHROPIC_API_KEY` set)
2. OpenAI (if `OPENAI_API_KEY` set)
3. Ollama (if `OLLAMA_HOST` set)

## Benefits of cursor-agent-tools

✅ **Multiple Providers** - Claude, OpenAI, or local Ollama  
✅ **Function Calling** - Built-in tool support  
✅ **Code Generation** - Optimized for coding tasks  
✅ **Easy Integration** - Simple async API  
✅ **Well Maintained** - Active development  

## Resources

- [cursor-agent-tools GitHub](https://github.com/civai-technologies/cursor-agent)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Ollama Documentation](https://ollama.ai/docs)

## Next Steps

1. Set up your API keys
2. Run a test example
3. Try building a real project
4. Customize agent prompts for your needs

Happy coding! 🚀
