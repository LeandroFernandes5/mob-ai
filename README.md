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
     python -m tests.test_model_integration
     ```

## OpenAI Integration

The platform now supports integration with OpenAI's API to fetch external data based on user queries. To use this feature:

1. Include a `question` key in the user context when making a request to the API.
2. The question will be sent to OpenAI, and the response will be included in the context for the AI model.

For more details, see the [OpenAI Integration Guide](docs/openai_integration.md).

## Local Model Integration

The platform supports integration with locally-hosted models through services like Ollama:

1. **Install a Local Model Service**:
   For Ollama:
   - Install Ollama from [ollama.ai](https://ollama.ai)
   - Pull a model: `ollama pull llama3`

2. **Configure in config.yaml**:
   ```yaml
   interfaces:
     your_interface:
       model_providers:
         local_model:
           model_type: ollama  # Type of local model service
           base_url: http://localhost:11434  # URL where Ollama is running
           model: llama3  # Name of the model in your local service
           system_prompt: "Your system prompt here"
   ```

3. **Use in API Requests**:
   When making a request, specify `model_provider: "local_model"`:
   ```json
   {
     "interface_id": "your_interface",
     "model_provider": "local_model",
     "question": "Your question here"
   }
   ```

This integration allows you to keep all AI interactions within your local environment without sending data to third-party cloud services.
