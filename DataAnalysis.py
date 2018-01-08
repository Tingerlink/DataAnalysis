#!-*-coding:utf-8-*-
import sys
import os

import apiOS
import interface
import analysisMethods
import qTableModel
import masters
import structures
import methods

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure

(Ui_MainWindow, QMainWindow) = uic.loadUiType('gui/mainWindow.ui')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ActiveScheme = None

        self.api = apiOS.ApiOS()
        self.message = interface.StatusMessage()

        interface.set_program_status(self, self.message.get_message_text(self.message.FILE_PROJECT_NO_SELECT))

    def __del__(self):
        self.ui = None

    # Tab controls ------------------------------------

    def concat_tables(self, first, second):
        columns_name_set = first.get_name_columns() + second.get_name_columns()

        table_set = []

        for i in range(0, first.count_rows()):
            row_set = first.table[i] + [unicode(str(second.table[i][0]))]

            table_set.append(row_set)

        return structures.TableStructure(columns_name_set, table_set)

    def clear_tab_control(self):
        self.ui.tabWidget.deleteLater()
        self.ui.tabWidget = QTabWidget(self.ui.widget_2)
        self.ui.horizontalLayout.addWidget(self.ui.tabWidget)

    def add_data_views_by_id(self, data_id):
        if not self.ActiveScheme:
            return False

        data = self.ActiveScheme.get_data_by_id(data_id)
        name = data.data_info.get_name()

        learn_set = data.table_set.get_learn_set()
        test_set = data.table_set.get_test_set()

        table_learn = QTableView()
        table_test = QTableView()

        q_model_learn = qTableModel.QTableModel(table_learn, learn_set)
        q_model_test = qTableModel.QTableModel(table_test, test_set)

        table_learn.setModel(q_model_learn)
        table_test.setModel(q_model_test)

        self.ui.tabWidget.addTab(table_learn, u'Обучающая выборка (' + name + u')')
        self.ui.tabWidget.addTab(table_test, u'Тестовая выборка (' + name + u')')

    def add_analysis_table_views_by_id(self, analysis_id, data_id):
        if not self.ActiveScheme:
            return False

        data = self.ActiveScheme.get_data_by_id(data_id)

        test_set = data.table_set.get_input_test_table()
        result_set = data.get_analysis_set_by_id(analysis_id).get_result()

        method_name = data.get_analysis_set_by_id(analysis_id).get_method_name()
        data_name = data.data_info.get_name()

        output_test_table = self.concat_tables(test_set, result_set)

        result_table = QTableView()

        q_result = qTableModel.QTableModel(result_table, output_test_table)

        result_table.setModel(q_result)

        self.ui.tabWidget.addTab(result_table, u'Результат анализа (' + method_name + u') [' + data_name + u']')

    # Tree Schema Events -------------------------------

    def clear_tree_schema(self):
        self.ui.treeSchema.clear()

    def set_project_node_in_tree_schema(self):
        new_root_item = QTreeWidgetItem(self.ui.treeSchema)
        if not self.ActiveScheme:
            return False

        new_root_item.setIcon(0, QIcon(":/icons/icons/project.png"))
        new_root_item.setText(0, self.ActiveScheme.get_file_path())

        new_root_item.setData(0, Qt.UserRole, QVariant([0, 'Root']))

        self.ui.treeSchema.addTopLevelItem(new_root_item)

    def add_graph_range_in_analysis_tree_item(self, analysis_item, graph_range):
        for graph in graph_range:
            if graph.enable:
                new_analysis_graph_item = QTreeWidgetItem(analysis_item)

                graph_title = graph.get_data_set()[1][0] + ' x ' + graph.get_data_set()[1][1]

                new_analysis_graph_item.setText(0, unicode(graph_title))
                new_analysis_graph_item.setIcon(0, QIcon(":/icons/icons/graph.png"))
                new_analysis_graph_item.setData(0, Qt.UserRole,QVariant([graph.get_id(), 'Graph']))

                analysis_item.addChild(new_analysis_graph_item)

    def add_analysis_range_in_data_tree_item(self, data_item, analysis_range):
        for analysis in analysis_range:
            new_analysis_item = QTreeWidgetItem(data_item)

            analysis_title = analysis.get_method_name() + u' (' + unicode(round(analysis.get_quality(), 2)) + u'%)'

            new_analysis_item.setText(0, analysis_title)
            new_analysis_item.setIcon(0, QIcon(":/icons/icons/analysis.png"))
            new_analysis_item.setData(0, Qt.UserRole, QVariant([analysis.get_id(), 'Analysis']))

            data_item.addChild(new_analysis_item)

            self.add_graph_range_in_analysis_tree_item(new_analysis_item, analysis.get_analysis_graphs())

    def add_data_range_in_project_item(self, project_item, data_range):
        if not data_range:
            return True

        for data in data_range:
            new_data_item = QTreeWidgetItem(project_item)

            new_data_item.setText(0, data.data_info.get_name())
            new_data_item.setIcon(0, QIcon(":/icons/icons/data.png"))
            new_data_item.setData(0, Qt.UserRole, QVariant([data.data_info.get_id(), 'Data']))

            project_item.addChild(new_data_item)

            self.add_analysis_range_in_data_tree_item(new_data_item, data.get_analysis_sets())

    def update_tree_schema(self):
        if not self.ActiveScheme:
            return False

        self.clear_tree_schema()

        self.set_project_node_in_tree_schema()
        self.add_data_range_in_project_item(self.ui.treeSchema.topLevelItem(0), self.ActiveScheme.data)

        self.ui.treeSchema.expandAll()

    def get_id_item_tree(self, item):
        return item.data(0, Qt.UserRole).toList()[0].toInt()[0]

    def get_type_item_tree(self, item):
        return item.data(0, Qt.UserRole).toList()[1].toString()

    def is_select_tree_schema_item(self):
        if not self.ActiveScheme:
            return True

        item = self.ui.treeSchema.currentItem()
        item_id = self.get_id_item_tree(item)
        item_type = self.get_type_item_tree(item)

        if 'Root' == item_type:
            self.clear_tab_control()

        if not self.ActiveScheme.data or len(self.ActiveScheme.data) == 0:
            return True

        if 'Data' == item_type:
            self.clear_tab_control()
            self.add_data_views_by_id(item_id)

        if 'Analysis' == item_type:
            self.clear_tab_control()
            data_parent = item.parent()
            data_parent_id = self.get_id_item_tree(data_parent)
            self.add_analysis_table_views_by_id(item_id, data_parent_id)

        if 'Graph' == item_type:
            self.clear_tab_control()

            graph_id = item_id

            graph = self.ActiveScheme.get_graph_by_id(graph_id)
            self.create_graph_tap(graph.get_data_set())

    def delete_item_tree(self):
        current_item = self.ui.treeSchema.currentItem()

        if not current_item:
            return True

        event = self.api.show_variants_to_delete_node()

        if not event:
            return True

        type_item = self.get_type_item_tree(current_item)
        id_item = self.get_id_item_tree(current_item)

        if type_item == 'Graph':
            self.ActiveScheme.get_graph_by_id(id_item).set_enable(False)

        if type_item == 'Analysis':
            self.ActiveScheme.remove_analysis_by_id(id_item)

        if type_item == 'Data':
            self.ActiveScheme.remove_data_by_id(id_item)

        self.ui.treeSchema.setCurrentItem(self.ui.treeSchema.topLevelItem(0))

        self.update_tree_schema()

    def create_graphs(self):
        current_item = self.ui.treeSchema.currentItem()

        if not current_item:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для визуализации данных необходимо'
                                                                   u' выбрать результат анализа')

            return True

        type_item = self.get_type_item_tree(current_item)
        id_item = self.get_id_item_tree(current_item)

        if type_item == 'Analysis':
            for graph in self.ActiveScheme.get_analysis_by_id(id_item).get_analysis_graphs():
                graph.set_enable(True)

            self.ui.treeSchema.setCurrentItem(self.ui.treeSchema.topLevelItem(0))

            self.update_tree_schema()
        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для визуализации данных необходимо'
                                                                   u' выбрать результат анализа')

    # Window Operations ----------------------------

    def update_window_title(self):
        if self.ActiveScheme:
            interface.set_title_main_window(self, unicode(interface.PROGRAM_NAME + self.ActiveScheme.get_file_path()))

    def set_window_default_title(self):
        interface.set_title_main_window(self, unicode(interface.PROGRAM_NAME))

    # Tools Schema Events -----------------------

    def master_import_data(self):
        if self.ActiveScheme:
            master = masters.ImportDataMaster(self)
            master.exec_()

            if master.table_data:
                master.data_info.set_id(self.ActiveScheme.get_next_id())
                self.ActiveScheme.add_data(master.table_data)

                interface.set_program_status(self, u"Данные успешно импортированны")
                self.update_tree_schema()
        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для импорта данных необходимо открыть проект')

    def master_export_data(self):
        pass

    def master_analysis_data(self):
        if not self.ActiveScheme:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для анализа необходимо выбрать набор данных')
            return False

        item = self.ui.treeSchema.currentItem()
        if item:
            item_type = self.get_type_item_tree(item)
        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для анализа необходимо выбрать набор данных')
            return False

        if item_type == 'Data':
            data_id = self.get_id_item_tree(item)

            analysis_master = masters.AnalysisDataMaster(self)
            analysis_master.exec_()

            type_method = analysis_master.get_type_method()

            if type_method >= 0:
                self.start_analysis(data_id, type_method)

                self.update_tree_schema()

        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для анализа необходимо выбрать набор данных')

    # Graph analysis ------------------------------

    def create_graph_tap(self, graph_set):
        graph_tab = QWidget()
        dpi = 72
        graph = Figure((18.0, 8.0), dpi=dpi, facecolor='w')

        canvas = FigureCanvas(graph)
        canvas.setParent(graph_tab)

        graph_area = graph.add_subplot(111)
        graph_toolbar = NavigationToolbar2QT(canvas, graph_tab)

        graph_area.grid(True)

        vertical_layout_tab = QVBoxLayout()
        vertical_layout_tab.addWidget(canvas)
        vertical_layout_tab.addWidget(graph_toolbar)

        graph_tab.setLayout(vertical_layout_tab)

        graph_name = graph_set[1][0] + ' x ' + graph_set[1][1]

        graph_area.set_title((graph_name), size=14, family='verdana')

        graph_area.set_xlabel((graph_set[1][0]), family='verdana')
        graph_area.set_ylabel((graph_set[1][1]), family='verdana')

        self.ui.tabWidget.addTab(graph_tab, graph_name)

        legends = []

        for plot in graph_set[0]:
            x = plot[0]
            y = plot[1]
            label_legend = plot[2]

            graph_area.plot(x, y, linestyle='', marker='o', label=label_legend)

            legends.append(label_legend)

        graph_area.legend(legends)

        canvas.draw()

    # Analysis ------------------------------------

    def start_method_analysis(self, type_method):
        if not self.ActiveScheme:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для анализа необходимо выбрать набор данных')
            return False

        item = self.ui.treeSchema.currentItem()
        item_type = None

        if item:
            item_type = self.get_type_item_tree(item)

        if item_type == 'Data':
            data_id = self.get_id_item_tree(item)

            self.start_analysis(data_id, type_method)

            self.update_tree_schema()
        else:
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Для анализа необходимо выбрать набор данных')
            return False

    def add_analysis_in_data(self, output_vector, type_method, name_output_columns, data, analysis_id):
        if output_vector:
            output_vector_table = structures.TableStructure(name_output_columns, output_vector[0])

            analysis_set = structures.AnalyseSetStructure(output_vector_table,
                                                          type_method,
                                                          analysis_id,
                                                          output_vector[1],
                                                          output_vector[2])

            data.add_analysis_set(analysis_set)
            return True

        return False

    def start_analysis(self, data_id, type_method):
        data = self.ActiveScheme.get_data_by_id(data_id)

        learn_set = [data.table_set.get_input_learn_table().get_table(),
                     data.table_set.get_output_learn_table().get_table()]

        test_set = [data.table_set.get_input_test_table().get_table()]

        name_output_columns = data.table_set.get_output_learn_table().get_name_columns()

        output_vector = None

        if type_method == 0:
            output_vector = analysisMethods.naive_bayes_classifier(learn_set, test_set)
        if type_method == 1:
            output_vector = analysisMethods.SVM(learn_set, test_set)
        if type_method == 2:
            output_vector = analysisMethods.classification_tree(learn_set, test_set)
        if type_method == 3:
            output_vector = analysisMethods.nearest_neighbors_classification(learn_set, test_set)

        analysis_id = self.ActiveScheme.get_next_id()
        if self.add_analysis_in_data(output_vector, type_method, name_output_columns,
                                     data,
                                     analysis_id):

            graph_sets = self.ActiveScheme.get_graph_sets_by_analysis_id(data_id, analysis_id)

            for graph_set in graph_sets:
                self.ActiveScheme.get_analysis_by_id(analysis_id).\
                    add_graph(structures.AnalysisGraph(self.ActiveScheme.get_next_id(), graph_set))

            interface.set_program_status(self, u'Анализ выполнен', methods.get_method_name_by_id(type_method))
        else:
            interface.set_program_status(self, u'Анализ не выполнен', methods.get_method_name_by_id(type_method))
            self.api.send_system_message(self.api.MESSAGE_WARNING, u'Не удалось выполнить анализ')

    # MainMenu Schema Events -----------------------

    def new_project(self):
        self.ActiveScheme = interface.create_new_schema(self, self.ActiveScheme)
        if self.ActiveScheme:
            self.clear_tab_control()
            self.update_window_title()
            self.update_tree_schema()

    def open_project(self):
        self.ActiveScheme = interface.open_schema(self, self.ActiveScheme)
        if self.ActiveScheme:
            self.clear_tab_control()
            self.update_window_title()
            self.update_tree_schema()

    def save_project(self):
        interface.save_schema(self, self.ActiveScheme)
        self.update_window_title()

    def save_project_as(self):
        interface.save_schema_as(self, self.ActiveScheme)
        self.update_window_title()

    def close_project(self):
        self.ActiveScheme = interface.close_schema(self, self.ActiveScheme)
        if not self.ActiveScheme:
            self.set_window_default_title()
            self.clear_tab_control()
            self.clear_tree_schema()

    def close_program(self):
        self.ActiveScheme = interface.close_schema(self, self.ActiveScheme)
        if not self.ActiveScheme:
            self.clear_tab_control()
            self.clear_tree_schema()

            self.close()

    def naive_bayes_classifier(self):
        self.start_method_analysis(0)

    def cvm(self):
        self.start_method_analysis(1)

    def classification_tree(self):
        self.start_method_analysis(2)

    def nearest_neighbors_classification(self):
        self.start_method_analysis(3)


if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName(interface.PROGRAM_NAME)

    # create widget
    w = MainWindow()
    w.setWindowTitle(interface.PROGRAM_NAME)
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())
