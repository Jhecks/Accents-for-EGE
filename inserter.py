import sys
from PyQt5 import QtWidgets
import Designe
import pymysql
from pymysql.cursors import DictCursor


def initialization():
    global db
    db = pymysql.connect(
    host='localhost',
    user='root',
    password='1111',
    db='dictionary',
    charset='utf8mb4',
    cursorclass=DictCursor)


class App(QtWidgets.QMainWindow, Designe.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Button1)
        self.lineEdit.returnPressed.connect(self.Button1)

    def Button1(self):
        try:
            InputText = self.lineEdit.text()
            with db.cursor() as cursor:
                query = "INSERT INTO inserter (word, word_with_accent) VALUES (lower(%s), %s)"
                value = (InputText, InputText)
                cursor.execute(query, value)
                db.commit()
                self.lineEdit.clear()
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            if inst.args[0] == 1062:
                self.lineEdit.setText("Слово уже существует")


def main():
    try:
        initialization()
        app = QtWidgets.QApplication(sys.argv)
        window = App()
        window.show()
        app.exec_()
        db.close()
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)


if __name__ == '__main__':
    main()
