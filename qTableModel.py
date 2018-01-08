from PyQt4.QtCore import *


class QTableModel(QAbstractTableModel):
    def __init__(self, _gui_table, _table):
        QAbstractTableModel.__init__(self)
        self.gui = _gui_table
        self.column_headers = _table.get_name_columns()
        self.cached = _table.get_table()

    # Overriding -------------------------

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.cached)

    def columnCount(self, parent=None, *args, **kwargs):
        if not self.column_headers:
            return

        return len(self.column_headers)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole and role != Qt.EditRole:
            return QVariant()
        value = ''
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.cached[row][col]
        return QVariant(value)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.column_headers[section])
        return QVariant()
