# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def generate_content(output_uri: str) -> str:
    # [START googlegenaisdk_batchpredict_with_bq]
    import time

    from google import genai

    client = genai.Client()
    # TODO(developer): Update and un-comment below line
    # output_uri = f"bq://your-project.your_dataset.your_table"

    job = client.batches.create(
        model="gemini-1.5-pro-002",
        src="bq://storage-samples.generative_ai.batch_requests_for_multimodal_input",
        config={
            "dest": output_uri
        }
    )
    print(f"Job name: {job.name}")
    print(f"Job state: {job.state}")
    # Example response:
    # Job name: projects/%PROJECT_ID%/locations/us-central1/batchPredictionJobs/9876453210000000000
    # Job state: JOB_STATE_PENDING

    # See the documentation: https://googleapis.github.io/python-genai/genai.html#genai.types.BatchJob
    completed_states = [
        "JOB_STATE_SUCCEEDED",
        "JOB_STATE_FAILED",
        "JOB_STATE_CANCELLED",
        "JOB_STATE_PAUSED",
    ]
    while job.state not in completed_states:
        time.sleep(30)
        job = client.batches.get(name=job.name)
        print(f"Job state: {job.state}")
    # Example response:
    # Job state: JOB_STATE_PENDING
    # Job state: JOB_STATE_RUNNING
    # Job state: JOB_STATE_RUNNING
    # ...
    # Job state: JOB_STATE_SUCCEEDED

    # [END googlegenaisdk_batchpredict_with_bq]
    return job.state


if __name__ == "__main__":
    generate_content(
        output_uri="bq://your-project.your_dataset.your_table"
    )
