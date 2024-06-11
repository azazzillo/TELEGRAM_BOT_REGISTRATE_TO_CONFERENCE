from database.database import DB, Record


def get_my_records(data: str) -> int:

    db: DB = DB()

    result = db.my_record(data=data)

    if result ==  0:
        return 0
    
    return result