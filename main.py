# This is a sample Python script.
import os
import sys
import random

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QPalette, QColor

from field1 import Ui_MainWindow
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QStyle

from split_image import main



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # наш код

        self.move(500, 150)  # располагаем окно посередине
        self.flag = 0  # флаг первого хода
        self.num_step = 0  # счетчик ходов
        self.pushButton.clicked.connect(self.game)  # вызываем функцию для выбора файла




    def game(self):
        text_label = str(self.num_step)
        self.button_new_game = QPushButton('Новая игра')
        self.button_new_game.setMaximumSize(QtCore.QSize(90, 30))
        self.horizontalLayout.addWidget(self.button_new_game)
        self.pushButton.hide()
        self.spinBox.hide()
        self.label.setText(text_label)
        self.button_new_game.clicked.connect(self.new_game)

        self.size = self.spinBox.value()
        self.dict_piece = main(self.size)
        # Создаем список чисел
        num0 = [i for i in range(int((self.size**2)/2))]
        num = num0+num0
        random.shuffle(num)
        # Создаем словарик ключoм которого является индекс строки и столбца наших кнопок,
        # а значение цифры открываемые кнопками
        self.button_num = dict()
        for row in range(self.size):
            for col in range(self.size):
                self.button_num[f'{row}{col}'] = num.pop()
        # функция создания кнопок
        self.create_buttons()



    def create_buttons(self):
        '''Создаем кнопки игрового поля'''
        self.dict_button = dict()

        self.field_layout = QGridLayout()
        # Задаем расстояние между элементами компоновщика
        self.field_layout.setSpacing(5)

        # Задаем отступы вокруг компоновщика
        self.field_layout.setContentsMargins(1, 1, 1, 1)
        for row in range(self.size):
            for col in range(self.size):
                button = QPushButton('')
                button.setObjectName(f"Button{row}{col}")
                button.setMaximumSize(QtCore.QSize(30, 30))
                button.setMinimumSize(QtCore.QSize(30, 30))
                button.setStyleSheet("background-color: rgb(74, 161, 228);color: black")
                button.clicked.connect(self.button_clicked)  # Связываем каждую кнопку с обработчиком
                self.field_layout.addWidget(button, row, col)
                self.dict_button[f"Button{row}{col}"] = button

        self.verticalLayout.addLayout(self.field_layout)
        self.setMaximumWidth(self.size*35 + 10)



    def button_clicked(self):
        # Обработчик нажатия на кнопку
        sender_button = self.sender()
        button_object_name = sender_button.objectName()
        
        index = button_object_name[-2:]  # получаем индекс нажатой кнопки
        num = self.button_num[index]  # получаем номер по индексу
        self.dict_button["Button"+index].setText(str(num))  # ставим номер на нажатую кнопку

        self.num_step += 1
        text_label = str(self.num_step)
        self.label.setText(text_label)
        if self.flag == 0:
            self.flag = 1
            self.first_num = num
            self.first_num_index = index


        else:
            if self.dict_button["Button" + index] == self.dict_button["Button" + self.first_num_index]:
                return
            self.second_num = num
            if self.first_num == self.second_num:
                self.dict_button["Button" + index].setText('')
                self.set_image_to_button(self.dict_button["Button" + index], index)
                self.dict_button["Button" + index].setEnabled(False)

                # Создаем палитру
                palette = QPalette()

                # Определяем цвет фона виджета
                palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)


                # Устанавливаем палитру для кнопки
                self.dict_button["Button" + index].setPalette(palette)

                # self.dict_button["Button" + index].setStyleSheet("background-color: rgb(223, 118, 118);color: black")
                self.dict_button["Button" + self.first_num_index].setText('')
                self.set_image_to_button(self.dict_button["Button" + self.first_num_index], self.first_num_index)
                self.dict_button["Button" + self.first_num_index].setEnabled(False)
                self.dict_button["Button" + self.first_num_index].setPalette(palette)

                # self.dict_button["Button" + self.first_num_index].setStyleSheet("background-color: rgb(223, 118, 118);color: black")

            else:

                self.dict_button["Button" + self.first_num_index].setText('')
                self.first_num = num
                self.first_num_index = index

    def set_image_to_button(self, but, ind):
        # Преобразуем массив NumPy в изображение Pillow
        pillow_image = self.dict_piece[ind]

        # Записываем изображение не кнопке в файл
        paths = os.path.join(os.getcwd(), f"piece.jpg")
        pillow_image.save(paths)
        # устанавливаем изображение с файла
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(paths), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        but.setIcon(icon)
        but.setIconSize(QtCore.QSize(30, 30))



    def new_game(self):
        self.close()

        # Создание нового экземпляра окна, обязательно при инициализации прописываем
        # parent=None, а в __init__ parent см. выше
        window = MyApp(parent=self)
        window.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
