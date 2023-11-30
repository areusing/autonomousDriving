import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from animated_car_widget import AnimatedCarWidget
from PyQt5 import QtWidgets

class MainWindow(QMainWindow):
    """
    Main Window of the Autonomous Driving Simulation.
    It sets up the AnimatedCarWidget as the central widget.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = AnimatedCarWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Autonomous Driving Simulation')
        self.center_on_screen()

    def center_on_screen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def show(self):
        super().show()  # 调用基类的 show 方法
        self.center_on_screen()

def main():
    """
    Main function to run the Autonomous Driving Simulation.
    It creates the main application and window, and manages the application lifecycle.
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
