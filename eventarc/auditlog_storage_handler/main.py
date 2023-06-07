# Copyright 2023 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START eventarc_audit_storage_http_server]
import os

from flask import Flask, request
from cloudevents.http import from_http
from google.protobuf import json_format
from google.events.cloud.storage import StorageObjectData
from google.events.cloud.audit import AuditLog, LogEntryData

app = Flask(__name__)
# [END eventarc_audit_storage_http_server]


# [START eventarc_audit_storage_http_handler]
@app.route("/", methods=["POST"])
def index():
    event = from_http(request.headers, request.get_data())

    log_entry = LogEntryData(event.data)
    auditlog = log_entry.proto_payload

    if auditlog.service_name != "storage.googleapis.com":
        return("non-storage audit log found.", 400)

    user = auditlog.authentication_info.principal_email
    return (
        f"Cloud Storage object changed: {auditlog.resource_name} updated by {user}",
        200,
    )


# [START eventarc_audit_storage_http_handler]


# [START eventarc_audit_storage_server]
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END eventarc_audit_storage_server]