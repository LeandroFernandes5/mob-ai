# Generic AI Platform

This repository is an illustrative example of a generic AI platform for handling queries against various AI models (cloud-hosted or local). It demonstrates how to configure system prompts and model endpoints based on the incoming user interface identifier.

## Features

- **Flexible Configuration Manager**: Map any user interface ID to a specific system prompt and model.
- **Prompt Orchestration**: Combine system prompts, user input, and optional external data for best results.
- **Model Adapter**: Abstract calls to multiple AI models (OpenAI, local LLMs, etc.) behind a single interface.
- **Response Handling**: Simple post-processing logic to format and filter AI outputs.
- **External Integration**: Placeholder for retrieving or pushing data to external systems.

## Architecture

Refer to the design diagram in our documentation for more details. The system bootstrap stage provides metadata and deployment context, while the AI Platform orchestrates the query flow, model invocation, and integration with external systems.

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
2.	Run Locally: 
3.	uvicorn src.main:app --reload
4.	Test: 
o	Visit http://127.0.0.1:8000/docs to see the Swagger UI, or use a curl command to test the /v1/query endpoint.
