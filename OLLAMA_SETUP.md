# Ollama Setup Guide

This project uses Ollama for local LLM inference instead of OpenAI. Follow these steps to set up Ollama.

## Installation

### Windows
1. Download Ollama from: https://ollama.ai/download
2. Run the installer
3. Ollama will start automatically as a service

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### macOS
```bash
brew install ollama
```

## Download the Model

After installing Ollama, download the recommended model:

```bash
ollama pull llama3.1:8b
```

Other recommended models:
- `llama3.1:8b` - Good balance of speed and quality (recommended)
- `llama2:13b` - Better quality, slower
- `mistral:7b` - Fast and efficient
- `codellama:7b` - Optimized for code tasks

## Verify Installation

Check if Ollama is running:

```bash
ollama list
```

Test the model:

```bash
ollama run llama3.1:8b "Hello, how are you?"
```

## Configuration

Update your `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Using Different Models

To use a different model:

1. Pull the model:
```bash
ollama pull mistral:7b
```

2. Update `.env`:
```env
OLLAMA_MODEL=mistral:7b
```

## Troubleshooting

### Ollama not responding
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama (Linux/macOS)
systemctl restart ollama

# Windows: Restart from Services or Task Manager
```

### Model not found
```bash
# List available models
ollama list

# Pull the model if missing
ollama pull llama3.1:8b
```

### Performance Issues
- Use smaller models (7b instead of 13b)
- Ensure you have enough RAM (8GB minimum for 7b models)
- Close other applications to free up resources

## API Endpoints

Ollama runs on `http://localhost:11434` by default with these endpoints:
- `/api/generate` - Generate completions
- `/api/chat` - Chat completions
- `/api/tags` - List available models

The CrewAI agents will automatically use these endpoints through the LangChain Ollama integration.
