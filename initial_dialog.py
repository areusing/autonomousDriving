from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QRadioButton,
    QPushButton,
)

from constants import DEFAULT_OPTIONS_INITIAL_DIALOG


class InitialDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initial_scenario_mode = DEFAULT_OPTIONS_INITIAL_DIALOG[0]

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.renderRadioButtons(layout)

        # Create and setup the save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

    def renderRadioButtons(self, layout):
        for index, option in enumerate(DEFAULT_OPTIONS_INITIAL_DIALOG, start=0):
            radiobutton = QRadioButton(option)
            radiobutton.setChecked(True if index == 0 else False)
            radiobutton.value = option
            radiobutton.toggled.connect(self.onClicked)
            layout.addWidget(radiobutton, 0, index)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.initial_scenario_mode = radioButton.value

    def save(self):
        self.accept()
