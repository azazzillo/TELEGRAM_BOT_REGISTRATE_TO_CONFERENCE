from database.database import DB, Record


def get_all_records() -> int:

    db: DB = DB()

    result = db.all_record()
    
    return result