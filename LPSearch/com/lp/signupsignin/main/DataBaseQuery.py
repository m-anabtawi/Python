from django.core.management.base import NoArgsCommand
from psycopg2._json import Json

__author__ = 'manarPC'
import DataBaseHelper


class DataBaseQuery:

    dbh = None
    connection = None
    cursor = None

    def __init__(self):
        self.dbh = DataBaseHelper.DataBaseHelper()
        self.connection = self.dbh.Connection()
        self.cursor = self.connection.cursor()

    def SelectImage(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT data->>'image' FROM users WHERE data->>'email'= (%s) AND data->>'password'=(%s)", (email, password))
        return cursor

    def SelectUser(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT exists (SELECT 1 FROM users WHERE data->>'email'=(%s) LIMIT 1)", (email,))
        return cursor

    def InsertUser(self, email, password, userName, userImage):
       cursor = self.connection.cursor()
       connection = self.connection
       cursor.execute("INSERT INTO users (data) VALUES (%s)", [Json({'password': password, 'name': userName, 'email': email, 'image':userImage })])
       connection.commit()

    def SelectUserId(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE data->>'email'= (%s) AND data->>'password'=(%s)", (email, password))
        return cursor