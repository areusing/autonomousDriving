from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QComboBox,
)

from constants import (
    DEFAULT_CUSTOMIZATION_OTHER_CAR_OPTIONS,
    DEFAULT_CUSTOMIZATION_COLUMNS,
)


class CustomizationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.input_list = []
        self.customized_scenario = {}

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        column_width = 150
        column_spacing = 15  # Adjust the spacing value as needed
        layout.setHorizontalSpacing(column_spacing)
        layout.setVerticalSpacing(column_spacing)

        for i in range(0, 2):
            for j in range(0, len(DEFAULT_CUSTOMIZATION_COLUMNS)):
                print(i, j)
                layout.setColumnMinimumWidth(j, column_width)
                layout.setColumnStretch(j, 0)
                if i == 0:
                    layout.addWidget(
                        QLabel(str(DEFAULT_CUSTOMIZATION_COLUMNS[j])), i, j
                    )
                else:
                    if j == 3:
                        dropdown = QComboBox()
                        dropdown.addItems(DEFAULT_CUSTOMIZATION_OTHER_CAR_OPTIONS)
                        self.input_list.append(dropdown)
                        layout.addWidget(dropdown, i, j)
                    else:
                        checkbox = QCheckBox()
                        self.input_list.append(checkbox)
                        layout.addWidget(checkbox, i, j)

        # Create and setup the save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button, 2, 0, 1, 4)

    def getInputValue(self):
        for j in range(0, len(DEFAULT_CUSTOMIZATION_COLUMNS)):
            colKey = DEFAULT_CUSTOMIZATION_COLUMNS[j]
            if j == 3:
                dropdown_value = self.input_list[j].currentText()
                self.customized_scenario[colKey] = dropdown_value
            else:
                checkbox_state = self.input_list[j].isChecked()
                self.customized_scenario[colKey] = checkbox_state

    def save(self):
        self.getInputValue()
        self.accept()
