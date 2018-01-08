#!-*-coding:utf-8-*-
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import *

import cellTableTypes
import apiOS
import structures
import excelAdapter
import qTableModel

(Ui_AnalysisMaster, QAnalysisMaster) = uic.loadUiType('gui/analysisMaster.ui')
(Ui_Widget, QImportMaster) = uic.loadUiType('gui/importMaster.ui')


class AnalysisDataMaster(QWizard):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ui = Ui_AnalysisMaster()
        self.ui.setupUi(self)
        self.typeMethods = None

    def get_type_method(self):
        return self.typeMethods

    def set_type_method(self):
        self.typeMethods = self.ui.listWidget.selectedIndexes()[0].row()

    def validateCurrentPage(self):
        if self.currentId() == 0:
            if self.ui.listWidget.selectedIndexes():
                self.set_type_method()
                return True
            else:
                return False

    def __del__(self):
        self.ui = None


class ImportDataMaster(QWizard):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.api = apiOS.ApiOS()

        self.learn_table = None
        self.test_table = None

        self.data_info = structures.DataInformationStructure(None, None, None)
        self.table_data = None
        self.table_set = None

    def __del__(self):
        self.ui = None

    def validateCurrentPage(self):
        if self.currentId() == 0:
            return self.is_valid_page_1()

        if self.currentId() == 1:
            return self.is_valid_page_2()

        if self.currentId() == 2:
            return self.is_valid_page_3()

        if self.currentId() == 3:
            return self.is_valid_page_4()

    def is_valid_page_1(self):
        if self.ui.tbFilePath.text() and self.ui.nameData.text() and self.learn_table:

            self.set_list_item()
            return True
        else:
            return False

    def is_valid_page_2(self):
        count_output_param = self.learn_table.get_count_output_columns()
        count_input_param = self.learn_table.get_count_output_columns()

        if not (count_output_param == 1 and count_input_param >= 1):
            message_text = u'Обучающая выборка должна иметь один или более одного входного атрибута, ' \
                           u'и только один выходной.\n\n Входные атрибуты должны быть числовыми.'
            self.api.send_system_message(u'Предупреждение', message_text)

            return False

        return True

    def is_valid_page_3(self):
        if self.ui.chbEnableTest.checkState() == Qt.Checked:
            input_user_param = self.learn_table.get_input_user_parameters()
            column_names = self.learn_table.get_name_columns()

            new_names = []

            for index_column in range(0, len(input_user_param)):
                    if input_user_param[index_column] == 1:
                        new_names.append(column_names[index_column])


            new_table = []
            for row in self.learn_table.get_table():
                new_row = []
                for index_column in range(0, len(input_user_param)):
                    if input_user_param[index_column] == 1:
                        new_row.append(row[index_column])

                new_table.append(new_row)

            self.test_table = structures.TableStructure(new_names,
                                                        new_table,
                                                        [1 for i in range(0 , len(new_names))],
                                                        [1 for i in range(0 , len(new_names))])

            self.set_table_set()
            self.close()
            return True

        if self.test_table:
            data_type_test_columns = self.test_table.get_column_types()
            count_input_param_in_learn_table = self.learn_table.get_input_user_parameters().count(1)

            if data_type_test_columns.count(cellTableTypes.FLOAT_TYPE) == len(data_type_test_columns):
                if count_input_param_in_learn_table != len(data_type_test_columns):
                    self.api.send_system_message(self.api.MESSAGE_WARNING,
                                                 u'Количество входных атрибутов тестовой выборки должно быть '
                                                 u'равно количеству атрибутов обучающей выборки ['\
                                                 + str(count_input_param_in_learn_table) + u']')
                    return False

                self.set_option_list()

            else:
                self.api.send_system_message(self.api.MESSAGE_WARNING, u'Входные тестовые данные должны быть числовыми')
                return False

        return True

    def is_valid_page_4(self):
        selected_values = self.get_selected_values_from_option_list()
        selected_values.sort()

        if selected_values == [i for i in range(0, self.test_table.count_columns())]:
            self.set_table_set()
            return True
        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING,
                                         u'Не все входные тестовые атрибуты были сопоставленны')

    # All -------------------------------

    def set_pre_view_table_model(self, gui_table, q_model):
        self.clear_pre_view_table(gui_table)
        gui_table.setModel(q_model)

    def clear_pre_view_table(self, gui_table):
        gui_table.setModel(None)

    # Page 1 -----------------------------

    def open_data_file(self, reload_trigger=False):
        try:
            if reload_trigger:
                file_data_path = self.ui.tbFilePath.text()

                if not file_data_path:
                    return True
            else:
                file_data_path = self.api.show_open_data_dialog(self)

            if file_data_path:
                page_for_import = self.ui.spinLoadPage.value() - 1
                starting_row = self.ui.spinRowStart.value() - 1
                is_have_headers = self.ui.chbFirstRowIsHeader.isChecked()

                adapter = excelAdapter.ExcelAdapter()

                self.learn_table = adapter.load_table_set_from_excel(file_data_path,
                                                                     page_for_import,
                                                                     starting_row,
                                                                     is_have_headers)

                q_table_model = qTableModel.QTableModel(self.ui.preViewTable,
                                                        self.learn_table)

                if self.learn_table:
                    self.ui.tbFilePath.setText(file_data_path)
                    self.set_pre_view_table_model(self.ui.preViewTable, q_table_model)

                    return True

            self.clear_pre_view_page_1()
            return False

        except IndexError:
            self.clear_pre_view_page_1()
            return False

    def clear_pre_view_page_1(self):
        self.ui.tbFilePath.setText('')
        self.clear_pre_view_table(self.ui.preViewTable)

    def is_value_row_start_change(self):
        self.open_data_file(True)

    def is_value_page_change(self):
        self.open_data_file(True)

    def is_have_headers(self):
        self.open_data_file(True)

    # Page 2 -----------------------------

    def set_list_item(self):
        column_types = self.learn_table.get_column_types()

        column_index = 0

        self.ui.columnsWidget.clear()

        for column_name in self.learn_table.get_name_columns():
            row = QListWidgetItem()

            row.setText(QString("[" + cellTableTypes.get_name_type(column_types[column_index]) +
                                "] | " + unicode(column_name)))

            row.setIcon(self.get_icon_by_input_param_type(
                self.learn_table.get_input_user_parameter_for_column(column_index)))

            self.ui.columnsWidget.addItem(row)

            column_index += 1

    def set_select_data_type(self, data_type_index):
        self.ui.cb_data_type.setCurrentIndex(data_type_index)

    def set_select_input_param(self, input_param_index):
        self.ui.cb_input_param.setCurrentIndex(input_param_index)

    def set_type_column_in_item_list(self, column_id, new_type):
        column_item_name = u'[' + cellTableTypes.get_name_type(new_type) + u'] | ' \
                           + unicode(self.learn_table.get_name_columns()[column_id])

        self.ui.columnsWidget.item(column_id).setText(QString(column_item_name))

    def set_icon_for_column_in_item_list(self, column_id, input_param):
        self.ui.columnsWidget.item(column_id).setIcon(self.get_icon_by_input_param_type(input_param))

    def is_name_column_change(self):
        index_column = self.ui.columnsWidget.currentRow()
        new_name = self.ui.tbColumnName.text()

        if not new_name or len(new_name) <= 0:
            new_name = self.learn_table.get_default_column_name_by_id(index_column)

        self.learn_table.set_name_column_by_id(new_name, index_column)

        self.set_type_column_in_item_list(index_column, self.learn_table.get_user_column_data_type_by_id(index_column))

    def is_name_column_finished(self):
        self.is_name_column_change()

    def is_list_columns_item_selected(self):
        index = self.ui.columnsWidget.currentRow()
        self.ui.tbColumnName.setText(unicode(self.learn_table.get_name_columns()[index]))

        self.set_select_input_param(self.learn_table.get_input_user_parameter_for_column(index))
        self.set_select_data_type(self.learn_table.get_user_column_data_type_by_id(index))


    def is_data_type_change(self):
        index_column = self.ui.columnsWidget.currentRow()
        index_data_type = self.ui.cb_data_type.currentIndex()
        index_input_param = self.ui.cb_input_param.currentIndex()

        if index_data_type >= self.learn_table.get_column_types()[index_column]:
            if index_input_param == 1:
                if index_data_type == cellTableTypes.FLOAT_TYPE:
                    self.learn_table.set_user_column_data_type_by_id(index_column, index_data_type)
                    self.set_type_column_in_item_list(index_column, index_data_type)
                else:
                    self.api.send_system_message(self.api.MESSAGE_WARNING,
                                                 u"Входной атрибут должен иметь числовой тип")
                    self.set_select_data_type(self.learn_table.get_user_column_data_type_by_id(index_column))
            else:
                self.learn_table.set_user_column_data_type_by_id(index_column, index_data_type)
                self.set_type_column_in_item_list(index_column, index_data_type)

        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING,
                                         u"Для данного атрибута выбранный тип данных не применим")
            self.set_select_data_type(self.learn_table.get_user_column_data_type_by_id(index_column))

    def is_input_param_change(self):
        index_column = self.ui.columnsWidget.currentRow()
        index_input_param = self.ui.cb_input_param.currentIndex()

        if index_input_param == 1:
            if self.learn_table.get_user_column_data_type_by_id(index_column) == cellTableTypes.FLOAT_TYPE:
                self.learn_table.set_input_user_parameter_for_column(index_column, index_input_param)
                self.set_icon_for_column_in_item_list(index_column, index_input_param)
            else:
                self.api.send_system_message(self.api.MESSAGE_WARNING,
                                             u"Входной атрибут должен иметь числовой тип")
                self.ui.cb_input_param.setCurrentIndex(
                    self.learn_table.get_input_user_parameter_for_column(index_column))
        else:
            self.learn_table.set_input_user_parameter_for_column(index_column, index_input_param)
            self.set_icon_for_column_in_item_list(index_column, index_input_param)

    def get_select_input_param(self):
        pass

    def get_icon_by_input_param_type(self, input_param_type):
        if input_param_type == 0:
            return self.get_resource_icon('info')
        if input_param_type == 1:
            return self.get_resource_icon('input')
        if input_param_type == 2:
            return self.get_resource_icon('output')

    def get_resource_icon(self, icon_name):
        return QIcon(":/icons/icons/" + str(icon_name) + ".png")

    # Page 3 -----------------------------

    def open_test_data_file(self, reload_trigger=False):
        try:
            if reload_trigger:
                file_data_path = self.ui.tbFileTestDataPath.text()

                if not file_data_path:
                    return True
            else:
                file_data_path = self.api.show_open_data_dialog(self)

            if file_data_path:
                page_for_import = self.ui.spin_test_load_page.value() - 1
                starting_row = self.ui.spin_test_row_start.value() - 1
                is_have_headers = self.ui.chb_test_first_row_is_header.isChecked()

                adapter = excelAdapter.ExcelAdapter()

                self.test_table = adapter.load_table_set_from_excel(file_data_path,
                                                                    page_for_import,
                                                                    starting_row,
                                                                    is_have_headers)

                q_test_table_model = qTableModel.QTableModel(self.ui.preViewTestTable,
                                                             self.test_table)

                if self.test_table:
                    self.ui.tbFileTestDataPath.setText(file_data_path)
                    self.set_pre_view_table_model(self.ui.preViewTestTable, q_test_table_model)

                    return True

            self.clear_pre_view_page_3()
            return False

        except IndexError:
            self.clear_pre_view_page_3()
            return False

    def clear_pre_view_page_3(self):
        self.ui.tbFileTestDataPath.setText('')
        self.clear_pre_view_table(self.ui.preViewTestTable)

    def is_test_value_row_start_change(self):
        self.open_test_data_file(True)

    def is_test_value_page_change(self):
        self.open_test_data_file(True)

    def is_test_have_headers(self):
        self.open_test_data_file(True)

    def is_test_enable(self):
        if self.ui.chbEnableTest.checkState() == Qt.Checked:
            self.ui.testWidget.setEnabled(False)
        else:
            self.ui.testWidget.setEnabled(True)

    # Page 4 -----------------------------

    def set_option_list(self):

        count_input_param_in_learn_table = self.learn_table.get_input_user_parameters().count(1)
        count_input_param_in_test_table = self.test_table.count_columns()

        self.ui.testForLearnColumns.setColumnCount(1)

        table_headers = [u'Тестовая выборка']

        self.ui.testForLearnColumns.setHorizontalHeaderLabels(table_headers)
        self.ui.testForLearnColumns.setColumnWidth(0, 280)

        self.ui.testForLearnColumns.setRowCount(count_input_param_in_learn_table)
        self.ui.testForLearnColumns.setVerticalHeaderLabels(self.learn_table.get_input_name_columns())

        for index in range(count_input_param_in_test_table):
            cb_with_test_column = QComboBox()
            for item in self.test_table.get_name_columns():
                cb_with_test_column.addItem(item)

            self.ui.testForLearnColumns.setCellWidget(index, 0, cb_with_test_column)

    def get_selected_values_from_option_list(self):
        selected_values = []
        for i in range(self.test_table.count_columns()):
            cb_next = self.ui.testForLearnColumns.cellWidget(i, 0)
            selected_values.append(cb_next.currentIndex())

        return selected_values

    def set_table_set(self):
        if self.test_table and self.learn_table:
            columns_type = self.learn_table.get_user_column_data_types()
            input_params = self.learn_table.get_input_user_parameters()

            info_table = []
            input_table = []
            output_table = []

            for row in self.learn_table.get_table():
                input_row = []
                output_row = []
                info_row = []

                index_cell = 0
                for cell in row:
                    if input_params[index_cell] == 0:
                        info_row.append(cell)
                    if input_params[index_cell] == 1:
                        input_row.append(cell)
                    if input_params[index_cell] == 2:
                        output_row.append(cell)
                    index_cell += 1

                info_table.append(info_row)
                input_table.append(input_row)
                output_table.append(output_row)

            info_table_headers = []
            input_table_headers = []
            output_table_headers = []

            info_table_data_types = []
            input_table_data_types = []
            output_table_data_types = []

            info_table_input_param = []
            input_table_input_param = []
            output_table_input_param = []

            column_headers = self.learn_table.get_name_columns()

            index = 0
            for input_param in input_params:
                if input_param == 0:
                    info_table_headers.append(column_headers[index])
                    info_table_data_types.append(columns_type[index])
                    info_table_input_param.append(input_param)

                if input_param == 1:
                    input_table_data_types.append(columns_type[index])
                    input_table_headers.append(column_headers[index])
                    input_table_input_param.append(input_param)

                if input_param == 2:
                    output_table_data_types.append(columns_type[index])
                    output_table_input_param.append(input_param)
                    output_table_headers.append(column_headers[index])

                index += 1

            info_data_structure = structures.TableStructure(info_table_headers,
                                                            info_table,
                                                            info_table_data_types,
                                                            info_table_input_param)

            input_data_structure = structures.TableStructure(input_table_headers,
                                                             input_table,
                                                             input_table_data_types,
                                                             input_table_input_param)

            output_data_structure = structures.TableStructure(output_table_headers,
                                                              output_table,
                                                              output_table_data_types,
                                                              output_table_input_param)

            if self.ui.chbEnableTest.checkState() != Qt.Checked:

                not_moving_test_table = self.test_table.get_table()

                moving_test_table = []
                for i in range(0, self.test_table.count_rows()):
                    moving_row = []
                    for j in self.get_selected_values_from_option_list():
                        moving_row.append(not_moving_test_table[i][j])

                    moving_test_table.append(moving_row)

                test_data_structure = structures.TableStructure(input_table_headers,
                                                                moving_test_table,
                                                                [1 for i in range(0, self.test_table.count_columns())],
                                                                [1 for i in range(0, self.test_table.count_columns())])
            else:
                test_data_structure = self.test_table

            self.table_set = structures.TableSetStructure(input_data_structure,
                                                          info_data_structure,
                                                          output_data_structure,
                                                          test_data_structure)

            self.data_info.set_file_path(self.ui.tbFilePath.text())
            self.data_info.set_name(self.ui.nameData.text())

            self.table_data = structures.DataStructure(self.table_set, self.data_info)
