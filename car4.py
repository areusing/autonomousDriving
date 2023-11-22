import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
import seaborn as sns
import matplotlib.pyplot as plt

class AnimatedCarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AnimatedCarWidget, self).__init__(parent)
        self.crossroad_pixmap = QtGui.QPixmap('Cross_road.png')
        self.car_pixmap = QtGui.QPixmap('car.jpeg').scaledToWidth(50)

        # set the start point
        self.car_position = QtCore.QPoint(110, 530)

        # let initial direction is right
        self.direction = 'right'

        # when car has reached the middle
        self.middle_point_reached = False

        #  record positions
        self.positions = []

        self.initUI()

    def initUI(self):
        self.setMinimumSize(self.crossroad_pixmap.size())
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)  # Timer interval in milliseconds

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.crossroad_pixmap)
        painter.drawPixmap(self.car_position, self.car_pixmap)

    def animate(self):
        self.positions.append((self.car_position.x(), self.car_position.y()))

        if not self.middle_point_reached:
            # Move right
            self.car_position.setX(self.car_position.x() + 5)

          #when arrivae the middle point
            if self.car_position.x() > 835:
                self.middle_point_reached = True
                # Randomly choose trun right or down
                self.direction = random.choice(['right', 'down'])
        else:
            # After reaching the middle point, move to chosen direction
            if self.direction == 'right':
                self.car_position.setX(self.car_position.x() + 5)
            else:
                self.car_position.setY(self.car_position.y() + 5)

            # when car is out of the window ,stop the programme
            if (self.direction == 'right' and self.car_position.x() > self.width()) or \
                    (self.direction == 'down' and self.car_position.y() > self.height()):
                self.timer.stop()
                self.plot_track()  # Plot the trajectory

        self.update()

    def plot_track(self):
        # record the data for seaborn
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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()