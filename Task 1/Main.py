import math

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

import MainWindow
import InputCords
import Results
import Error


class Enter(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_data)

    def get_data(self):
        flag = 1
        if self.From_box.currentText() == 'Полярных' and (self.To_box.currentText() == 'Цилиндрические' or self.To_box.currentText() == 'Сферические'):
            self.new_error = Errors('Перевод невозможен')
            self.new_error.show()
            flag = 0
        if (self.From_box.currentText() == 'Цилиндрических' or self.From_box.currentText() == 'Сферических') and self.To_box.currentText() == 'Полярные':
            self.new_error = Errors('Перевод невозможен')
            self.new_error.show()
            flag = 0
        if self.To_box.currentText()[0] == self.From_box.currentText()[0]:
            self.new_error = Errors('Введите разные СК')
            self.new_error.show()
            flag = 0
        if flag:
            self.close()
            self.start = Cords(self.From_box.currentText(), self.To_box.currentText(), self.Znaki_box.currentText())
            self.start.show()


class Cords(QtWidgets.QWidget, InputCords.Ui_InputCords):
    def __init__(self, from_, to_, tochn):
        super().__init__()
        self.from_ = from_
        self.to_ = to_
        self.tochn = tochn
        self.setupUi(self)
        self.flag = 0
        if self.from_ == 'Декартовых' and self.to_ != 'Полярные':
            self.first_input.setText('X')
            self.second_input.setText('Y')
            self.first_input_2.setText('Z')
        if self.from_ == 'Декартовых' and self.to_ == 'Полярные':
            self.first_input.setText('X')
            self.second_input.setText('Y')
            self.first_input_2.hide()
            self.lineEdit_3.hide()
        if self.from_ == 'Полярных':
            self.first_input.setText('r')
            self.second_input.setText('Ω')
            self.first_input_2.hide()
            self.lineEdit_3.hide()
            self.flag = 2
        if self.from_ == 'Сферических':
            self.first_input.setText('r')
            self.second_input.setText('φ')
            self.first_input_2.setText('θ')
            self.about_rad_1.setText('в радианах')
            self.about_rad_2.setText('в радианах')
            self.flag = 3
        if self.from_ == 'Цилиндрических':
            self.first_input.setText('r')
            self.second_input.setText('φ')
            self.first_input_2.setText('Z')
            self.about_rad_1.setText('в радианах')
            self.flag = 4
        self.pushButton.clicked.connect(self.perevod)

    def perevod(self):
        if self.from_ == 'Декартовых' and self.to_ == 'Полярные':
            self.x = float(self.lineEdit.text())
            self.y = float(self.lineEdit_2.text())
            result = self.from_decart_to_polar(self.x, self.y, int(self.tochn))
            self.close()
            self.new_result = Result((self.x, self.y), result, self.from_, self.to_)
            self.new_result.show()

        if self.from_ == 'Декартовых' and self.to_ == 'Цилиндрические':
            try:
                self.x = float(self.lineEdit.text())
                self.y = float(self.lineEdit_2.text())
                self.z = float(self.lineEdit_3.text())
                result = self.from_decart_to_cylinder(self.x, self.y, self.z, int(self.tochn))
                self.close()
                self.new_result = Result((self.x, self.y, self.z), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

        if self.from_ == 'Декартовых' and self.to_ == 'Сферические':
            try:
                self.x = float(self.lineEdit.text())
                self.y = float(self.lineEdit_2.text())
                self.z = float(self.lineEdit_3.text())
                result = self.from_decart_to_sphere(self.x, self.y, self.z, int(self.tochn))
                self.close()
                self.new_result = Result((self.x, self.y, self.z), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

        if self.from_ == 'Полярных' and self.to_ == 'Декартовы':
            try:
                self.r = float(self.lineEdit.text())
                self.fi = float(self.lineEdit_2.text())
                result = self.from_polar_to_decart(self.r, self.fi, int(self.tochn))
                self.close()
                self.new_result = Result((self.r, self.fi), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

        if self.from_ == 'Цилиндрических' and self.to_ == 'Сферические':
            try:
                self.r = float(self.lineEdit.text())
                self.fi = float(self.lineEdit_2.text())
                self.z = float(self.lineEdit_3.text())
                part_result = self.from_cylinder_to_decart(self.r, self.fi, self.z, int(self.tochn))
                result = self.from_decart_to_sphere(part_result[0], part_result[1], part_result[2], int(self.tochn))
                self.close()
                self.new_result = Result((self.r, self.fi, self.z), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

        if self.from_ == 'Цилиндрических' and self.to_ == 'Декартовы':
            try:
                self.r = float(self.lineEdit.text())
                self.fi = float(self.lineEdit_2.text())
                self.z = float(self.lineEdit_3.text())
                result = self.from_cylinder_to_decart(self.r, self.fi, self.z, int(self.tochn))
                self.close()
                self.new_result = Result((self.r, self.fi, self.z), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

        if self.from_ == 'Сферических' and self.to_ == 'Декартовы':
            try:
                self.r = float(self.lineEdit.text())
                self.fi = float(self.lineEdit_2.text())
                self.tetta = float(self.lineEdit_3.text())
                result = self.from_sphere_to_decart(self.r, self.fi, self.tetta, int(self.tochn))
                self.close()
                self.new_result = Result((self.r, self.fi, self.tetta), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

        if self.from_ == 'Сферических' and self.to_ == 'Цилиндрические':
            try:
                self.r = float(self.lineEdit.text())
                self.fi = float(self.lineEdit_2.text())
                self.tetta = float(self.lineEdit_3.text())
                part_result = self.from_sphere_to_decart(self.r, self.fi, self.tetta, int(self.tochn))
                result = self.from_decart_to_cylinder(part_result[0], part_result[1], part_result[2], int(self.tochn))
                self.close()
                self.new_result = Result((self.r, self.fi, self.tetta), result, self.from_, self.to_)
                self.new_result.show()
            except:
                self.new_error = Errors('Некорректный ввод')
                self.new_error.show()

    def get_r(self, x, y):
        return (x ** 2 + y ** 2) ** 0.5

    def get_r_sphere(self, x, y, z):
        return (x ** 2 + y ** 2 + z ** 2) ** 0.5

    def get_arccos(self, x, y):
        return math.acos(x / y)

    def get_omega(self, x, y):
        return math.atan2(y, x)

    # def from_decart_to_polar(self, x, y, symbols_to_point):
    #     return (round(self.get_r(x, y), symbols_to_point), round(self.get_omega(x, y), symbols_to_point))
    #
    # # r - радиус вектор omega - угол между положительным направлением оси x и радиусом-вектором r
    # def from_polar_to_decart(self, r, omega, symbols_to_point):
    #     x = r * math.cos(omega)
    #     y = r * math.sin(omega)
    #     return (round(x, symbols_to_point), round(y, symbols_to_point))
    #
    # def from_decart_to_cylinder(self, x, y, z, symbols_to_point):
    #     r = self.get_r(x, y)
    #     omega = self.get_omega(x, y)
    #     return (round(r, symbols_to_point), round(omega, symbols_to_point), z)
    #
    # # r - радиус вектор omega - угол между положительным направлением оси x и радиусом-вектором r
    # def from_cylinder_to_decart(self, r, omega, z, symbols_to_point):
    #     x = r * math.cos(omega)
    #     y = r * math.sin(omega)
    #     return (round(x, symbols_to_point), round(y, symbols_to_point), round(z, symbols_to_point))
    #
    # def from_decart_to_sphere(self, x, y, z, symbols_to_point):
    #     r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    #
    #     theta = math.acos(z / r) if r != 0 else 0
    #
    #     phi = math.atan2(y, x)
    #
    #     return round(r, symbols_to_point), round(math.degrees(theta), symbols_to_point), round(math.degrees(phi), symbols_to_point)
    #
    # # r - радиус вектор omega - угол между положительным направлением оси x и радиусом-вектором r, psi - азимутальный угол (угол между осью x и проекцией вектора на плоскость xy
    # def from_sphere_to_decart(self, r, omega, psi, symbols_to_point):
    #     x = r * math.sin(omega) * math.cos(psi)
    #     y = r * math.sin(psi) * math.sin(omega)
    #     z = r * math.cos(omega)
    #     return (round(x, symbols_to_point), round(y, symbols_to_point), round(z, symbols_to_point))
    def from_decart_to_polar(self, x, y, symbols_to_point):
        return (round(self.get_r(x, y), symbols_to_point), round(self.get_omega(x, y), symbols_to_point))

    # r - радиус вектор omega - угол между положительным направлением оси x и радиусом-вектором r
    def from_polar_to_decart(self, r, omega, symbols_to_point):
        x = r * math.cos(omega)
        y = r * math.sin(omega)
        return (round(x, symbols_to_point), round(y, symbols_to_point))

    def from_decart_to_cylinder(self, x, y, z, symbols_to_point):
        r = self.get_r(x, y)
        omega = self.get_omega(x, y)
        return (round(r, symbols_to_point), round(omega, symbols_to_point), z)

    # r - радиус вектор omega - угол между положительным направлением оси x и радиусом-вектором r
    def from_cylinder_to_decart(self, r, omega, z, symbols_to_point):
        x = r * math.cos(omega)
        y = r * math.sin(omega)
        return (round(x, symbols_to_point), round(y, symbols_to_point), round(z, symbols_to_point))

    def from_decart_to_sphere(self, x, y, z, symbols_to_point):
        r = math.sqrt(self.x ** 2 + self.y**2 + self.z ** 2)

        # Вычисление угла teta (угол с осью z)
        teta = math.acos(self.z / r)

        # Вычисление угла phi (азимутальный угол)
        phi = math.atan2(self.y, self.x)

        return round(r, symbols_to_point), round(teta, symbols_to_point), round(phi, symbols_to_point)

    # r - радиус вектор omega - угол между положительным направлением оси x и радиусом-вектором r, psi - азимутальный угол (угол между осью x и проекцией вектора на плоскость xy
    def from_sphere_to_decart(self, r, omega, psi, symbols_to_point):
        x = r * math.sin(psi) * math.cos(omega)
        y = r * math.sin(psi) * math.sin(omega)
        z = r * math.cos(psi)
        return (round(x, symbols_to_point), round(y, symbols_to_point), round(z, symbols_to_point))


class Result(QtWidgets.QMainWindow, Results.Ui_Results):
    def __init__(self, base_cords_in_cortage, new_cords_in_cortage, from_, to_):
        super().__init__()
        self.setupUi(self)
        self.new_cords_in_cortage = new_cords_in_cortage
        self.base_cords_in_cortage = base_cords_in_cortage
        self.from_ = from_
        self.to_ = to_
        self.pushButton.clicked.connect(self.go_to_main)
        if self.from_ == 'Декартовых' and self.to_ == 'Полярные':
            self.base_3.hide()
            self.New_3.hide()
            self.Base_3_cord.hide()
            self.New_3_cord.hide()
            self.base_1.setText('X')
            self.base_2.setText('Y')
            self.New_1.setText('r')
            self.New_2.setText('Ω')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))

        if self.from_ == 'Декартовых' and self.to_ == 'Цилиндрические':
            self.base_1.setText('X')
            self.base_2.setText('Y')
            self.base_3.setText('Z')
            self.New_1.setText('r')
            self.New_2.setText('φ')
            self.New_3.setText('Z')
            self.about_rad_1.setText('в радианах')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.Base_3_cord.setText(str(base_cords_in_cortage[2]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))
            self.New_3_cord.setText(str(new_cords_in_cortage[2]))

        if self.from_ == 'Декартовых' and self.to_ == 'Сферические':
            self.base_1.setText('X')
            self.base_2.setText('Y')
            self.base_3.setText('Z')
            self.New_1.setText('r')
            self.New_2.setText('φ')
            self.New_3.setText('θ')
            self.about_rad_1.setText('в радианах')
            self.about_rad_2.setText('в радианах')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.Base_3_cord.setText(str(base_cords_in_cortage[2]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))
            self.New_3_cord.setText(str(new_cords_in_cortage[2]))

        if self.from_ == 'Полярных' and self.to_ == 'Декартовы':
            self.base_3.hide()
            self.New_3.hide()
            self.Base_3_cord.hide()
            self.New_3_cord.hide()
            self.base_1.setText('r')
            self.base_2.setText('Ω')
            self.New_1.setText('X')
            self.New_2.setText('Y')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))

        if self.from_ == 'Цилиндрических' and self.to_ == 'Сферические':
            self.base_1.setText('r')
            self.base_2.setText('φ')
            self.base_3.setText('Z')
            self.New_1.setText('r')
            self.New_2.setText('φ')
            self.New_3.setText('θ')
            self.about_rad_1.setText('в радианах')
            self.about_rad_2.setText('в радианах')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.Base_3_cord.setText(str(base_cords_in_cortage[2]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))
            self.New_3_cord.setText(str(new_cords_in_cortage[2]))

        if self.from_ == 'Цилиндрических' and self.to_ == 'Декартовы':
            self.base_1.setText('r')
            self.base_2.setText('φ')
            self.base_3.setText('Z')
            self.New_1.setText('X')
            self.New_2.setText('Y')
            self.New_3.setText('Z')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.Base_3_cord.setText(str(base_cords_in_cortage[2]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))
            self.New_3_cord.setText(str(new_cords_in_cortage[2]))

        if self.from_ == 'Сферических' and self.to_ == 'Декартовы':
            self.base_1.setText('r')
            self.base_2.setText('φ')
            self.base_3.setText('θ')
            self.New_1.setText('X')
            self.New_2.setText('Y')
            self.New_3.setText('Z')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.Base_3_cord.setText(str(base_cords_in_cortage[2]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))
            self.New_3_cord.setText(str(new_cords_in_cortage[2]))

        if self.from_ == 'Сферических' and self.to_ == 'Цилиндрические':
            self.base_1.setText('r')
            self.base_2.setText('φ')
            self.base_3.setText('θ')
            self.New_1.setText('r')
            self.New_2.setText('φ')
            self.New_3.setText('Z')
            self.about_rad_1.setText('в радианах')
            self.Base_1_cord.setText(str(base_cords_in_cortage[0]))
            self.Base_2_cord.setText(str(base_cords_in_cortage[1]))
            self.Base_3_cord.setText(str(base_cords_in_cortage[2]))
            self.New_1_cord.setText(str(new_cords_in_cortage[0]))
            self.New_2_cord.setText(str(new_cords_in_cortage[1]))
            self.New_3_cord.setText(str(new_cords_in_cortage[2]))

    def go_to_main(self):
        self.close()
        self.start = Enter()
        self.start.show()


class Errors(QtWidgets.QDialog, Error.Ui_Dialog):
    def __init__(self, text_error):
        super().__init__()
        self.setupUi(self)
        self.text_error = text_error
        self.Error.setText(self.text_error)
        self.pushButton.clicked.connect(self.close_dialog)

    def close_dialog(self):
        self.close()


dialog = QtWidgets.QApplication([])
d = Enter()
d.show()
dialog.exec_()
