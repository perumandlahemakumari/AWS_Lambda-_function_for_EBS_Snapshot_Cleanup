import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all EBS snapshots owned by this account
    try:
        snapshots_response = ec2.describe_snapshots(OwnerIds=['self'])
    except ClientError as e:
        print(f"Failed to retrieve snapshots: {e}")
        return

    # Get all active EC2 instance IDs
    try:
        instances_response = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
    except ClientError as e:
        print(f"Failed to retrieve running instances: {e}")
        return

    active_instance_ids = {
        instance['InstanceId']
        for reservation in instances_response['Reservations']
        for instance in reservation['Instances']
    }

    # Iterate through each snapshot
    for snapshot in snapshots_response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            # Snapshot not linked to any volume
            try:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} (no volume attached).")
            except ClientError as e:
                print(f"Error deleting snapshot {snapshot_id}: {e}")
            continue

        # Check if the volume exists and is attached to a running instance
        try:
            volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
            volume = volume_response['Volumes'][0]
            attachments = volume.get('Attachments', [])

            # Delete snapshot if volume is not attached to any running instance
            if not attachments:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} (volume not attached).")
            else:
                instance_id = attachments[0].get('InstanceId')
                if instance_id not in active_instance_ids:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} (attached to stopped instance).")

        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted EBS snapshot {snapshot_id} (volume not found).")
            else:
                print(f"Error checking volume {volume_id}: {e}")
