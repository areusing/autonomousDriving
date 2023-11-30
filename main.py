import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from animated_car_widget import AnimatedCarWidget


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

def main():
    """
    Main function to run the Autonomous Driving Simulation.
    It creates the main application and window, and manages the application lifecycle.
    """
    exit_code = AnimatedCarWidget.EXIT_CODE_REBOOT  # Initial exit code for reboot
    while exit_code == AnimatedCarWidget.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        exitCode = app.exec()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
