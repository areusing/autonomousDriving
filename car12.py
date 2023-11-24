import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog, QPushButton, QVBoxLayout
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
        self.middle_point = 835  # Middle point position
        self.direction = 'right'
        self.middle_point_reached = False
        self.turning_right = False  # defaiult for turning right
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
        self.timer.start(100)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.crossroad_pixmap)
        if self.load_banana:
            banana_position = QtCore.QPoint(500, 530)
            painter.drawPixmap(banana_position, self.banana_pixmap)
        if self.load_stop:
            painter.drawPixmap(self.stop_position, self.stop_pixmap)
        painter.drawPixmap(self.car_position, self.car_pixmap)

    def animate(self):
        near_banana = self.load_banana and (
            self.banana_rect.left() - 60 <= self.car_position.x() <= self.banana_rect.right()
        )

        if near_banana:
            speed = 15
        else:
            speed = 25

        if self.load_stop and self.car_position.x() >= self.stop_position.x() - 80:
            self.timer.stop()
            self.plot_track()
            return

        if not self.middle_point_reached and self.car_position.x() >= self.middle_point - 80:
            self.timer.stop()
            self.show_direction_dialog()
            return

        if self.turning_right and self.car_position.x() < self.middle_point + 80:
            self.car_position.setX(self.car_position.x() + speed)
            if self.car_position.x() >= self.middle_point + 0:
                self.direction = 'down'
                self.turning_right = False
            self.update()
            return

        self.positions.append((self.car_position.x(), self.car_position.y()))

        if not self.middle_point_reached:
            self.car_position.setX(self.car_position.x() + speed)
            if self.car_position.x() > self.middle_point:
                self.middle_point_reached = True
        else:
            if self.direction == 'right':
                self.car_position.setX(self.car_position.x() + speed)
            elif self.direction == 'down':
                self.car_position.setY(self.car_position.y() + speed)

            if (self.direction == 'right' and self.car_position.x() > self.width()) or \
               (self.direction == 'down' and self.car_position.y() > self.height()):
                self.timer.stop()
                self.plot_track()

        self.update()

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
        self.dialog.exec_()

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

    def plot_track(self):
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