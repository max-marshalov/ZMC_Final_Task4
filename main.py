from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
from join import *
from student_room import *
import sys
import os


class Join(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Join()
        self.ui.setupUi(self)

        self.ui.label_error.hide()

        self.ui.btn_join.clicked.connect(self.go_join)

    def go_join(self):
        Login = None
        Password = None

        if len(self.ui.edit_login.text()) > 0:
            Login = self.ui.edit_login.text()
        else:
            self.ui.label_error.setText("Введите логин и пароль")
            self.ui.label_error.show()
            return

        if len(self.ui.edit_password.text()) > 0:
            Password = self.ui.edit_password.text()
        else:
            self.ui.label_error.setText("Введите логин и пароль")
            self.ui.label_error.show()
            return

        con = sqlite3.connect("DATABASE.db")
        curs = con.cursor()
        fio = curs.execute(
            """SELECT id FROM UserForm WHERE email = "{}" and password = "{}" """.format(Login,
                                                                                         Password)).fetchall()

        if not fio:
            try:
                self.ui.label_error.setText("Неверный логин или пароль")
                self.ui.label_error.show()
                return
            except Exception as ex:
                print(ex)
        else:

            fio = curs.execute(
                """SELECT id FROM UserForm WHERE email = "{}" and password = "{}" """.format(Login,
                                                                                             Password)).fetchall()[0][0]

            ex = curs.execute(f"""Select Branch, facultet, Groups from Students Where FIO = {fio}""").fetchall()[0]
            try:
                self.win = Main("DATABASE.db", ex)
                self.close()
                self.win.show()
            except Exception as er:
                print(er)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, path, user):
        self.path = path
        self.user = user
        super(Main, self).__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(self.path)
        self.curs = self.con.cursor()
        self.branch = self.curs.execute(f"""Select name FROM Branches Where id = {self.user[0]}""").fetchall()[0][0]
        self.facultet = self.curs.execute(f"""Select name FROM Facultets Where id = {self.user[1]}""").fetchall()[0][0]
        self.group = self.curs.execute(f"""Select name FROM Groups Where id = {self.user[2]}""").fetchall()[0][0]
        print(self.group, self.branch, self.facultet)
        self.lbl_branch.setText(self.branch)
        self.lbl_fuck.setText(self.facultet)
        self.lbl_group.setText(str(self.group))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Join()
    mainWindow.show()
    sys.exit(app.exec())