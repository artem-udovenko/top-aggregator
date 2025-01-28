import sqlite3
from pathlib import Path
from typing import Tuple, List

from root import ROOT
from src.smtp.user import User

root = Path(ROOT)

class UsersManager:
    @staticmethod
    def create_users():
        conn = sqlite3.connect(str(root / "src" / "smtp" / "smtp.db"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Surname TEXT,
                Name TEXT,
                Patronymic TEXT,
                email TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def add_to_users(user: User):
        conn = sqlite3.connect(str(root / "src" / "smtp" / "smtp.db"))
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO Users (Surname, Name, Patronymic, email)
            VALUES (?, ?, ?, ?)
            """

        cursor.execute(
            insert_query,
            (
                user.surname or None,
                user.name or None,
                user.patronymic or None,
                user.email or None,
            )
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_users() -> List[Tuple[int, User]]:
        conn = sqlite3.connect(str(root / "src" / "smtp" / "smtp.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT id, Surname, Name, Patronymic, email FROM Users")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            user = User(
                surname=row[1],
                name=row[2],
                patronymic=row[3],
                email=row[4],
            )
            result.append((row[0], user))

        conn.close()
        return result

    @staticmethod
    def remove_from_users(id: int):
        conn = sqlite3.connect(str(root / "src" / "smtp" / "smtp.db"))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_emails():
        conn = sqlite3.connect(str(root / "src" / "smtp" / "smtp.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Users")
        rows = cursor.fetchall()
        result = [row[0] for row in rows]
        conn.close()
        return result


if __name__ == "__main__":
    UsersManager.create_users()
