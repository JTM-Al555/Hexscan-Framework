import json
import sqlite3

from datetime import datetime


class DatabaseManager:

    def __init__(self):

        self.connection = sqlite3.connect(
            "hexscan.db"
        )

        self.cursor = (
            self.connection.cursor()
        )

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            target TEXT,

            risk_level TEXT,

            risk_score INTEGER,

            technologies TEXT,

            scan_date TEXT
        )

        """)

        self.connection.commit()

    def save_scan(

        self,

        target,

        results

    ):

        risk = results.get(
            "risk_analysis",
            {}
        )

        technologies = results.get(
            "technologies",
            []
        )

        self.cursor.execute("""

        INSERT INTO scans (

            target,

            risk_level,

            risk_score,

            technologies,

            scan_date

        )

        VALUES (?, ?, ?, ?, ?)

        """, (

            target,

            risk.get(
                "risk_level",
                "Unknown"
            ),

            risk.get(
                "risk_score",
                0
            ),

            json.dumps(
                technologies
            ),

            str(
                datetime.utcnow()
            )
        ))

        self.connection.commit()

    def get_scans(self):

        self.cursor.execute("""

        SELECT * FROM scans

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()