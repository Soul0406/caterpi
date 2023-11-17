import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import serial
import time  # Agrega la importación de time

class GreenDetector(Node):
    def __init__(self):
        super().__init__('detector_verde')

        # Create the subscriber
        self.subscription = self.create_subscription(Image, 'video_frames', self.listener_callback, 10)

        # Initialize CvBridge
        self.br = CvBridge()

        # Set initial values for the green color range
        self.green_lower = np.array([40, 40, 40], np.uint8)
        self.green_upper = np.array([80, 255, 255], np.uint8)

        # Open a serial connection (replace 'COMx' with your actual port)
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        
    def listener_callback(self, data):
        self.get_logger().info('Detectando color verde del Video-Frame')

        # Convert ROS Image message to OpenCV image
        current_frame = self.br.imgmsg_to_cv2(data)

        self.serial_port.write(b'T')

        time.sleep(10)

        """ # Apply green color filter
        hsvFrame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)
        # Normalize histogram for better adaptation to varying lighting conditions
        hsvFrame = self.normalize_histogram(hsvFrame)
        green_mask = cv2.inRange(hsvFrame, self.green_lower, self.green_upper)

        kernal = np.ones((5, 5), "uint8")
        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(current_frame, current_frame, mask=green_mask)

        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 1000:  # Ajusta el área mínima según sea necesario
                x, y, w, h = cv2.boundingRect(contour)
                current_frame = cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(current_frame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

        # Después de encontrar los contornos, calcula la suma total del área de los contornos
        total_area_contornos = sum(cv2.contourArea(contour) for contour in contours)

        # Define un umbral para la detección
        umbral_deteccion = 1000  # Ajusta este valor según sea necesario

        # Establece deteccion como True si la suma total del área es mayor que el umbral
        deteccion = total_area_contornos > umbral_deteccion

        # Imprimir el valor booleano en la terminal
        self.get_logger().info(f'Detección de color verde: {deteccion}')

        # Enviar "T" si hay detección, "N" si no hay detección por el puerto serial
        if deteccion:
            try:
                self.serial_port.write(b'T')
                self.serial_port.flush()  # Asegura que todos los datos se envíen
                time.sleep(0.1)  # Pequeño retardo
            except Exception as e:
                self.get_logger().error(f'Error al escribir en el puerto serie: {e}')
        else:
            try:
                self.serial_port.write(b'N')
                self.serial_port.flush()  # Asegura que todos los datos se envíen
                time.sleep(0.1)  # Pequeño retardo
            except Exception as e:
                self.get_logger().error(f'Error al escribir en el puerto serie: {e}')

        #cv2.imshow("Camara de deteccion", current_frame)
        cv2.waitKey(1) """

    def normalize_histogram(self, image):
        # Normalize the histogram of the image
        img_hist = cv2.equalizeHist(image[:, :, 2])
        image[:, :, 2] = img_hist
        return image

def main(args=None):
    rclpy.init(args=args)
    detector_verde = GreenDetector()
    rclpy.spin(detector_verde)
    detector_verde.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
