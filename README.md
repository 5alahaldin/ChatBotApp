## Preview

![Preview](./preview.png)
**Lyla** is a smart Arabic-speaking chatbot. Just type your message, and it will respond in **Modern Standard Arabic** with natural, intelligent replies.

## Features

* Beautiful Arabic UI using PyQt5
* Typing animation for responses
* Remembers previous chat context
* Powered by Ollama + LangChain
* Arabic-only intelligent assistant
* Press `Enter` to send messages

## How It Works

Lyla uses an **Ollama** language model through **LangChain**. It is configured to:

* Only understand and respond in **Arabic**
* Use both the current question and previous messages to generate accurate answers

The default model used is: `prakasharyan/qwen-arabic`
**You can also specify a different model** when running the app.


## How to Run

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Run the app** (with optional model name):

```bash
python app.py [model-name]
```

### Examples:

```bash
python app.py                        # Uses default model: prakasharyan/qwen-arabic
python app.py llama3                # Uses LLaMA 3
python app.py arabic-llm            # Uses your custom Arabic model
```