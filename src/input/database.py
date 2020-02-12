from operator import eq

from database.lib import MYSQL
import database.constant as dbconstant
from src.exception import Error


class Database:
    def __init__(self, table, lineEdit_dbid, checkBox_dbid):
        self.custom_db_connectivity = False
        self.table = table
        self.lineEdit_dbid = lineEdit_dbid
        self.checkBox_dbid = checkBox_dbid

    def on_cancel_click(self):
        filled = self.is_table_filled()
        if filled is False or self.is_connectable() is False:
            self.table.clearContents()

    def on_apply_click(self):
        error = Error()
        if self.is_table_filled() is not True:
            error.set_message("Not Filled!")
        if self.is_connectable() is False:
            error.set_message("Not Valid Information!")
        return error

    def on_id_apply(self):
        error = Error()
        if self.is_existing_id():
            error.set_message("Duplicated ID!")
        if self.is_valid_id() is not True:
            error.set_message("Not Valid ID!")
            self.lineEdit_dbid.setText("")
        if error.is_true:
            self.checkBox_dbid.setChecked(False)
        return error

    def is_table_filled(self):
        for row in range(5):
            if self.table.item(row, 0) is None:
                self.custom_db_connectivity = False
                return False
        return True

    def is_connectable(self):
        dbconn = MYSQL(
            dbhost=self.table.item(0, 0).text(),
            dbuser=self.table.item(1, 0).text(),
            dbpwd=self.table.item(2, 0).text(),
            dbname=self.table.item(3, 0).text(),
            dbcharset=self.table.item(4, 0).text()
        )

        if dbconn.session() is None:
            dbconn.close()
            self.custom_db_connectivity = False
            return False
        else:
            dbconn.close()
            self.custom_db_connectivity = True
            return True

    def is_valid_id(self):
        if eq(self.lineEdit_dbid.displayText(), "") is True: return False
        if len(self.lineEdit_dbid.displayText()) > 255: return False
        return True

    def get_dbconn(self):
        if self.custom_db_connectivity is True:
            dbconn = MYSQL(
                dbhost=self.table.item(0, 0).text(),
                dbuser=self.table.item(1, 0).text(),
                dbpwd=self.table.item(2, 0).text(),
                dbname=self.table.item(3, 0).text(),
                dbcharset=self.table.item(4, 0).text()
            )
        else:
            dbconn = MYSQL(
                dbhost=dbconstant.HOST,
                dbuser=dbconstant.USER,
                dbpwd=dbconstant.PASSWORD,
                dbname=dbconstant.DB_NAME,
                dbcharset=dbconstant.CHARSET
            )

        return dbconn

    def is_existing_id(self):
        dbconn = self.get_dbconn()

        condition = {'id': self.lineEdit_dbid.displayText()}
        count = dbconn.count(table=dbconstant.TABLE, condition=condition)
        dbconn.close()

        return True if count > 0 else False

    def save(self, data, parser, size):
        dbconn = self.get_dbconn()
        width, height = parser.get_card_size()
        horizontal_margin, vertical_margin = parser.get_margins()

        for i in range(len(data)):
            tuple = {
                'id': data[i].id,
                'status': data[i].status,
                't': self.t_index[i],
                't_order': self.t_order[i],
                'left_x': data[i].left_point.x,
                'left_y': data[i].left_point.y,
                'left_validity': data[i].left_point.validity,
                'right_x': data[i].right_point.x,
                'right_y': data[i].right_point.x,
                'right_validity': data[i].right_point.validity,
                'average_x': data[i].average_point.x,
                'average_y': data[i].average_point.y,
                'average_validity': data[i].average_point.validity,
                'left_pupil_diameter': data[i].left_pupil.diameter,
                'left_pupil_validity': data[i].left_pupil.validity,
                'right_pupil_diameter': data[i].right_pupil.diameter,
                'right_pupil_validity': data[i].right_pupil.validity,
                'average_pupil_diameter': data[i].average_pupil.diameter,
                'average_pupil_validity': data[i].average_pupil.validity,
                'width': size.width(),
                'height': size.height(),
                'card_width': width,
                'card_height': height,
                'card_horizontal_margin': horizontal_margin,
                'card_vertical_margin': vertical_margin
            }

            dbconn.insert(table=dbconstant.TABLE, data=tuple)

