from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton
)

from constants import (
    DEFAULT_COLUMNS_FOR_CONFIGURATION_DIALOG,
    DEFAULT_ROWS_FOR_CONFIGURATION_DIALOG
)


class ConfigurationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.selected_scenario = None

    def initUI(self):
        self.resize(1000,400)

        # Create a QVBoxLayout instance, QVBoxLayout will help the table
        # widget to take up the entie space available in the dialog
        layout = QVBoxLayout(self)

        # Initialize tableWidget and set properties
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(9)

        # Setup for vertical and horizontal table items
        self.setupTableItems()

        # Set dynamic resize mode for the columns
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # Select the first row by default
        self.tableWidget.selectRow(0)

        # Add tableWidget to the layout
        layout.addWidget(self.tableWidget)

        # Create and setup the save button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

    def setupTableItems(self):
        self.tableWidget.setHorizontalHeaderLabels(DEFAULT_COLUMNS_FOR_CONFIGURATION_DIALOG)

        for i, row in enumerate(DEFAULT_ROWS_FOR_CONFIGURATION_DIALOG):
            for j, val in enumerate(row):
                item = QTableWidgetItem(val)
                # item.setFlags(QtCore.Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, j, item)

    def save(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            selected_row = self.tableWidget.row(selected_items[0])
            self.selected_scenario = f"Scenario {selected_row + 1}"
        else:
            self.selected_scenario = None
        self.accept()
