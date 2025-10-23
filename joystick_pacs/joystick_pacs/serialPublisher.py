import rclpy
from rclpy.node import Node
from nemo_interfaces.msg import RovCommands
import serial
import time

START_BIT = 0xAA
STOP_BIT = 0x55

class ThrusterSerialNode(Node):
    def __init__(self):
        super().__init__('thruster_serial_node')

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
            time.sleep(2)
            self.get_logger().info("✅ Serial port /dev/ttyUSB0 connected.")
        except serial.SerialException as e:
            self.get_logger().error(f"❌ Serial open failed: {e}")
            self.ser = None

        self.subscription = self.create_subscription(
            RovCommands,
            '/input_cmd',
            self.cmd_callback,
            10
        )

    def cmd_callback(self, msg):
        if not self.ser or not self.ser.is_open:
            self.get_logger().warn("Serial not available.")
            return

        # Convert float command to 0-255 integer (example scaling)
        surge_val = int(msg.surge * 100) & 0xFF
        heave_val = int(msg.heave * 100) & 0xFF

        # C-style struct as bytearray
        packet = bytearray(4)
        packet[0] = START_BIT
        packet[1] = surge_val
        packet[2] = heave_val
        packet[3] = STOP_BIT

        print(f"The Published Packet is: {packet.hex(' ')}")

        try:
            self.ser.write(packet)
            self.get_logger().info(f"➡️ Sent packet: {list(packet)}")
        except Exception as e:
            self.get_logger().error(f"❌ Serial write failed: {e}")

    def destroy_node(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.get_logger().info("🔌 Serial port closed.")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ThrusterSerialNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
