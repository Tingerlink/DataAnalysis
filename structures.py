#!-*-coding:utf-8-*-

import cellTableTypes
import methods


class TableStructure:

    def __init__(self, _name_columns, _table, _data_types=None, _input_param=None):
        self.name_columns = _name_columns
        self.table = _table

        if _input_param:
            self.input_parameters = _input_param
            self.input_user_parameters = _input_param
        else:
            self.input_parameters = self.get_start_input_parameters()
            self.input_user_parameters = self.input_parameters

        if _data_types:
            self.user_column_data_type = _data_types
        else:
            self.user_column_data_type = self.get_column_types()

    def get_cell_type(self, type_column, cell_in_column):
        cell_type = cellTableTypes.get_type(cell_in_column)

        if cell_type > type_column:
            return cell_type

        return type_column

    def update_column_types(self, row, column_types):
        for row_index in range(0, len(row)):
            column_types[row_index] = self.get_cell_type(column_types[row_index], row[row_index])

        return column_types

    def get_start_input_parameters(self):
        return [0 for i in range(self.count_columns())]

    # set --------------------------

    def set_input_user_parameters(self, params):
        self.input_user_parameters = params

    def set_name_columns(self, _name_columns):
        self.name_columns = _name_columns

    def set_name_column_by_id(self, new_name, column_index):
        self.name_columns[column_index] = new_name

    def set_table(self, _table):
        self.table = _table

    def set_input_user_parameter_for_column(self, column_id, new_param):
        self.input_user_parameters[column_id] = new_param

    def set_user_column_data_type_by_id(self, column_index, new_type):
        self.user_column_data_type[column_index] = new_type

    # get --------------------------

    def get_user_column_data_type_by_id(self, column_index):
        return self.user_column_data_type[column_index]

    def get_user_column_data_types(self):
        return self.user_column_data_type

    def get_input_user_parameter_for_column(self, column_id):
        return self.input_user_parameters[column_id]

    def get_enable_input_params_for_column(self, column_id):
        pass

    def get_enable_types_for_column(self, column_id):
        pass

    def get_input_user_parameters(self):
        return self.input_user_parameters

    def get_name_columns(self):
        return self.name_columns

    def get_default_column_name_by_id(self, column_index):
        column_name = u'Атрибут ' + unicode(str(column_index + 1))
        return column_name

    def get_table(self):
        return self.table

    def count_rows(self):
        return len(self.table)

    def count_columns(self):
        if self.name_columns:
            return len(self.name_columns)
        else:
            return 0

    def get_column_types(self):
        column_types = []

        for i in range(0, self.count_columns()):
            column_types.append(0)

        for row in self.get_table():
            column_types = self.update_column_types(row, column_types)

        return column_types

    def get_count_output_columns(self):
        count = 0
        for column_input_param in self.input_user_parameters:
            if column_input_param == 2:
                count += 1

        return count

    def get_count_input_columns(self):
        count = 0
        for column_input_param in self.input_user_parameters:
            if column_input_param == 1:
                count += 1

        return count

    def get_count_info_columns(self):
        count = 0
        for column_input_param in self.input_user_parameters:
            if column_input_param == 0:
                count += 1

        return count

    def get_info_name_columns(self):
        column_names = []

        index = 0
        for column_input_param in self.input_user_parameters:
            if column_input_param == 0:
                column_names.append(self.name_columns[index])
            index += 1

        return column_names

    def get_output_name_columns(self):
        column_names = []

        index = 0
        for column_input_param in self.input_user_parameters:
            if column_input_param == 2:
                column_names.append(self.name_columns[index])
            index += 1

        return column_names

    def get_input_name_columns(self):
        column_names = []

        index = 0
        for column_input_param in self.input_user_parameters:
            if column_input_param == 1:
                column_names.append(self.name_columns[index])
            index += 1

        return column_names


class TableSetStructure:
    def __init__(self, _input_learn_table, _info_learn_table, _output_learn_table, _input_test_table):
        self.input_learn_table = _input_learn_table
        self.info_learn_table = _info_learn_table
        self.output_learn_table = _output_learn_table
        self.input_test_table = _input_test_table

    def get_learn_set(self):
        columns_name_set = self.input_learn_table.get_name_columns()\
                           + self.info_learn_table.get_name_columns()\
                           + self.output_learn_table.get_name_columns()

        input_table_set = []

        for i in range(0, len(self.info_learn_table.table)):
            row_set = self.input_learn_table.table[i]\
                      + self.info_learn_table.table[i]\
                      + self.output_learn_table.table[i]

            input_table_set.append(row_set)

        return TableStructure(columns_name_set, input_table_set)

    def get_test_set(self):
        return self.input_test_table

    def get_input_learn_table(self):
        return self.input_learn_table

    def get_info_learn_table(self):
        return self.info_learn_table

    def get_output_learn_table(self):
        return self.output_learn_table

    def get_input_test_table(self):
        return self.input_test_table


class AnalysisGraph:
    def __init__(self, _id, _data_set):
        self.id = _id
        self.data_set = _data_set
        self.enable = True

    def set_enable(self, status):
        self.enable = status

    def set_id(self, _id):
        self.id = _id

    def get_id(self):
        return self.id

    def get_data_set(self):
        return self.data_set


class AnalyseSetStructure:
    def __init__(self, _result, _id_type_method, _id, _count_true, _count_false):
        self.result = _result
        self.id_type_method = _id_type_method
        self.id = _id
        self.count_true = _count_true
        self.count_false = _count_false
        self.analysis_graphs = []

    # set ----------------------

    def set_id(self, _id):
        self.id = _id

    def add_graph(self, analysis_graph):
        self.analysis_graphs.append(analysis_graph)

    # get ----------------------

    def get_analysis_graph_by_id(self, graph_id):
        for graph in self.analysis_graphs:
            if graph.get_id() == graph_id:
                return graph

    def get_analysis_graphs(self):
        return self.analysis_graphs

    def get_id_type_method(self):
        return self.id_type_method

    def get_id(self):
        return self.id

    def get_result(self):
        return self.result

    def get_method_name(self):
        return methods.get_method_name_by_id(self.id_type_method)

    def get_quality(self):
        return float(float(self.count_true) / float((self.count_true + self.count_false))) * 100


class DataInformationStructure:
    def __init__(self, _name, _file_path, _id):
        self.name = _name
        self.file_path = _file_path
        self.id = _id

    # get -----------------------

    def get_name(self):
        return self.name

    def get_file_path(self):
        return self.file_path

    def get_id(self):
        return self.id

    # set -----------------------

    def set_name(self, _name):
        self.name = _name

    def set_file_path(self, _file_path):
        self.file_path = _file_path

    def set_id(self, _id):
        self.id = _id


class DataStructure:
    def __init__(self, _table_set, _data_info):
        self.table_set = _table_set
        self.data_info = _data_info
        self.analysis_sets = []

    def add_analysis_set(self, analysis_set):
        self.analysis_sets.append(analysis_set)

    def get_analysis_set_by_id(self, _id):
        for analysis_set in self.analysis_sets:
            if analysis_set.get_id() == _id:
                return analysis_set

    def remove_analysis_set_by_id(self, _id):
        for analysis_set in self.analysis_sets:
            if analysis_set.get_id() == _id:
                self.analysis_sets.remove(analysis_set)
                return True

        return False

    def get_analysis_sets(self):
        return self.analysis_sets
