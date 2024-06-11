
TABLE_RECORD = '''

CREATE TABLE IF NOT EXISTS record(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_firstname TEXT NOT NULL,
    chat_id TEXT NOT NULL,
    datee DATE NOT NULL,
    timee TEXT NOT NULL,
    description TEXT NOT NULL
);

'''
