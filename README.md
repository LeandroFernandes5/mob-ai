# Generic AI Platform

This repository is an illustrative example of a generic AI platform for handling queries against various AI models (cloud-hosted or local). It demonstrates how to configure system prompts and model endpoints based on the incoming user interface identifier.

## Features

- **Modular Interface Configuration**: Each interface has its own directory with dedicated configuration files.
- **Flexible Configuration Manager**: Map any user interface ID to a specific system prompt and model.
- **Prompt Orchestration**: Combine system prompts, user input, and optional external data for best results.
- **Model Adapter**: Abstract calls to multiple AI models (OpenAI, local LLMs, etc.) behind a single interface.
- **Response Handling**: Simple post-processing logic to format and filter AI outputs.
- **External Integration**: Integration with OpenAI API to fetch external data based on user queries.
- **Structured Logging**: JSON-formatted logs with correlation IDs for request tracking and analysis.
- **Robust Error Handling**: Comprehensive validation and specific error messages for different failure types.

## Architecture

Refer to the design diagram in our documentation for more details. The system bootstrap stage provides metadata and deployment context, while the AI Platform orchestrates the query flow, model invocation, and integration with external systems.

## Getting Started

1. **Install Dependencies**:
   ```bash
   uv sync
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

## Interface Configuration

The platform uses a directory-based configuration system where each interface has its own dedicated configuration:

1. **Directory Structure**:
   ```
   interfaces/
   ├── at_risk/
   │   └── config.yaml
   ├── your_interface/
   │   └── config.yaml
   ```

2. **Configuration Format**:
   Each interface's `config.yaml` should follow this structure:
   ```yaml
   model_providers:
     openai:
       model: gpt-3.5-turbo
       api_key: OPENAI_API_KEY
       system_prompt: |
         Your system prompt here
     local_model:
       model_type: ollama
       base_url: http://localhost:11434
       model: llama3
       system_prompt: "Your system prompt here"
   ```

3. **Using Interfaces**:
   When making API requests, specify the interface ID (which matches the directory name):
   ```json
   {
     "interface_id": "at_risk",
     "model_provider": "openai",
     "question": "Your question here"
   }
   ```

## OpenAI Integration

The platform supports integration with OpenAI's API for processing user queries. To use this feature:

1. Ensure your `config.yaml` has a properly configured `openai` section with model, API key, and system prompt.
2. When making API requests, include the `model_provider` set to "openai":
   ```json
   {
     "interface_id": "at_risk",
     "model_provider": "openai",
     "question": "Your question here"
   }
   ```
3. The platform will validate your configuration, make the API call, and return the response.

All requests and responses are logged with correlation IDs for easy tracking and analysis.

### SSL Verification Control

You can control SSL verification for OpenAI API requests using the `MOBAI_DISABLE_SSL_VERIFY` environment variable:

```bash
# To disable SSL verification (not recommended for production)
export MOBAI_DISABLE_SSL_VERIFY=true

# To enable SSL verification (default and recommended)
export MOBAI_DISABLE_SSL_VERIFY=false
```

**Note**: Disabling SSL verification should only be used in development or testing environments. It is not recommended for production use as it can expose your application to security risks.

For more details, see the [OpenAI Integration Guide](docs/openai_integration.md).

## Local Model Integration

The platform supports integration with locally-hosted models through services like Ollama:

1. **Install a Local Model Service**:
   For Ollama:
   - Install Ollama from [ollama.ai](https://ollama.ai)
   - Pull a model: `ollama pull llama3`

2. **Configure in Interface Config**:
   Add the following to your interface's `config.yaml`:
   ```yaml
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

## Streamlit GUI

The platform includes a Streamlit-based web interface for easy interaction with different use cases:

1. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```

2. **Run the GUI**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Using the Interface**:
   - Select a use case from the sidebar
   - Enter your question or input in the text area
   - Click "Submit" to send the request to the backend
   - View the response in the main area

The GUI automatically detects available interfaces from the `interfaces/` directory and provides a user-friendly way to interact with them.
