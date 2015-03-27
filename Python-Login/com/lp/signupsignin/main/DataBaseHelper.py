import psycopg2

__author__ = 'manarPC'

class DataBaseHelper:
    conn_string = "host='localhost' dbname='ASAL_AUD' user='postgres' password='123'"
    __connection = None
    cursor = None

    def __init__(self):
        self.__connection = psycopg2.connect(self.conn_string)

    def Connection(self):
        return self.__connection

    def Cursor(self):
        return self.__connection.cursor()