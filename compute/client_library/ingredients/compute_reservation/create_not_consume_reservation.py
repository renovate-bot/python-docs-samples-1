# Copyright 2024 Google LLC
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

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT create_compute_not_consume_reservation>


def create_vm_not_consume_reservation(
    project_id: str, zone: str, instance_name: str, machine_type: str = "n2-standard-2"
) -> compute_v1.Instance:
    """Creates a VM that explicitly doesn't consume reservations
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the VM will be created.
        instance_name (str): The name of the instance to create.
        machine_type (str, optional): The machine type for the instance.
    Returns:
        compute_v1.Instance: The created instance.
    """
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"
    instance.zone = zone

    instance.disks = [
        compute_v1.AttachedDisk(
            boot=True,  # Indicates that this is a boot disk
            auto_delete=True,  # The disk will be deleted when the instance is deleted
            initialize_params=compute_v1.AttachedDiskInitializeParams(
                source_image="projects/debian-cloud/global/images/family/debian-11",
                disk_size_gb=10,
            ),
        )
    ]

    instance.network_interfaces = [
        compute_v1.NetworkInterface(
            network="global/networks/default",  # The network to use
            access_configs=[
                compute_v1.AccessConfig(
                    name="External NAT",  # Name of the access configuration
                    type="ONE_TO_ONE_NAT",  # Type of access configuration
                )
            ],
        )
    ]

    # Set the reservation affinity to not consume any reservation
    instance.reservation_affinity = compute_v1.ReservationAffinity(
        consume_reservation_type="NO_RESERVATION",  # Prevents the instance from consuming reservations
    )

    # Create a request to insert the instance
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    vm_client = compute_v1.InstancesClient()
    operation = vm_client.insert(request)
    wait_for_extended_operation(operation, "Instance creation")

    print(f"Creating the {instance_name} instance in {zone}...")

    return vm_client.get(project=project_id, zone=zone, instance=instance_name)


# </INGREDIENT>
