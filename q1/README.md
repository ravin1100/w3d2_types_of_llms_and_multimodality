# LLM Model Comparison Tool

This command-line tool helps users compare different types of language models (Base, Instruct, and Fine-tuned) from popular providers like OpenAI, Google (Gemini), and Hugging Face.

## Features

- Compare responses from different model types and providers
- Display model characteristics and capabilities
- Track token usage
- Optional visualization of token usage
- Support for multiple providers:
  - OpenAI (gpt-3.5-turbo)
  - Google Gemini (gemini-pro)
  - Hugging Face (TinyLlama-1.1B-Chat-v1.0)

## Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repo-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys for OpenAI and Google

## Usage

Basic usage:
```bash
python model_comparison.py --prompt "Your prompt here" --provider openai
```

Options:
- `--prompt`: The input prompt for the models (required)
- `--model-type`: Type of model to use (base/instruct/fine-tuned)
- `--provider`: Model provider to use (openai/gemini/huggingface)
- `--show-viz`: Show token usage visualization
- `--interactive` or `-i`: Run in interactive mode

Examples:
```bash
# Use OpenAI's GPT-3.5-turbo
python model_comparison.py --prompt "Explain quantum computing" --provider openai

# Use Google's Gemini Pro
python model_comparison.py --prompt "Write a poem about AI" --provider gemini

# Use HuggingFace's TinyLlama
python model_comparison.py --prompt "Summarize this text" --provider huggingface

# Run in interactive mode
python model_comparison.py --interactive
```

## Model Characteristics

### GPT-3.5-turbo (OpenAI)
- Type: Instruct
- Context Window: 4096 tokens
- Optimized for: Dialogue and instruction following

### Gemini Pro (Google)
- Type: Instruct
- Context Window: 32k tokens
- Optimized for: Reasoning and multimodal capabilities
- Features: Strong performance in coding, analysis, and creative tasks

### TinyLlama-1.1B-Chat (HuggingFace)
- Type: Base with chat fine-tuning
- Context Window: 2048 tokens
- Optimized for: Efficient, lightweight chat applications

## Note on API Keys

To use this tool, you'll need API keys from:
- OpenAI: Get from [OpenAI Platform](https://platform.openai.com/)
- Google: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

Store these in your `.env` file as shown in `.env.example`. 