from datetime import datetime
from operator import eq

from database.lib import MYSQL
import database.constant as dbconstant
from src.exception import Error
from src.game.status import Status


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

    def get_id(self):
        if self.checkBox_dbid.isChecked() is not True:
            return datetime.now().strftime("%y%m%d%H%M%S")
        if self.is_valid_id():
            return self.lineEdit_dbid.displayText()

    def is_existing_id(self):
        dbconn = self.get_dbconn()

        condition = {'id': self.lineEdit_dbid.displayText()}
        count = dbconn.count(table=dbconstant.TABLE, condition=condition)
        dbconn.close()

        return True if count > 0 else False

    def save(self, result, parser):
        dbconn = self.get_dbconn()
        width, height = parser.get_card_size()
        horizontal_margin, vertical_margin = parser.get_margins()
        id = self.get_id()

        for count in range(len(result.ranges)):
            start, end = result.ranges[count]
            t_index = result.t_index[count]
            t_order = result.t_order[count]

            if result.data[start].status != Status.PUPIL and \
                    result.data[start].status != Status.SEQUENCE and \
                    result.data[start].status != Status.GAME:
                continue

            for i in range(start, end):
                tuple = {
                    'id': id,
                    'status': result.data[i].status.value,
                    't': t_index[i - start],
                    't_order': t_order[i - start],
                    'left_x': result.data[i].left_point.x,
                    'left_y': result.data[i].left_point.y,
                    'left_validity': result.data[i].left_point.validity,
                    'right_x': result.data[i].right_point.x,
                    'right_y': result.data[i].right_point.x,
                    'right_validity': result.data[i].right_point.validity,
                    'average_x': result.data[i].average_point.x,
                    'average_y': result.data[i].average_point.y,
                    'average_validity': result.data[i].average_point.validity,
                    'left_pupil_diameter': result.data[i].left_pupil.diameter,
                    'left_pupil_validity': result.data[i].left_pupil.validity,
                    'right_pupil_diameter': result.data[i].right_pupil.diameter,
                    'right_pupil_validity': result.data[i].right_pupil.validity,
                    'average_pupil_diameter': result.data[i].average_pupil.diameter,
                    'average_pupil_validity': result.data[i].average_pupil.validity,
                    'width': result.data[i].screen_size.width,
                    'height': result.data[i].screen_size.height,
                    'card_width': width,
                    'card_height': height,
                    'card_horizontal_margin': horizontal_margin,
                    'card_vertical_margin': vertical_margin,
                    'is_wandering': 1 if result.data[i].is_wandering else 0
                }

                dbconn.insert(table=dbconstant.TABLE, data=tuple)

