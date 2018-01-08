#!-*-coding:utf-8-*-
from PyQt4.QtCore import *

import math


class MetaForTreeSchema:
    def __init__(self, _id, _type_schema_node):

        self.id = _id
        self.type_schema_node = _type_schema_node

    def get_q_variant(self):
        q_variant = [self.id, self.type_schema_node]

        return QVariant(q_variant)

    def get_id(self):
        return self.id

    def get_type_schema_node(self):
        return self.type_schema_node


class Scheme:
    def __init__(self, _scheme_data=None, _file_path=None):
        self.data = _scheme_data
        self.file_path = _file_path

        self.next_id = 0

    def get_next_id(self):
        self.next_id += 1
        return self.next_id

    def get_file_path(self):
        return self.file_path

    def get_data_by_id(self, id_data):
        for data_set in self.data:
            if data_set.data_info.get_id() == id_data:
                return data_set

    def get_analysis_by_id(self, id_analysis):
        for data_set in self.data:
            analysis_set = data_set.get_analysis_set_by_id(id_analysis)
            if analysis_set:
                return analysis_set

        return None

    def get_graph_by_id(self, id_graph):
        for data_set in self.data:
            for analysis_set in data_set.get_analysis_sets():
                graph = analysis_set.get_analysis_graph_by_id(id_graph)
                if graph:
                    return graph
        return None

    def add_analysis_set_to_data(self, analysis_set, id_data):
        self.get_data_by_id(id_data).add_analysis_set(analysis_set)

    def add_data(self, _data):
        if self.data:
            self.data.append(_data)
        else:
            self.data = [_data]

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_graph_sets_by_analysis_id(self, id_data, id_analysis):
        data = self.get_data_by_id(id_data)
        analysis = self.get_analysis_by_id(id_analysis)

        column_names = data.table_set.get_input_learn_table().get_name_columns()
        input_test_table = data.table_set.get_input_test_table().get_table()
        output_table = analysis.get_result().get_table()

        unique_output_values = []

        for k in output_table:
            if not k[0] in unique_output_values:
                unique_output_values.append(k[0])

        count_columns = len(input_test_table[0])
        count_graph = math.factorial(count_columns) / math.factorial((count_columns - 2)) / 2

        index_i = 0
        index_j = 1

        all_sets = []
        for i in range(0, count_graph):

            set_dict = dict()

            for item in unique_output_values:
                set_dict[item] = [[], []]

            for index_row in range(0, len(input_test_table)):
                unique_name = unicode(output_table[index_row][0])
                set_dict[unique_name][0].append(input_test_table[index_row][index_i])
                set_dict[unique_name][1].append(input_test_table[index_row][index_j])

            name_x = column_names[index_i]
            name_y = column_names[index_j]

            all_sets.append([set_dict, name_x, name_y])

            if index_j < count_columns - 1:
                index_j += 1
            else:
                index_i += 1
                index_j = index_i + 1

        graph_sets = []

        for table_set in all_sets:
            all_plot = []
            for item in unique_output_values:
                x = table_set[0][item][0]
                y = table_set[0][item][1]
                _class = item
                all_plot.append([x, y, _class])

            graph_sets.append([all_plot, [table_set[1], table_set[2]]])

        return graph_sets

    def remove_analysis_by_id(self, id_analysis):
        for data_set in self.data:
            if data_set.remove_analysis_set_by_id(id_analysis):
                return True

        return False

    def remove_data_by_id(self, id_data):
        for data_set in self.data:
            if data_set.data_info.get_id() == id_data:
                self.data.remove(data_set)

                if len(self.data) <= 0:
                    self.data = None
                return True
        return False
