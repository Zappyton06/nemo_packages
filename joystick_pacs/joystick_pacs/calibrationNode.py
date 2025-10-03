import rclpy
from rclpy.node import Node
from joystickCalibratorlib import joystickCalibrator


class JoystickCalibrationNode(Node):
    def __init__(self):
        super().__init__("JoystickCalibrationNode")
        self.get_logger().info("CALIBRATION STARTED")

        self.calibrator = joystickCalibrator(0)

        self.results = self.calibrator.runCalibrationCycle()
        print(self.results)

        self.get_logger().info("Calibration finished, shutting down node.")
        rclpy.shutdown()