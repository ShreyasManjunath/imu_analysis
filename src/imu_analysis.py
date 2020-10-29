#!/usr/bin/env python

import rospy
import rosbag
import yaml, csv
from time import sleep
import numpy as np
import matplotlib.pyplot as plt



bag_name = "/home/nvidia/storage/imu_data_for_analysis_35mins.bag"
rostopic_name = "/dji_osdk_ros/imu"
file_to_be_opened = "/home/nvidia/catkin_ws/src/imu_analysis/csv/Imu_data.csv"	

def analyse_imu():
	bag = rosbag.Bag(bag_name)
	bag_info = yaml.load(bag._get_yaml_info())
	csvfile = open(file_to_be_opened, 'wb')
	writer = csv.writer(csvfile, delimiter=',')

	for msg in bag.read_messages(rostopic_name):
		current_time_stamp = rospy.Time.now()
		print(msg.message)
		gyroscope_data = msg.message.angular_velocity
		accelerometer_data = msg.message.linear_acceleration
		#orientation = msg.message.orientation		
		row = [current_time_stamp, gyroscope_data.x,gyroscope_data.y,gyroscope_data.z,accelerometer_data.x,accelerometer_data.y,accelerometer_data.z]
		
			
		writer.writerow(row)

	print("Done writing into csv")



def plot_data(file):
	t = []
	gyro_x = []
	gyro_y = []
	gyro_z = []

	with open(file,'r') as csvfile:
	    plots = csv.reader(csvfile, delimiter=',')
	    for row in plots:
		t.append(float(row[0]))
		gyro_x.append(float(row[1]))
		gyro_y.append(float(row[2]))
		gyro_z.append(float(row[3]))
	
	plt.figure(1)
	plt.plot(t,gyro_x, label='gyro_x', color='b',marker="x")
	plt.xlabel('t')
	plt.ylabel('gyro_x')
	plt.title('IMU_Gyro_x')
	plt.legend()

	plt.figure(2)
	plt.plot(t,gyro_y, label='gyro_y', color='g',marker='o')
	plt.xlabel('t')
	plt.ylabel('gyro_y')
	plt.title('IMU_Gyro_y')
	plt.legend()

	plt.figure(3)
	plt.plot(t,gyro_z, label='gyro_z', color='r',marker='v')
	plt.xlabel('t')
	plt.ylabel('gyro_z')
	plt.title('IMU_Gyro_z')
	plt.legend()
	plt.show()

def compute_intrinsic():

# add your code here
	pass

	
	

if __name__=='__main__':
	rospy.init_node("imu_analysis_node")
	analyse_imu()
	#plot_data("Imu_data.csv")
	rospy.spin()
	
