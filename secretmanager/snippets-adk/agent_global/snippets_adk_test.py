# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import os
import subprocess
import time
from typing import Iterator
import uuid

from google.api_core import exceptions
from google.cloud import secretmanager
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)


@pytest.fixture()
def client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def secret_id(
    client: secretmanager.SecretManagerServiceClient, project_id: str
) -> Iterator[str]:
    secret_id = f"python-adk-test-{uuid.uuid4()}"
    yield secret_id

    # Teardown: delete the secret
    secret_path = client.secret_path(project_id, secret_id)
    print(f"Deleting secret {secret_id}...")
    try:
        # Wait a bit to avoid conflicts if operations are still pending
        time.sleep(2)
        client.delete_secret(request={"name": secret_path})
    except exceptions.NotFound:
        pass


def test_agent_global(
    client: secretmanager.SecretManagerServiceClient, project_id: str, secret_id: str
) -> None:
    # Create the secret
    parent = f"projects/{project_id}"
    print(f"Creating secret {secret_id}...")
    client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    # Add a version
    secret_path = client.secret_path(project_id, secret_id)
    print(f"Adding version to {secret_id}...")
    client.add_secret_version(
        request={
            "parent": secret_path,
            "payload": {"data": b"test-payload"},
        }
    )

    # Set environment variables required by the agent
    # GOOGLE_CLOUD_PROJECT is already set in the environment (required to run this test)
    os.environ["ADK_TEST_SECRET_ID"] = secret_id
    os.environ["ADK_TEST_SECRET_VERSION"] = "latest"

    print(f"Running adk run agent_global from {PARENT_DIR}...")
    # Run the sample using adk run
    result = subprocess.run(
        ["adk", "run", "agent_global"],
        input="exit\n",
        capture_output=True,
        text=True,
        cwd=PARENT_DIR,
    )

    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    assert result.returncode == 0
    assert "Successfully fetched secret" in result.stdout
    assert "Agent initialized successfully" in result.stdout
