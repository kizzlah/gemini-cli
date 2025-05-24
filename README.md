# Gemini CLI

This tool allows you to have conversations with Gemini models directly from your terminal. This is me taking advantage of Google providing Gemini Pro "for free" to students for a the following year. By which I mean, I'm utilizing a Gemini API key to access the Gemini fleet of models. Note that even after your API key has been added that the larger, more powerful models will run through you alotted uses rather quickly. The smaller models are useful and fast enough buf I still prefer models by competitors more. 

## Features

- Interactive chat interface with Gemini models
- Support for multiple Gemini models
- Simple command-line arguments
- Configurable model parameters
- Rate limit error handling with helpful messages
- Text wrapping for better readability

## Installation

### Prerequisites

- Python 3.7 or higher
- A Google AI Studio API key
- Generative AI

### Installing from source

```bash
# Clone the repository
git clone https://github.com/yourusername/gemini-cli.git
cd gemini-cli

# Install the package
pip install -e .
```

### Manual installation

```bash
# Install required dependencies
pip install google-generativeai

# Copy the script to a location in your PATH
cp gemini_cli.py ~/.local/bin/gemini-cli
chmod +x ~/.local/bin/gemini-cli
```

## API Key Setup

You need a Google AI API key to use this tool. Get one from [Google AI Studio](https://makersuite.google.com/app/apikey).

Set up your API key as an environment variable:

```bash
export GEMINI_API_KEY='your-api-key'
```

For permanent setup, add the line above to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file.

## Usage

### Basic Chat

```bash
gemini-cli
```

This starts a chat session with the default model (gemini-1.5-flash).

### Chat Commands

- Type your messages and press Enter to send
- Type `exit` or `quit` to end the conversation
- Type `clear` to start a new conversation
- Press `Ctrl+C` to exit

### Using Specific Models

```bash
# Use a specific model
gemini-cli --model models/gemini-1.5-pro

# Use a lighter model (better for rate limits)
gemini-cli --model models/gemini-1.5-flash-8b
```

### List Available Models

```bash
gemini-cli --list-models
```

## Available Models

Different models have different capabilities and rate limits:

| Model | Description | Best for |
|-------|-------------|----------|
| gemini-1.5-flash | Balanced performance | General use, good balance of speed and capability |
| gemini-1.5-flash-8b | Lighter model | When hitting rate limits, faster responses |
| gemini-1.5-pro | Advanced model | Complex reasoning, detailed responses |

## Troubleshooting

### Rate Limit Errors

If you see an error about quota or rate limits:

1. Wait a minute before trying again
2. Try using a lighter model: `--model models/gemini-1.5-flash-8b`
3. Check your quota at [Google AI documentation](https://ai.google.dev/gemini-api/docs/rate-limits)

### Model Not Found Errors

If a model is not found or not supported for content generation:

1. Use `--list-models` to see available models
2. Stick to core models like `gemini-1.5-flash` or `gemini-1.5-pro`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

