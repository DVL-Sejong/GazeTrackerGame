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

    def is_existing_id(self):
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

        condition = {'id': self.lineEdit_dbid.displayText()}
        count = dbconn.count(table=dbconstant.TABLE, condition=condition)
        dbconn.close()

        return True if count > 0 else False
