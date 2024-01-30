import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from turbojpeg import TurboJPEG, TJPF_GRAY, TJSAMP_GRAY, TJFLAG_PROGRESSIVE, TJFLAG_FASTUPSAMPLE, TJFLAG_FASTDCT
import cv2
import numpy as np

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('viewer')
        self.subscription = self.create_subscription(
            CompressedImage,
            '/image_compressed',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.jpeg = TurboJPEG()
        cv2.namedWindow("out",cv2.WINDOW_NORMAL)

    def listener_callback(self, msg:CompressedImage):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        
        # self.get_logger().info("image obtained")
        image = self.jpeg.decode(msg.data)
        image_mc=image[:640,:]
        image_orig=image[640:,:]
        # cv2.imshow("out",np.hstack((image_mc,image_orig)))
        cv2.imshow("out",image_mc)
        cv2.waitKey(1)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()