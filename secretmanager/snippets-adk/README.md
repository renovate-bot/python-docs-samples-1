# ADK Secret Manager Samples

This directory contains samples demonstrating how to use the Agent Development Kit (ADK) with Google Cloud Secret Manager.

## Folders
*   `agent_global`: Sample for accessing secrets from a global Secret Manager instance.
*   `agent_regional`: Sample for accessing secrets from a regional Secret Manager endpoint.

## Prerequisites

1.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Set up Application Default Credentials**:
    ```bash
    gcloud auth application-default login
    ```

3.  **Install dependencies**:
    You need to install dependencies for the specific sample or test you want to run.
    
    For global agent samples and tests:
    ```bash
    pip install -r agent_global/requirements.txt
    ```

    For regional agent samples and tests:
    ```bash
    pip install -r agent_regional/requirements.txt
    ```

4.  **Set up environment variables**:
    *   `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID. (Required for both samples and tests).
    
    The following environment variables are **only required when running the samples manually**. The tests will generate and use their own temporary secrets automatically.
    
    *   `ADK_TEST_SECRET_ID`: The ID of the secret to access.
    *   `ADK_TEST_SECRET_VERSION` (Optional): The version of the secret (defaults to `latest`).
    *   `GOOGLE_CLOUD_PROJECT_LOCATION` (Required for regional samples): The region where the secret is located (e.g., `us-central1`).

## Running the Samples

The samples are designed to be run from this directory (`snippets-adk`) using the `adk run` command.

### Global Secret Manager Agent

1.  **Create a `.env` file** alongside `agent_global.py` in the `agent_global` directory:
    ```env
    GOOGLE_GENAI_USE_VERTEXAI=1
    GOOGLE_CLOUD_PROJECT=your-project-id
    GOOGLE_CLOUD_LOCATION=your-region
    ```
    *Note: Replace `your-project-id` with your GCP project ID and `your-region` with your desired region.*

2.  **Run the agent**:
    ```bash
    export GOOGLE_CLOUD_PROJECT="your-project-id"
    export ADK_TEST_SECRET_ID="your-secret-id"
    adk run agent_global
    ```

### Regional Secret Manager Agent

1.  **Create a `.env` file** alongside `agent_regional.py` in the `agent_regional` directory:
    ```env
    GOOGLE_GENAI_USE_VERTEXAI=1
    GOOGLE_CLOUD_PROJECT=your-project-id
    GOOGLE_CLOUD_LOCATION=your-region
    ```
    *Note: Replace `your-project-id` with your GCP project ID and `your-region` with your desired region.*

2.  **Run the agent**:
    ```bash
    export GOOGLE_CLOUD_PROJECT="your-project-id"
    export GOOGLE_CLOUD_PROJECT_LOCATION="your-region"
    export ADK_TEST_SECRET_ID="your-secret-id"
    adk run agent_regional
    ```

## Running the Tests

The tests are located within the specific agent folders and run the samples using `adk run`.

To run tests for the global agent:
```bash
pip install -r agent_global/requirements.txt
pip install -r agent_global/requirements-test.txt
pytest agent_global/snippets_adk_test.py
```

To run tests for the regional agent:
```bash
pip install -r agent_regional/requirements.txt
pip install -r agent_regional/requirements-test.txt
pytest agent_regional/snippets_adk_test.py
```
