import sqlite3
import datetime

from settings.database_sql import TABLE_RECORD
from typing import NamedTuple


class Record(NamedTuple):
    user_firstname: str
    chat_id: str
    datee: str
    timee: str
    description: str


class DB:
    def __init__(self) -> None:
        self.basename = "sqlite.bd"
        self.connection = sqlite3.connect(self.basename)
        self.cursor = self.connection.cursor()

        self.create_all_tables(
            TABLE_RECORD
        )
    
    def execute(self, query: str,is_commit: int = 0):
        try:
            result = self.cursor.execute(query)
            if is_commit == 1:
                self.connection.commit()
            else:
                return result.fetchall()
        except sqlite3.Error as e:
            print(f"ERRRRRROR AAAAAAAAAAAA {e}")
    
    def create_all_tables(self, *tables: list[str]):
        for table in tables:
            self.execute(query=table, is_commit=1)


    # Регистрация на конференцию
    def registrate(self, data:Record):
        print("РЕГИСТРАЦИЯ В ДБ")
        print(data)
        record_exists = self.execute(
            query=f'''
                SELECT id FROM record
                WHERE chat_id='{data.chat_id}'
                AND
                datee='{data.datee}' 
            '''
        )
        print(record_exists)
        if len(record_exists) > 0:
            return 1
        
        result = self.execute(
            query=f'''
                INSERT INTO record (user_firstname, chat_id, datee, timee, description)
                VALUES
                ('{data.user_firstname}', '{data.chat_id}', '{data.datee}', '{data.timee}', '{data.description}');
            ''',
            is_commit=1
        )
        print(result)

        return 0
    
    # Конференции, на которые записан пользователь 
    def my_record(self, data:str):
        my_r = self.execute(
            query=f'''
            SELECT * FROM record
            WHERE chat_id='{data}'
        '''
        )
        if len(my_r) <= 0:
            return 1
        return my_r
    

    def all_record(self):
        print("AAAAAALLLLL")
        record = self.execute(
            query=f'''
            SELECT * FROM record
        '''
        )

        return record
        


