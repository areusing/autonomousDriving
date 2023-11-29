from PyQt5 import QtCore, QtWidgets

from constants import (
    DEFAULT_SCENARIOS_CHECKED_POSITIONS,
    DEFAULT_COLUMN_HEADERS_FOR_CONFIGURATION_DIALOG
)


class Ui_ConfigurationDialog(object):
    def setupUi(self, ConfigurationDialog):
        ConfigurationDialog.setObjectName("ConfigurationDialog")
        ConfigurationDialog.resize(800, 600)

        # Create a QVBoxLayout instance, QVBoxLayout will help the table
        # widget to take up the entie space available in the dialog
        layout = QtWidgets.QVBoxLayout(ConfigurationDialog)

        # Initialize tableWidget and set properties
        self.tableWidget = QtWidgets.QTableWidget(ConfigurationDialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(9)
        self.tableWidget.setSortingEnabled(False)

        # Setup for vertical and horizontal header items
        self.setupHeaderItems()

        # Adding checkboxes and setting flags for table items
        self.setupTableItems()

        # Set dynamic resize mode for the columns
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # Add tableWidget to the layout
        layout.addWidget(self.tableWidget)

        self.retranslateUi(ConfigurationDialog)
        QtCore.QMetaObject.connectSlotsByName(ConfigurationDialog)

    def setupTableItems(self):
        # Adding checkboxes and setting flags for table items
        for row in range(9):
            for column in range(5):
                item = QtWidgets.QTableWidgetItem()
                flags = QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
                item.setFlags(flags)
                check_state = QtCore.Qt.Checked if (row, column) in DEFAULT_SCENARIOS_CHECKED_POSITIONS else QtCore.Qt.Unchecked
                item.setCheckState(check_state)
                self.tableWidget.setItem(row, column, item)

    def setupHeaderItems(self):
        # Setup for vertical and horizontal header items
        _translate = QtCore.QCoreApplication.translate
        for i in range(9):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate("ConfigurationDialog", f"Scenario {i + 1}"))
            self.tableWidget.setVerticalHeaderItem(i, item)

        for i, header in enumerate(DEFAULT_COLUMN_HEADERS_FOR_CONFIGURATION_DIALOG):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate("ConfigurationDialog", header))
            self.tableWidget.setHorizontalHeaderItem(i, item)

    def retranslateUi(self, ConfigurationDialog):
        ConfigurationDialog.setWindowTitle(QtCore.QCoreApplication.translate("ConfigurationDialog", "ConfigurationDialog"))
