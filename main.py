from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
from contacts import *
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
        self.btn_info.clicked.connect(self.inf)

    def inf(self):
        try:
            self.ex = Contacts(self.facultet)
            self.ex.show()
        except Exception as er:
            print(er)

    def schedule(self):
        try:
            dt = self.curs.execute(f"""Select timetable from Groups where id = {self.user[2]}""")
            self.shed = Example(dt)
            self.shed.show()
        except Exception as er:
            print(er)


class Example(QWidget):

    def __init__(self, path):
        self.path = path
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        pixmap = QtGui.QPixmap(self.path)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Photo')
        self.show()


class Contacts(QMainWindow, Ui_Contacts):
    def __init__(self, facultet):
        self.facultet = facultet
        super(Contacts, self).__init__()
        self.setupUi(self)
        if self.facultet == 1:
            self.lbl_decan.setText("""Декан - Пупкин Василий Эдуардович 
(телефон 8 (800) 000-00-01, E-mail - pupkin.v.sgu@yandex.ru) 
Зам. декана - Прекрасная Василиса Ивановна 
(телефон 8 (800) 000-00-02, E-mail - prekrasnaya.v.sgu@yandex.ru) 
Секретарь - Секретарев Дмитрий Борисович 
(телефон 8 (800) 000-00-03, E-mail - sekretarev.d.sgu@yandex.ru) 
Секретарь - Ухов Евгений Олегович 
(телефон 8 (800) 000-00-04, E-mail - uhov.e.sgu@yandex.ru) 
""")
        elif self.facultet == 2:
            self.lbl_decan.setText(""" Декан - Иванов Иван Иванович
                                   (телефон 8 (800) 001-00-01, E-mail - ivanov.i.sgu@yandex.ru)
            Зам. декана - Сидоров Сергей Петрович
            (телефон 8 (800) 001-00-02, E-mail - sidorov.s.sgu@yandex.ru)
            Секретарь - Петрова Ирина Викторовна
            (телефон 8 (800) 001-00-03, E-mail - petrova.i.sgu@yandex.ru)
            """)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Join()
    mainWindow.show()
    sys.exit(app.exec())
