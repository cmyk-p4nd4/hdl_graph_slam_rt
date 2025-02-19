#!/usr/bin/python
# SPDX-License-Identifier: BSD-2-Clause
import tf
import rospy
from geometry_msgs.msg import TransformStamped


class Map2OdomPublisher:
	def __init__(self):
		self.broadcaster = tf.TransformBroadcaster()
		self.subscriber = rospy.Subscriber('/hdl_graph_slam/odom2pub', TransformStamped, self.callback)
		

	def callback(self, odom_msg:TransformStamped):
		self.odom_msg: TransformStamped = odom_msg

	def spin(self):
		if not hasattr(self, 'odom_msg'):
			self.broadcaster.sendTransform((0, 0, 0), (0, 0, 0, 1), rospy.Time.now(), 'odom', 'map')
			return

		pose = self.odom_msg.transform
		pos = (pose.translation.x, pose.translation.y, pose.translation.z)
		quat = (pose.rotation.x, pose.rotation.y, pose.rotation.z, pose.rotation.w)

		map_frame_id = self.odom_msg.header.frame_id
		odom_frame_id = self.odom_msg.child_frame_id

		self.broadcaster.sendTransform(pos, quat, rospy.Time.now(), odom_frame_id, map_frame_id)


def main():
	rospy.init_node('map2odom_publisher')
	freq = rospy.get_param("~publish_rate", 25.0)
	node = Map2OdomPublisher()

	rate = rospy.Rate(freq)
	while not rospy.is_shutdown():
		node.spin()
		try:
			rate.sleep()
		except rospy.exceptions.ROSInterruptException:
			pass

if __name__ == '__main__':
	main()
