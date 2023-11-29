import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMessageBox,
    QPushButton,
    QLabel,
    QDialog,
    QVBoxLayout
)
import seaborn as sns
import matplotlib.pyplot as plt

from constants import (
    DEFAULT_USER_VEHICLE_IMG,
    DEFAULT_NPC_VEHICLE_IMG,
    DEFAULT_CROSS_ROAD_IMG,
    DEFAULT_BANANA_IMG,
    DEFAULT_ROADBLOCK_IMG
)
from ConfigurationDialog import ConfigurationDialog


class AnimatedCarWidget(QWidget):
    EXIT_CODE_REBOOT = -123  # for restarting application

    DEFAULT_NPC_SPEED = 20
    DEFAULT_NPC_POSITION_X = {
        'OPPOSITE': 1600,
        'CROSS': 845
    }
    DEFAULT_NPC_POSITION_Y = {
        'OPPOSITE': 475,
        'CROSS': 0
    }
    NPC_DIRECTION = {
        'OPPOSITE': 'opposite',
        'CROSS': 'cross'
    }
    # Log
    LOG_CODES = {
        '1001': "Avoidable obstacle detected, reduce speed",
        '1002': "Unavoidable obstacle detected, emergency stop",
        '1003': "Potential collision detected, emergency stop"
    }

    def __init__(self, parent=None):
        super(AnimatedCarWidget, self).__init__(parent)
        self.selected_scenario = "Scenario 1"
        self.crossroad_pixmap = QtGui.QPixmap(DEFAULT_CROSS_ROAD_IMG)
        self.car_pixmap = QtGui.QPixmap(DEFAULT_USER_VEHICLE_IMG).scaledToWidth(50)
        self.speed = 25  # default speed
        self.npc_speed = self.DEFAULT_NPC_SPEED  # default speed
        self.dec_button_pressed = False
        self.inc_button_pressed = False

        # set speed label
        self.speedInfo = QLabel(str(self.speed) + ' km/h', self)
        self.speedInfo.move(20, 5)
        self.speedInfo.setStyleSheet("font-size: 25px;")

        # button to increase speed
        self.increase_button = QPushButton(self)
        self.increase_button.setText("+")
        self.increase_button.setGeometry(QtCore.QRect(25, 50, 60, 60))
        self.increase_button.setStyleSheet("QPushButton {"
                                           "background-color: #e6e6e6;"
                                           "border-style: outset;"
                                           "border-width: 2px;"
                                           "font-size: 25px;"
                                           "border-radius: 15px;"
                                           "border-color: black;"
                                           "padding: 4px;}"
                                           "QPushButton:pressed {"
                                           "background-color: gray;}")
        self.increase_button.clicked.connect(self.increase_button_pressed)

        # button to decrease speed
        self.decrease_button = QPushButton(self)
        self.decrease_button.setText("-")
        self.decrease_button.setGeometry(QtCore.QRect(25, 125, 60, 60))
        self.decrease_button.setStyleSheet("QPushButton {"
                                           "background-color: #e6e6e6;"
                                           "border-style: outset;"
                                           "font-size: 25px;"
                                           "border-width: 2px;"
                                           "border-radius: 15px;"
                                           "border-color: black;"
                                           "padding: 4px;}"
                                           "QPushButton:pressed {"
                                           "background-color: gray;}")
        self.decrease_button.clicked.connect(self.decrease_button_pressed)

        self.load_banana = self.ask_to_load_image('Add Road Slip?')
        if self.load_banana:
            self.banana_pixmap = QtGui.QPixmap(DEFAULT_BANANA_IMG).scaled(200, 50)
            self.banana_rect = QtCore.QRect(500, 530, 200, 50)

        self.load_stop = self.ask_to_load_image('Add Roadblocks?')
        if self.load_stop:
            self.stop_pixmap = QtGui.QPixmap(DEFAULT_ROADBLOCK_IMG).scaled(50, 50)
            self.stop_position = QtCore.QPoint(1100, 530)  # Stop image position

        # Load NPC
        self.load_npc_vehicle = self.ask_to_load_image('Add NPC Vehicle?')
        if self.load_npc_vehicle:
            self.npc_vehicle_pixmap = QtGui.QPixmap(DEFAULT_NPC_VEHICLE_IMG).scaled(50, 50)
            self.npc_vehicle_direction = self.ask_npc_direction()
            if self.npc_vehicle_direction == self.NPC_DIRECTION['OPPOSITE']:
                self.npc_vehicle_position = QtCore.QPoint(self.DEFAULT_NPC_POSITION_X['OPPOSITE'],
                                                          self.DEFAULT_NPC_POSITION_Y['OPPOSITE'])
            elif self.npc_vehicle_direction == self.NPC_DIRECTION['CROSS']:
                self.npc_vehicle_position = QtCore.QPoint(self.DEFAULT_NPC_POSITION_X['CROSS'],
                                                          self.DEFAULT_NPC_POSITION_Y['CROSS'])
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

        self.initUI()

    def decrease_button_pressed(self):
        self.dec_button_pressed = True

    def increase_button_pressed(self):
        self.inc_button_pressed = True

    def ask_to_load_image(self, message):
        reply = QMessageBox.question(self, 'Load Image', message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def ask_npc_direction(self):
        message_box = QMessageBox()
        # message_box.setWindowTitle("Message")
        message_box.setText("Please select the driving direction for NPC vehicle.")
        message_box.addButton(QMessageBox.Yes)
        message_box.button(QMessageBox.Yes).setText("Opposite")
        message_box.addButton(QMessageBox.No)
        message_box.button(QMessageBox.No).setText("Cross")
        choice = message_box.exec()
        if choice == QMessageBox.Yes:
            return self.NPC_DIRECTION["OPPOSITE"]
        elif choice == QMessageBox.No:
            return self.NPC_DIRECTION["CROSS"]
        else:
            return ''

    def rotate_pixmap(self, pixmap, degrees):
        transform = QtGui.QTransform().rotate(degrees)
        rotated_pixmap = pixmap.transformed(transform, mode=QtCore.Qt.SmoothTransformation)
        return rotated_pixmap

    def change_speed(self, speed_value):
        self.speed = speed_value
        return str(self.speed) + ' km/h'

    def initUI(self):
        self.setMinimumSize(self.crossroad_pixmap.size())
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)  # Timer interval in milliseconds

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
        near_banana = self.load_banana and (
                self.banana_rect.left() - 60 <= self.car_position.x() <= self.banana_rect.right()
        )
        if self.dec_button_pressed:
            newSpeed = self.speed - 3
            if newSpeed > 0:
                self.speed = newSpeed
                self.speedInfo.setText(self.change_speed(newSpeed))
                self.dec_button_pressed = False

        if self.inc_button_pressed:
            newSpeed = self.speed + 3
            self.change_speed(newSpeed)
            self.speedInfo.setText(self.change_speed(newSpeed))
            self.inc_button_pressed = False

        if near_banana and self.speed > 10:
            newSpeed = 10
            self.change_speed(newSpeed)
            self.speedInfo.setText(self.change_speed(newSpeed))
            print('1001' + ": " + self.LOG_CODES['1001'])  # record the console

        # Check if the car is near the stop sign
        if self.load_stop and self.car_position.x() >= self.stop_position.x() - 80:
            self.timer.stop()
            print('1002' + ": " + self.LOG_CODES['1002'])  # Reporting to the console
            self.destination_query()
            return  # Stop the animation

        if self.load_npc_vehicle:
            # NPC driving
            if self.load_npc_vehicle and self.npc_vehicle_direction == self.NPC_DIRECTION["OPPOSITE"]:
                self.npc_vehicle_position.setX(self.npc_vehicle_position.x() - self.npc_speed)
            elif self.load_npc_vehicle and self.npc_vehicle_direction == self.NPC_DIRECTION["CROSS"]:
                self.npc_vehicle_position.setY(self.npc_vehicle_position.y() + self.npc_speed)
            # Check whether there will be a collision with NPC vehicle
            if self.npc_vehicle_direction != self.NPC_DIRECTION["OPPOSITE"] and (
                    (
                            abs(self.car_position.x() - self.npc_vehicle_position.x())
                            < (self.speed + 20)
                    )
                    and abs(self.car_position.y() - self.npc_vehicle_position.y()) < self.speed
            ):
                self.timer.stop()
                print('1003' + ": " + self.LOG_CODES['1003'])
                self.destination_query()
                return

        if not self.middle_point_reached and self.car_position.x() >= self.middle_point - 80:
            self.timer.stop()
            self.show_direction_dialog()
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
            QtWidgets.QApplication.exit(
                AnimatedCarWidget.EXIT_CODE_REBOOT)  # will exit with the exit code set above & stay in while loop of main
        else:
            self.timer.stop()
            sys.exit()

    def show_direction_dialog(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle('Choose Direction')
        layout = QVBoxLayout()

        btn_right = QPushButton('Turn right', self.dialog)
        btn_right.clicked.connect(self.on_direction_chosen)
        layout.addWidget(btn_right)

        btn_straight = QPushButton('Go straight', self.dialog)
        btn_straight.clicked.connect(self.on_direction_chosen)
        layout.addWidget(btn_straight)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def on_direction_chosen(self):
        sender = self.sender()
        if sender.text() == 'Turn right':
            self.turning_right = True
            self.middle_point_reached = True
        else:
            self.direction = 'right'
            self.middle_point_reached = True
        self.dialog.close()
        self.timer.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        config_dialog = ConfigurationDialog()
        config_dialog.exec_()  # This will block until the dialog is closed
        config_dialog.close()
        self.central_widget = AnimatedCarWidget(self)
        print(f"Selected Sceanrio: {config_dialog.selected_scenario}")
        self.central_widget.selected_scenario = config_dialog.selected_scenario
        self.setCentralWidget(self.central_widget)
        self.showMaximized()
        self.setWindowTitle('Autonomous Driving Simulation')


def main():
    exitCode = AnimatedCarWidget.EXIT_CODE_REBOOT  # set exit code so code will run
    while exitCode == AnimatedCarWidget.EXIT_CODE_REBOOT:  # will keep rebooting the program until user selects quit (with different exit code)
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        exitCode = app.exec()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
