import sys
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QDialog, QVBoxLayout

from configuration_dialog import ConfigurationDialog
from constants import (
    DEFAULT_CAR_SPEED,
    DEFAULT_NPC_SPEED,
    DEFAULT_NPC_POSITION_X,
    DEFAULT_NPC_POSITION_Y,
    LOG_CODES,
    SCENARIO_TO_CONFIGURATION_MAP,
    DEFAULT_USER_VEHICLE_IMG,
    DEFAULT_NPC_VEHICLE_IMG,
    DEFAULT_CROSS_ROAD_IMG,
    DEFAULT_BANANA_IMG,
    DEFAULT_ROADBLOCK_IMG
)


class AnimatedCarWidget(QWidget):
    """
    Animated Car Widget for Autonomous Driving Simulation.
    It represents the main interactive component of the simulation.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_configuration()
        self.initialize_ui_elements()
        self.load_scenario_dependent_elements()
        self.init_ui()

    def load_configuration(self):
        """ Load configuration settings from the Configuration Dialog. """
        config_dialog = ConfigurationDialog()
        config_dialog.exec_()  # Blocks until the dialog is closed
        self.selected_scenario = config_dialog.selected_scenario

    def initialize_ui_elements(self):
        """ Initialize UI elements like buttons, labels, and pixmaps. """
        self.crossroad_pixmap = QtGui.QPixmap(DEFAULT_CROSS_ROAD_IMG)
        self.car_pixmap = QtGui.QPixmap(DEFAULT_USER_VEHICLE_IMG).scaledToWidth(50)
        self.speed = DEFAULT_CAR_SPEED
        self.npc_speed = DEFAULT_NPC_SPEED
        self.dec_button_pressed = False
        self.inc_button_pressed = False
        self.newSpeed = self.speed
        self.init_speed_label()
        self.init_control_buttons()

    def init_speed_label(self):
        """ Initialize the speed label displaying the car's speed. """
        self.speed_info = QLabel(f'{self.speed} km/h', self)
        self.speed_info.move(20, 5)
        self.speed_info.setStyleSheet("font-size: 25px;")

    def init_control_buttons(self):
        """ Initialize buttons to control the car's speed. """
        self.increase_button = self.create_button("+", QtCore.QRect(25, 50, 60, 60), self.increase_button_pressed)
        self.decrease_button = self.create_button("-", QtCore.QRect(25, 125, 60, 60), self.decrease_button_pressed)

    def create_button(self, text, geometry, callback):
        """ Create a QPushButton with specified text, geometry, and callback. """
        button = QPushButton(self)
        button.setText(text)
        button.setGeometry(geometry)
        button.setStyleSheet(
            "QPushButton {"
            "background-color: #e6e6e6;"
            "border-style: outset;"
            "border-width: 2px;"
            "font-size: 25px;"
            "border-radius: 15px;"
            "border-color: black;"
            "padding: 4px;}"
            "QPushButton:pressed {"
            "background-color: gray;}"
        )
        button.clicked.connect(callback)
        return button

    def decrease_button_pressed(self):
        self.dec_button_pressed = True

    def increase_button_pressed(self):
        self.inc_button_pressed = True

    def load_scenario_dependent_elements(self):
        # Load Avoidable Obstacle
        self.load_banana = SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["AvoidableObstacle"]
        if self.load_banana:
            self.banana_pixmap = QtGui.QPixmap(DEFAULT_BANANA_IMG).scaled(200, 50)
            self.banana_rect = QtCore.QRect(500, 530, 200, 50)

        # Load Unavoidable Obstacle
        self.load_stop = SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["UnavoidableObstacle"]
        if self.load_stop:
            self.stop_pixmap = QtGui.QPixmap(DEFAULT_ROADBLOCK_IMG).scaled(50, 50)
            self.stop_position = QtCore.QPoint(1100, 530)  # Stop image position

        # Load NPC
        self.load_npc_vehicle = (
            SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarOpposite"]
            or SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarCross"])
        if self.load_npc_vehicle:
            self.npc_vehicle_pixmap = QtGui.QPixmap(DEFAULT_NPC_VEHICLE_IMG).scaled(50, 50)

            if SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarOpposite"]:
                self.npc_vehicle_position = QtCore.QPoint(
                    DEFAULT_NPC_POSITION_X['OPPOSITE'],
                    DEFAULT_NPC_POSITION_Y['OPPOSITE']
                )
            elif SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarCross"]:
                self.npc_vehicle_position = QtCore.QPoint(
                    DEFAULT_NPC_POSITION_X['CROSS'],
                    DEFAULT_NPC_POSITION_Y['CROSS']
                )
                self.npc_vehicle_pixmap = self.rotate_pixmap(self.npc_vehicle_pixmap, -90)

        self.car_position = QtCore.QPoint(110, 530)
        self.middle_point = 835

        # Initial direction is right
        self.direction = 'right'

        # When car has reached the middle
        self.middle_point_reached = False

        self.turning_right = False

        # Record positions
        self.positions = []

    def init_ui(self):
        self.setMinimumSize(self.crossroad_pixmap.size())
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)  # Timer interval in milliseconds

    def rotate_pixmap(self, pixmap, degrees):
        transform = QtGui.QTransform().rotate(degrees)
        rotated_pixmap = pixmap.transformed(transform, mode=QtCore.Qt.SmoothTransformation)
        return rotated_pixmap

    def change_speed(self, speed_value):
        self.speed = speed_value
        return str(self.speed) + ' km/h'

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.crossroad_pixmap)
        if self.load_banana:
            banana_position = QtCore.QPoint(500, 530)  # Change to desired position
            painter.drawPixmap(banana_position, self.banana_pixmap)
        if self.load_stop:
            painter.drawPixmap(self.stop_position, self.stop_pixmap)
        if self.load_npc_vehicle:
            painter.drawPixmap(self.npc_vehicle_position, self.npc_vehicle_pixmap)
        painter.drawPixmap(self.car_position, self.car_pixmap)

    def animate(self):
        # Check if the car is over the banana 
        # .car_position.x() + car image width
        near_banana = self.load_banana and (
                self.banana_rect.left() <= (self.car_position.x() + 50) <= self.banana_rect.right()
        )
        passed_banana = self.load_banana and (
                self.car_position.x() >= self.banana_rect.right() 
        )

        if near_banana:
            # Disable speed change
            self.dec_button_pressed = False
            self.inc_button_pressed = False
            if self.speed > 10:
                self.change_speed(10)
                self.speed_info.setText(self.change_speed(10))
                print('1001' + ": " + LOG_CODES['1001'])  # record the console
        elif passed_banana:
            self.change_speed(self.newSpeed)
            self.speed_info.setText(self.change_speed(self.newSpeed))

        if self.dec_button_pressed:
            if near_banana == False or passed_banana == True:
                self.newSpeed = self.speed - 3
                if self.newSpeed > 0:
                    self.speed = self.newSpeed
                    self.speed_info.setText(self.change_speed(self.newSpeed))
                    self.dec_button_pressed = False

        if self.inc_button_pressed:
            if near_banana == False or passed_banana == True:
                self.newSpeed = self.speed + 3
                self.change_speed(self.newSpeed)
                self.speed_info.setText(self.change_speed(self.newSpeed))
                self.inc_button_pressed = False

        # Check if the car is near the stop sign
        if self.load_stop and self.car_position.x() >= self.stop_position.x() - 80:
            self.timer.stop()
            print('1002' + ": " + LOG_CODES['1002'])  # Reporting to the console
            self.destination_query()
            return  # Stop the animation

        if self.load_npc_vehicle:
            # NPC driving
            if self.load_npc_vehicle and SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarOpposite"]:
                self.npc_vehicle_position.setX(self.npc_vehicle_position.x() - self.npc_speed)
            elif self.load_npc_vehicle and SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarCross"]:
                self.npc_vehicle_position.setY(self.npc_vehicle_position.y() + self.npc_speed)
            # Check whether there will be a collision with NPC vehicle
            if SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["OtherCarCross"] and (
                    (
                            abs(self.car_position.x() - self.npc_vehicle_position.x())
                            < (self.speed + 50)
                    )
                    and abs(self.car_position.y() - self.npc_vehicle_position.y()) < (self.speed + 50)
            ):
                self.timer.stop()
                print('1003' + ": " + LOG_CODES['1003'])
                self.destination_query()
                return

        if not self.middle_point_reached and self.car_position.x() >= self.middle_point - 80:
            if SCENARIO_TO_CONFIGURATION_MAP[self.selected_scenario]["MakeATurn"]:
                self.turning_right = True
                self.middle_point_reached = True
            else:
                self.direction = 'right'
                self.middle_point_reached = True
            return

        if self.turning_right and self.car_position.x() < self.middle_point + 80:
            self.car_position.setX(self.car_position.x() + self.speed)
            if self.car_position.x() >= self.middle_point + 0:
                self.direction = 'down'
                self.turning_right = False
                self.car_pixmap = self.rotate_pixmap(self.car_pixmap, 90)

            self.update()
            return

        self.positions.append((self.car_position.x(), self.car_position.y()))

        if not self.middle_point_reached:
            self.car_position.setX(self.car_position.x() + self.speed)

            # When arrive at the middle point
            if self.car_position.x() > 835:
                self.middle_point_reached = True
        else:
            # when to middle point, move in the chosen direction
            if self.direction == 'right':
                self.car_position.setX(self.car_position.x() + self.speed)
            elif self.direction == 'down':
                self.car_position.setY(self.car_position.y() + self.speed)

            # When car is out of the window, stop the program
            if (self.direction == 'right' and self.car_position.x() > self.width()) or \
                    (self.direction == 'down' and self.car_position.y() > self.height()):
                self.timer.stop()
                self.destination_query()
        self.update()

    def destination_query(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle('Destination Reached')
        layout = QVBoxLayout()

        btn_restart = QPushButton('Restart', self.dialog)
        btn_restart.clicked.connect(self.destination_reached)
        layout.addWidget(btn_restart)

        btn_quit = QPushButton('Quit', self.dialog)
        btn_quit.clicked.connect(self.destination_reached)
        layout.addWidget(btn_quit)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def destination_reached(self):
        sender = self.sender()

        if sender.text() == 'Restart':
            self.dialog.close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            self.timer.stop()
            QApplication.instance().quit()
