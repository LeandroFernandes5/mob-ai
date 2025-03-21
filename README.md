# Generic AI Platform

This repository is an illustrative example of a generic AI platform for handling queries against various AI models (cloud-hosted or local). It demonstrates how to configure system prompts and model endpoints based on the incoming user interface identifier.

## Features

- **Flexible Configuration Manager**: Map any user interface ID to a specific system prompt and model.
- **Prompt Orchestration**: Combine system prompts, user input, and optional external data for best results.
- **Model Adapter**: Abstract calls to multiple AI models (OpenAI, local LLMs, etc.) behind a single interface.
- **Response Handling**: Simple post-processing logic to format and filter AI outputs.
- **External Integration**: Integration with OpenAI API to fetch external data based on user queries.

## Architecture

Refer to the design diagram in our documentation for more details. The system bootstrap stage provides metadata and deployment context, while the AI Platform orchestrates the query flow, model invocation, and integration with external systems.

## Getting Started

1. **Install Dependencies**:
   ```bash
   # Using pip
   pip install -e .
   
   # Or using uv
   uv pip install -e .
   ```

2. **Set Up OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Run the Server**:
   ```bash
   python run.py
   ```
   
   Alternatively:
   ```bash
   uvicorn src.main:app --reload
   ```

4. **Test the API**:
   - Visit http://127.0.0.1:8000/docs to see the Swagger UI
   - Or run the test script:
     ```bash
     python test_openai_integration.py
     ```

## OpenAI Integration

The platform now supports integration with OpenAI's API to fetch external data based on user queries. To use this feature:

1. Include a `question` key in the user context when making a request to the API.
2. The question will be sent to OpenAI, and the response will be included in the context for the AI model.

For more details, see the [OpenAI Integration Guide](docs/openai_integration.md).
