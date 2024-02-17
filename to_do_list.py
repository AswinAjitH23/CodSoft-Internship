from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5 import uic
import pickle

class Todo(QMainWindow):

    def __init__(self):
        super(Todo, self).__init__()
        uic.loadUi("todolistgui.ui", self)
        self.show()

        self.setFixedSize(674, 567)
        #self.
        self.setWindowTitle("To-Do-List v0.1")
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)

        self.AddButton.clicked.connect(self.add_todo)
        self.RemoveButton.clicked.connect(self.remove_todo)
        self.actionLoad.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionClear.triggered.connect(self.clear_file)


    def add_todo(self):
        todo, confirmed = QInputDialog.getText(self, "Add Todo", "New Todo", QLineEdit.Normal, "")

        if confirmed and not todo.isspace():
            item = QStandardItem(todo)
            self.model.appendRow(item)

    def remove_todo(self):
        if len(self.listView.selectedIndexes()) != 0:
            selected = self.listView.selectedIndexes()[0]

            dialog = QMessageBox()
            dialog.setWindowTitle("Remove To-Do")
            dialog.setText(f"Do you want to remove '{selected.data()}'?")
            dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)
            dialog.addButton(QPushButton("No"), QMessageBox.NoRole)

            if dialog.exec_() == 0:
                self.model.removeRow(selected.row())

    def open_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Todo Files (*.todo)", options=options)
        if filename != "":
            with open(filename, "rb") as f:
                item_list = pickle.load(f)
                self.model = QStandardItemModel()
                self.listView.setModel(self.model)
                for item in item_list:
                    self.model.appendRow(QStandardItem(item))

    def save_file(self):
        item_list = []
        for x in range(self.model.rowCount()):
            item_list.append(self.model.item(x).text())
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Todo Files (*.todo)", options=options)
        if filename != "":
            with open(filename, "wb") as f:
                pickle.dump(item_list, f)

    def clear_file(self):
        self.model.clear()

app = QApplication([])
window = Todo()
app.exec()