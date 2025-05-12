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
    "model_provider": "openai",
    "question": "What are the main types of cloud computing services?"
}
```

The `question` will be sent to OpenAI, and the response will be returned.

### How It Works

1. When a request is received, the system calls the `fetch_external_data` function in `external_integration.py`.
2. The function validates the configuration for the specified interface and model provider.
3. The function makes an API call to OpenAI with the system prompt from the configuration and the user's question.
4. The response from OpenAI is returned and logged.

## Configuration

Each interface must have a configuration file at `interfaces/<interface_id>/config.yaml` with the following structure:

```yaml
description: "Interface description"
model_providers:
  openai:
    model: gpt-4.1-2025-04-14  # Specify the model to use
    api_key: OPENAI_API_KEY     # Environment variable containing the API key
    system_prompt: |
      Your system prompt here
```

The system will validate the configuration and provide specific error messages if any required fields are missing.

## Logging

The integration uses structured logging in JSON format with the following information:

- `correlation_id`: Unique identifier for tracing request-response pairs
- `event`: Type of event (api_request, api_response)
- `model_provider`: The provider being used (openai, local_model)
- `interface_id`: The interface being used
- `model`: The specific model being used
- `question`: The user's question (for requests)
- `response`: The model's response (for responses)

These logs can be parsed and analyzed to track usage and performance.

## Error Handling

The integration includes comprehensive error handling with specific error messages for different types of failures:

- Configuration validation errors
- API key errors
- Connection errors
- Import errors for model clients
- Response content errors

Error messages are clearly formatted and include suggestions for fixes when possible.

## Testing

You can test the OpenAI integration using the provided test script:

```bash
python test_openai_integration.py
```

This script sends a request to the API with a question about cloud computing services and prints the response.

## Customization

### Modifying the OpenAI Request

You can customize the OpenAI request by modifying the `fetch_external_data` function in `external_integration.py`. For example, you can change the model, adjust parameters, or add custom headers.

## Limitations

- The integration currently uses a fixed model (`gpt-3.5-turbo`). You may want to make this configurable.
- The maximum number of tokens is set to 150, which may be too low for some use cases.
- The system prompt is hardcoded. You may want to make it configurable or specific to each interface.
