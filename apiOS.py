#!-*-coding:utf-8-*-
from PyQt4 import QtGui


class ApiOS:
    FILE_EXTENDED = u'.dals'

    FILE_FORMAT_DALS = u'DataAnalysis file [.dals] (*.dals)'
    FILE_FORMAT_EXCEL_2007 = u'Microsoft Excel 2007/2010/2013 [.xlsx] (*.xlsx)'
    FILE_FORMAT_EXCEL_1997 = u'Microsoft Excel 97/2000/XP/2003 [.xls] (*.xls)'

    DIALOG_OPEN_PROJECT_NAME = u'Открыть проект'
    DIALOG_OPEN_DATA_NAME = u'Открыть файл с данными'
    DIALOG_SAVE_PROJECT_NAME = u"Сохранить проект"
    DIALOG_CREATE_PROJECT_NAME = u'Создать проект'

    NOT_PROJECT_BY_LOAD_DATA = u'Для закгрузки данных необходимо открыть проект'

    MESSAGE_WARNING = u'Предупреждение'
    MESSAGE_ERROR = u'Ошибка'

    MESSAGE_ASK_SAVE = u'Сохранить открытый проект?'

    VARIANT_SAVE_SCHEMA = 0
    VARIANT_NO_SAVE_SCHEMA = 1
    VARIANT_CANCEL = 2

    def __init__(self):
        pass

    def add_extended_to_file_name(self, file_name_without):
        return unicode(file_name_without) + self.FILE_EXTENDED

    def is_have_extended(self, file_path):
        extended_len = len(self.FILE_EXTENDED)
        extended = file_path[-extended_len:]

        if extended == self.FILE_EXTENDED:
            return True

        return False

    def get_list_format(self, formats):
        all_formats = ''
        for format_file in formats:
            all_formats += format_file + ';; '

        return all_formats[:-3]

    def show_open_schema_dialog(self, parent_window):
        schema_file_path = QtGui.QFileDialog.getOpenFileName(parent_window,
                                                             self.DIALOG_OPEN_PROJECT_NAME,
                                                             '',
                                                             self.FILE_FORMAT_DALS)
        if schema_file_path:
            return schema_file_path
        else:
            return None

    def show_open_data_dialog(self, parent_window):
        file_data_path = QtGui.QFileDialog.getOpenFileName(parent_window,
                                                           self.DIALOG_OPEN_DATA_NAME,
                                                           '',
                                                           self.get_list_format([self.FILE_FORMAT_EXCEL_2007,
                                                                                 self.FILE_FORMAT_EXCEL_1997]))
        if file_data_path:
            return file_data_path
        else:
            return None

    def show_save_schema_dialog(self, parent_window):
        file_schema_path = QtGui.QFileDialog.getSaveFileName(parent_window,
                                                             self.DIALOG_SAVE_PROJECT_NAME,
                                                             '',
                                                             self.FILE_FORMAT_DALS)
        if file_schema_path:
            return file_schema_path
        else:
            return None

    def show_create_schema_dialog(self, parent_window):

        new_schema_file_path = QtGui.QFileDialog.getSaveFileName(parent_window,
                                                                 self.DIALOG_CREATE_PROJECT_NAME,
                                                                 '',
                                                                 self.FILE_FORMAT_DALS
                                                                 )

        if new_schema_file_path:
            if self.is_have_extended(new_schema_file_path):
                return new_schema_file_path
            else:
                return self.add_extended_to_file_name(new_schema_file_path)
        else:
            return None

    def show_variants_to_delete_node(self):
        message_box = QtGui.QMessageBox()
        message_box.setText(u'Вы действительно хотите удалить выбранный элемент?')
        message_box.setWindowTitle(self.MESSAGE_WARNING)
        message_box.addButton(QtGui.QMessageBox.Yes)
        message_box.addButton(QtGui.QMessageBox.No)
        message_box.setDefaultButton(QtGui.QMessageBox.No)
        variant_select = message_box.exec_()

        if variant_select == QtGui.QMessageBox.Yes:
            return True

        if variant_select == QtGui.QMessageBox.No:
            return False

    def show_variants_to_save_schema(self):
        message_box = QtGui.QMessageBox()
        message_box.setText(self.MESSAGE_ASK_SAVE)
        message_box.setWindowTitle(self.MESSAGE_WARNING)
        message_box.addButton(QtGui.QMessageBox.Yes)
        message_box.addButton(QtGui.QMessageBox.No)
        message_box.addButton(QtGui.QMessageBox.Cancel)
        message_box.setDefaultButton(QtGui.QMessageBox.Yes)
        variant_select = message_box.exec_()

        if variant_select == QtGui.QMessageBox.Yes:
            return self.VARIANT_SAVE_SCHEMA

        if variant_select == QtGui.QMessageBox.No:
            return self.VARIANT_NO_SAVE_SCHEMA

        return self.VARIANT_CANCEL

    def send_system_message(self, title, text):
        message_box = QtGui.QMessageBox()
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.exec_()
