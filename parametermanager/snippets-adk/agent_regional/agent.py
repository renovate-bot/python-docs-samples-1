#!/usr/bin/env python

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
"""
ADK agent for accessing parameters from regional Parameter Manager.
"""

import os

from google.adk import Agent
from google.adk.integrations.parameter_manager.parameter_client import ParameterManagerClient

# Fetch parameter from regional Parameter Manager
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_PROJECT_LOCATION")
parameter_id = os.environ.get("ADK_TEST_PARAMETER_ID")
parameter_version = os.environ.get("ADK_TEST_PARAMETER_VERSION", "latest")

if not project_id or not location or not parameter_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_PROJECT_LOCATION, and ADK_TEST_PARAMETER_ID environment variables must be set.")

resource_name = f"projects/{project_id}/locations/{location}/parameters/{parameter_id}/versions/{parameter_version}"

print(f"Fetching parameter from regional Parameter Manager ({location})...")
# Initialize Parameter Manager Client (Regional)
client = ParameterManagerClient(location=location)

# Fetch parameter
try:
    parameter_payload = client.get_parameter(resource_name)
    print("Successfully fetched parameter.")
except Exception as e:
    print(f"Error fetching parameter: {e}")
    raise e

# Initialize Agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

print("Agent initialized successfully.")
