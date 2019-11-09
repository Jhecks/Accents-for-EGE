import sys
from PyQt5 import QtWidgets, QtCore
import QTTest
import pymysql
from pymysql.cursors import DictCursor
import random


def initialization():
    global db
    db = pymysql.connect(
    host='localhost',
    user='root',
    password='1111',
    db='dictionary',
    charset='utf8mb4',
    cursorclass=DictCursor)

    global words
    words = []
    global words_acc
    words_acc = []

    with db.cursor() as cursor:
        query = """
        SELECT
            word
        FROM
            tDictionary
        """
        if cursor.execute(query):
            for row in cursor:
                words.append(row['word'])

    with db.cursor() as cursor:
        query = """
        SELECT
            word_with_accent
        FROM
            tDictionary
        """
        if cursor.execute(query):
            for row in cursor:
                words_acc.append(row['word_with_accent'])


def get_data(model):
    model.setStringList(words)


class App(QtWidgets.QMainWindow, QTTest.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        completer = QtWidgets.QCompleter()
        self.lineEdit.setCompleter(completer)
        model = QtCore.QStringListModel()
        completer.setModel(model)
        get_data(model)
        self.pushButton.clicked.connect(self.Button1)
        self.pushButton_2.clicked.connect(self.Button2)
        self.lineEdit.returnPressed.connect(self.Button1)

    def Button1(self):
        InputText = self.lineEdit.text()
        with db.cursor() as cursor:
            query = """
                        SELECT
                            word_with_accent
                        FROM
                            tDictionary
                        WHERE 
                            word=%s
                        """
            if cursor.execute(query, InputText):
                for row in cursor:
                    self.textBrowser.setText(row['word_with_accent'])
            elif InputText == '':
                self.textBrowser.setText('Введите слово')
            else:
                self.textBrowser.setText('Слово не найдено')

    def Button2(self):
        random_num = int(random.uniform(0, len(words)))
        self.lineEdit.setText(words[random_num])
        self.textBrowser.setText(words_acc[random_num])


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
