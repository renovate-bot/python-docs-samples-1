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
# limitations under the License.

import os
import subprocess
import time
from typing import Iterator
import uuid

from google.api_core import exceptions
from google.cloud import parametermanager_v1
import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)


@pytest.fixture()
def location() -> str:
    return "us-central1"


@pytest.fixture()
def client(location: str) -> parametermanager_v1.ParameterManagerClient:
    api_endpoint = f"parametermanager.{location}.rep.googleapis.com"
    return parametermanager_v1.ParameterManagerClient(
        client_options={"api_endpoint": api_endpoint}
    )


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def parameter_id(
    client: parametermanager_v1.ParameterManagerClient, project_id: str, location: str
) -> Iterator[str]:
    parameter_id = f"python-adk-test-{uuid.uuid4()}"
    yield parameter_id

    # Teardown: delete the version then the parameter
    version_path = f"projects/{project_id}/locations/{location}/parameters/{parameter_id}/versions/1"
    parameter_path = f"projects/{project_id}/locations/{location}/parameters/{parameter_id}"

    print("Deleting parameter version 1...")
    try:
        time.sleep(1)
        client.delete_parameter_version(request={"name": version_path})
    except exceptions.NotFound:
        pass

    print(f"Deleting parameter {parameter_id}...")
    try:
        time.sleep(2)
        client.delete_parameter(name=parameter_path)
    except exceptions.NotFound:
        pass


def test_agent_regional(
    client: parametermanager_v1.ParameterManagerClient,
    project_id: str,
    location: str,
    parameter_id: str,
) -> None:
    # Create the parameter
    parent = f"projects/{project_id}/locations/{location}"
    print(f"Creating regional parameter {parameter_id} in {location}...")
    client.create_parameter(
        request={
            "parent": parent,
            "parameter_id": parameter_id,
        }
    )

    # Add a version
    parameter_path = f"projects/{project_id}/locations/{location}/parameters/{parameter_id}"
    print(f"Adding version to {parameter_id}...")
    client.create_parameter_version(
        request={
            "parent": parameter_path,
            "parameter_version_id": "1",
            "parameter_version": {
                "payload": {"data": b"test-payload"}
            },
        }
    )

    # Set environment variables required by the agent
    os.environ["ADK_TEST_PARAMETER_ID"] = parameter_id
    os.environ["ADK_TEST_PARAMETER_VERSION"] = "1"
    os.environ["GOOGLE_CLOUD_PROJECT_LOCATION"] = location

    print(f"Running adk run agent_regional from {PARENT_DIR}...")
    # Run the sample using adk run
    result = subprocess.run(
        ["adk", "run", "agent_regional"],
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
    assert "Successfully fetched parameter" in result.stdout
    assert "Agent initialized successfully" in result.stdout
