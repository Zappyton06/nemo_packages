import rclpy
from rclpy.node import Node
import pygame
import time
#core libraries
class joystickCalibrator:
    def __init__(self, controller_id):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(controller_id)
        if not self.controller.get_init():
            self.controller.init()
        
        self.isSurgeCalibrated = False
        self.isYawCalibrated = False
        self.isSwayCalibrated = False
        self.isHeaveCalibrated = False
        #modify the value for more precise timing.
        self.calibrationDuration = 5

        self.surgeVals = [0, 0, 0]
        self.yawVals = [0, 0, 0]
        self.heaveVals = [0, 0, 0]
        self.swayVals = [0, 0, 0]
        #used for terminating the ROS2 Node once the operations are over
        self.CalibrationState = False

        print("CALIBRATION OBJECT INITIALIZED - CONFIGURATION YET TO START")

    def _calculate_average(self,axis_id,duration):  
        values= []
        start = time.time()
        while time.time() - start < duration:
            pygame.event.pump()
            values.append(self.controller.get_axis(axis_id))
            time.sleep(0.01)
        avg = sum(values)/len(values)
        return avg

    def runCalibrationFunction(self,axis_id):
        '''returns the calibrated average value of the function'''
        print(f"[CALIBRATION_NODE]: Starting Calibration for {axis_id}")
        start_input1 = input("press enter while in the centre : ")

        #for finding the average value for the stick in the central position
        if start_input1 == '':
            centre_avg = self._calculate_average(axis_id,self.calibrationDuration)
            print(f"Average value of minimum is {centre_avg} \n")
        start_input2 = input("press enter while in the forward/extreme pos : ")
        
        #for finding the average value for the stick in the maximum position
        if start_input2 == '':
            max_avg = self._calculate_average(axis_id,self.calibrationDuration)
            print(f"Averag value of Maximum is {max_avg} \n")

        start_input3 = input("press enter while in the reverse /other extreme : ")
        #for finding the average value for the stick in the minimum position
        if start_input3 == '':
            min_avg = self._calculate_average(axis_id,self.calibrationDuration)
            print(f"Averag value of Maximum is {min_avg} \n")

        return [min_avg, centre_avg, max_avg]
    
    def calibrateSurge(self):
        if not self.isSurgeCalibrated:
            self.surgeVals = self.runCalibrationFunction(1)
            self.isSurgeCalibrated = True

    def calibrateYaw(self):
        if not self.isYawCalibrated:
            self.yawVals = self.runCalibrationFunction(0)
            self.isYawCalibrated = True


    def calibrateSway(self):
        if not self.isSwayCalibrated:
            self.swayVals = self.runCalibrationFunction(3)
            self.isSwayCalibrated = True


    def calibrateHeave(self):
        if not self.isHeaveCalibrated:
            self.heaveVals = self.runCalibrationFunction(4)
            self.isHeaveCalibrated = True

    
    def runCalibrationCycle(self):
        self.calibrateSurge()
        self.calibrateYaw()
        self.calibrateHeave()
        self.calibrateSway()

        calibrationParamDict = {
            "Surge":self.surgeVals,
            "Yaw":self.yawVals,
            "heave":self.heaveVals,
            "Sway":self.swayVals
        }

        self.CalibrationState = True

        return calibrationParamDict
    
#ros2 Part
class JoystickCalibrationNode(Node):
    def __init__(self):
        super().__init__("JoystickCalibrationNode")
        self.get_logger().info("CALIBRATION STARTED")

        self.calibrator = joystickCalibrator(0)

        self.results = self.calibrator.runCalibrationCycle()
        print(self.results)

        self.get_logger().info("Calibration finished, shutting down node.")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = JoystickCalibrationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == '__main__':
    main()

        

