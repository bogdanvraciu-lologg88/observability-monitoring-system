import sqlite3


DATABASE_NAME = "history.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT,
        response_time REAL,
        success INTEGER,
        timestamp TEXT
    )
    """)

    connection.commit()
    connection.close()


def save_result(result):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO metrics (
        service,
        response_time,
        success,
        timestamp
    )
    VALUES (?, ?, ?, ?)
    """, (
        result["service"],
        result.get("response_time", 0),
        int(result["success"]),
        result["timestamp"]
    ))

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
    SELECT service, response_time, success, timestamp
    FROM metrics
    ORDER BY id DESC
    LIMIT 1000
    """)

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:
        history.append({
            "service": row[0],
            "response_time": row[1],
            "success": bool(row[2]),
            "timestamp": row[3]
        })

    return history