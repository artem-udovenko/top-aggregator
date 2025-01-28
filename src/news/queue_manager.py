import sqlite3
from typing import List, Tuple
from pathlib import Path
from root import ROOT
from src.news.news import News


root = Path(ROOT)

class QueueManager:
    @staticmethod
    def create_queue():
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Queue (
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
    def push_to_queue(news_list: List[News]):
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO Queue (header, text, author, date, time)
        VALUES (?, ?, ?, ?, ?)
        """
        for news in news_list:
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
    def get_queue() -> List[Tuple[int, News]]:
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT id, header, text, author, date, time FROM Queue")
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

    @staticmethod
    def pop_queue(id: int):
        conn = sqlite3.connect(str(root / "src" / "news" / "database.db"))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Queue WHERE id = ?", (id,))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    print("Queue... ", end="")
    QueueManager.create_queue()
    QueueManager.push_to_queue([News(header="Привет", author="Артём", date="1 янв", time="12:30")])
    print("OK")

