
import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import seaborn as sns
import matplotlib.pyplot as plt

class AnimatedCarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AnimatedCarWidget, self).__init__(parent)
        self.crossroad_pixmap = QtGui.QPixmap('Cross_road.png')
        self.car_pixmap = QtGui.QPixmap('car.jpeg').scaledToWidth(50)

        self.load_banana = self.ask_to_load_image('Add Road Slip?')
        if self.load_banana:
            self.banana_pixmap = QtGui.QPixmap('banana.png').scaled(200, 50)
            self.banana_rect = QtCore.QRect(500, 530, 200, 50)

        self.load_stop = self.ask_to_load_image('Add Roadblocks?')
        if self.load_stop:
            self.stop_pixmap = QtGui.QPixmap('stop.png').scaled(50, 50)
            self.stop_position = QtCore.QPoint(1100, 530)  # Stop image position

        self.car_position = QtCore.QPoint(110, 530)

        # Initial direction is right
        self.direction = 'right'

        # When car has reached the middle
        self.middle_point_reached = False

        # Record positions
        self.positions = []

        self.initUI()

    def ask_to_load_image(self, message):
        reply = QMessageBox.question(self, 'Load Image', message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

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
        painter.drawPixmap(self.car_position, self.car_pixmap)

    def animate(self):
        # Check if the car is over the banana
        near_banana = self.load_banana and (
            self.banana_rect.left() - 60 <= self.car_position.x() <= self.banana_rect.right()
        )

        if near_banana:
            speed = 15  # reduce speed
            print("1001: reduce speed")  # record the console
        else:
            speed = 25  # Normal speed

        # Check if the car is near the stop sign
        if self.load_stop and self.car_position.x() >= self.stop_position.x() - 80:
            self.timer.stop()
            print("1002: emergency stop")  # Reporting to the console
            self.plot_track()  # Plot the trajectory
            return  # Stop the animation

        self.positions.append((self.car_position.x(), self.car_position.y()))

        if not self.middle_point_reached:
            self.car_position.setX(self.car_position.x() + speed)

            # When arrive at the middle point
            if self.car_position.x() > 835:
                self.middle_point_reached = True
                # Randomly choose turn right or down
                self.direction = random.choice(['right', 'down'])
        else:
            # when to middle point, move in the chosen direction
            if self.direction == 'right':
                self.car_position.setX(self.car_position.x() + speed)
            else:
                self.car_position.setY(self.car_position.y() + speed)

            # When car is out of the window, stop the program
            if (self.direction == 'right' and self.car_position.x() > self.width()) or \
                    (self.direction == 'down' and self.car_position.y() > self.height()):
                self.timer.stop()
                self.plot_track()  # Plot the trajectory

        self.update()

    def plot_track(self):
        # Record the data for seaborn
        x_data, y_data = zip(*self.positions)
        sns.lineplot(x=x_data, y=y_data)

        plt.xlabel('Horizontal Record')
        plt.ylabel('Vertical Record')
        plt.title('Car Track')
        plt.show(block=True)

class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = AnimatedCarWidget(self)
        self.setCentralWidget(self.central_widget)
        self.resize(self.central_widget.size())
        self.setWindowTitle('Crossroad Animation')
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    app.exec_()

if __name__ == '__main__':
    main()