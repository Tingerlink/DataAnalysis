#!-*-coding:utf-8-*-
import xlrd
import structures


class ExcelAdapter:
    DEFAULT_COLUMN_NAME = u'Атрибут'

    def __init__(self):
        pass

    def load_table_set_from_excel(self, file_path, index_page, start_row, is_have_headers):
        try:
            excel_file = xlrd.open_workbook(unicode(file_path), formatting_info=False)

            if len(excel_file.sheets()) > index_page:
                excel_sheet = excel_file.sheet_by_index(index_page)
            else:
                excel_sheet = excel_file.sheet_by_index(len(excel_file.sheets()) - 1)

            load_table = []
            load_table_headers = None

            index = 0

            for row in range(excel_sheet.nrows):
                if is_have_headers and index == 0:
                    load_table_headers = excel_sheet.row_values(row)
                else:
                    if start_row <= index:
                        load_table.append(excel_sheet.row_values(row))
                index += 1

            if not is_have_headers:
                load_table_headers = []

                for i in range(0, len(load_table[0])):
                    column_name = self.DEFAULT_COLUMN_NAME + u' ' + str(i)
                    load_table_headers.append(column_name)

            table_set = structures.TableStructure(load_table_headers, load_table)

            return table_set

        except IndexError:
            return None