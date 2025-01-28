import sqlite3
from pathlib import Path
from typing import List, Tuple

from root import ROOT
from src.news.news import News



root = Path(ROOT)

class ArchiveManager:
    @staticmethod
    def create_archive():
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                header TEXT,
                text TEXT,
                author TEXT,
                date VARCHAR(30),
                time VARCHAR(30)
            )
            """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def put_to_archive(news: News):
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO Archive (header, text, author, date, time)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(
            insert_query,
            (
                news.header or None,
                news.text or None,
                news.author or None,
                news.date or None,
                news.time or None
            )
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_archive() -> List[Tuple[int, News]]:
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT id, header, text, author, date, time FROM Archive")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            news = News(
                header=row[1],
                text=row[2],
                author=row[3],
                date=row[4],
                time=row[5]
            )
            result.append((row[0], news))

        conn.close()
        return result


if __name__ == "__main__":
    print("Archive... ", end="")
    ArchiveManager.create_archive()
    print("OK")
