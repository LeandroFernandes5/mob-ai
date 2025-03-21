# OpenAI Integration Guide

This document explains how to use the OpenAI integration in the Mobai Platform.

## Overview

The Mobai Platform now supports integration with OpenAI's API to fetch external data based on user queries. This allows the platform to enhance responses with information retrieved from OpenAI.

## Setup

### 1. Install Dependencies

Make sure you have the required dependencies installed:

```bash
# Using pip
pip install openai requests

# Or using uv
uv pip install openai requests
```

### 2. Set Up OpenAI API Key

You need an OpenAI API key to use this integration. You can get one from the [OpenAI website](https://platform.openai.com/api-keys).

Set the API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Alternatively, you can modify the `external_integration.py` file to use a different method of storing and retrieving the API key, such as a configuration file or a secure vault.

## Usage

### Including a Question in User Context

To use the OpenAI integration, include a `question` key in the user context when making a request to the API:

```python
payload = {
    "interface_id": "cs_support",
    "user_input": "Tell me about cloud computing services.",
    "user_context": {
        "user_id": "user123",
        "question": "What are the main types of cloud computing services and their differences?"
    }
}
```

The `question` will be sent to OpenAI, and the response will be included in the context for the AI model.

### How It Works

1. When a request is received with a `question` in the user context, the system calls the `fetch_external_data` function.
2. The function makes an API call to OpenAI with the question.
3. The response from OpenAI is added to the user context as `external_data`.
4. The prompt orchestrator includes this external data in the prompt for the AI model.

## Testing

You can test the OpenAI integration using the provided test script:

```bash
python test_openai_integration.py
```

This script sends a request to the API with a question about cloud computing services and prints the response.

## Customization

### Modifying the OpenAI Request

You can customize the OpenAI request by modifying the `fetch_external_data` function in `external_integration.py`. For example, you can change the model, adjust the maximum number of tokens, or modify the system prompt.

### Error Handling

The integration includes basic error handling. If the OpenAI API call fails, the function returns an error message that is included in the response.

## Limitations

- The integration currently uses a fixed model (`gpt-3.5-turbo`). You may want to make this configurable.
- The maximum number of tokens is set to 150, which may be too low for some use cases.
- The system prompt is hardcoded. You may want to make it configurable or specific to each interface.
