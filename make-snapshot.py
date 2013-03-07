import boto
import urllib2

ec2 = boto.connect_ec2()

#Get instance ID from GET http://169.254.169.254/latest/meta-data/instance-id using urllib2
get_volume_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = get_volume_id.read()
print instance_id
get_volume_id.close()

#Get the reservation for this instance
instance_reservation = ec2.get_all_instances(instance_ids=[instance_id])[0]
print instance_reservation

#Get the instance from the list of instances in the reservation
instance = instance_reservation.instances[0]
print instance

#The root device is probably /dev/sda1
instance_root_device = instance.root_device_name
print instance_root_device

#Get the EBS Volume id for the root device name
instance_volume_id = instance.block_device_mapping[instance_root_device].volume_id
print instance_volume_id

my_volume = ec2.get_all_volumes(volume_ids=[instance_volume_id])[0]
print my_volume

latest_snapshot = my_volume.create_snapshot('ERIN-RAWR')

print 'Just created the following snapshot:'

print(my_volume.snapshots()[0].start_time)

print(my_volume.snapshots()[0].id + '\n')
