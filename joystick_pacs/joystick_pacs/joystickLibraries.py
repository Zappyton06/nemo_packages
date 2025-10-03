import rclpy
from rclpy.node import Node
import pygame

#joystick input reader
class joystickReadWrapper:
    def __init__(self,controller_id):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(controller_id)
        if not self.controller.get_init():
            self.controller.init()

        self.pause_read = False

    def readAxis(self,axis_id):
        rawAxisval = None
        try:
            pygame.event.pump()
            rawAxisval = self.controller.get_axis(axis_id)
            return rawAxisval
        except self.pause_read:
            pass

    def buttonStatusReader(self,button_id):
        #pause development for a while
        pass     