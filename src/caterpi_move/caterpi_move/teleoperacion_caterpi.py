#!/usr/bin/env python3
# ROS2 Libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import sys, select, os


print("""
Controla al Robot Caterpillar
---------------------------
Comandos :
        F
   L    S    R
        B

Oprime F (Front) si quieres ir hacia delante 
Oprime B (Back) si quieres ir hacia atras 
Oprime R (Right) si quieres rotar hacia la izquierda 
Oprime L (Left) si quieres rotar hacia la derecha

PARO DE EMERGENCIA : S (Stop) si quieres detener todo

CTRL-C para cerrar la teleoperación
""")

if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

class ValueMotorPublisher(Node):
    def __init__(self):
        super().__init__('value_publisher_node')
        self.value_publisher = self.create_publisher(String, '/serial_port/value', 10)
        self.value_timer = self.create_timer(0.1, self.publish_value)

        # Lista de comandos válidos
        self.valid_commands = ['F', 'B', 'R', 'L', 'S']

        self.value_msg = String()

        # Información del puerto serial
        self.microcontroller_port = "/dev/ttyACM0"
        self.microcontroller_baudrate = 9600
        self.serial_port = serial.Serial(self.microcontroller_port, self.microcontroller_baudrate, timeout=10)

    def write_to_serial_port(self, value_msg):
        self.value_msg = value_msg
        data_out = str(self.value_msg.data)  # Guardar datos del mensaje ROS2 en una variable (práctica común)
        self.serial_port.write(bytes(data_out, 'utf-8'))  # Escribir datos del mensaje ROS2 en el microcontrolador
        print(f"{data_out}")

    def publish_value(self):
        key = get_key()
        if key and key.upper() in self.valid_commands:
            # Publicar la tecla presionada en mayúscula
            self.value_msg.data = key.upper()
            self.value_publisher.publish(self.value_msg)
            self.write_to_serial_port(self.value_msg)

def get_key():
    if os.name == 'nt':
        return msvcrt.getch().decode()
    else:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
        return key

def main(args=None):
    rclpy.init(args=args)
    value_publisher_node = ValueMotorPublisher()
    try:
        rclpy.spin(value_publisher_node)
    except KeyboardInterrupt:
        print("\nCerrando el nodo...")
        value_publisher_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
