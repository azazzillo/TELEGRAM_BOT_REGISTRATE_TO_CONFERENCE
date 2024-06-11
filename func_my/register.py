from database.database import DB, Record


def registrate(data: dict) -> int:
    print("REGISTRATION ПРОИСХОДИТ")

    rec = Record(
        user_firstname=data.get("user_firstname"),
        chat_id=data.get("chat_id"),
        datee=data.get("datee"),
        timee=data.get("timee"),
        description=data.get("description")
    )
    db: DB = DB()

    result_of_registration = db.registrate(data=rec)

    if isinstance(result_of_registration, int):
        if result_of_registration == 0:
            return 0
        return 1
    return 1