import os

import pytest


@pytest.fixture
def project_id() -> str:
    """Get the Google Cloud project ID from the environment."""
    project_id = os.environ.get("BUILD_SPECIFIC_GCLOUD_PROJECT")
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    return project_id
