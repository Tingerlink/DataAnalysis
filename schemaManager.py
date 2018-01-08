#!-*-coding:utf-8-*-
import pickle
import schema
import copy


def get_new_schema(data_schema, schema_file_path):
    return schema.Scheme(data_schema, schema_file_path)


def save_schema_in_file(active_schema, file_path):
    try:
        pickle_schema = copy.deepcopy(active_schema)
        output_file = open(file_path, 'wb')
        pickle.dump(pickle_schema, output_file, 2)

        output_file.close()

        return True
    except IndexError:
        return False


def load_schema_from_file(file_path):
    try:
        input_file = open(file_path, 'rb')
        active_scheme = pickle.load(input_file)
        active_scheme.set_file_path(file_path)
        input_file.close()

        return active_scheme
    except IndexError:
        return None
