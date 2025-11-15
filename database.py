"""
Database module for storing historical weather data.

Uses SQLite for simplicity. Stores each weather observation with:
- City name
- Data source (FMI, Foreca, Yr)
- Weather parameters (temperature, humidity, wind, etc.)
- Timestamp
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Optional


class WeatherDatabase:
    """Simple SQLite database for weather observations."""

    def __init__(self, db_path: str = "weather_data.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """Create weather_data table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                source TEXT NOT NULL,
                temperature REAL,
                humidity INTEGER,
                pressure REAL,
                wind_speed REAL,
                precipitation REAL,
                weather_description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def save_observation(self, city: str, source: str, weather_data: Dict) -> bool:
        """
        Save a single weather observation to database.

        Args:
            city: City name
            source: Data source (FMI, Foreca, or Yr)
            weather_data: Dictionary with weather parameters

        Returns:
            True if saved successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO weather_data
                (city, source, temperature, humidity, pressure,
                 wind_speed, precipitation, weather_description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    city,
                    source,
                    weather_data.get("temperature"),
                    weather_data.get("humidity"),
                    weather_data.get("pressure"),
                    weather_data.get("wind_speed"),
                    weather_data.get("precipitation"),
                    weather_data.get("weather"),
                ),
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error saving to database: {e}")
            return False

    def get_history(self, city: str, hours: int = 24) -> List[Dict]:
        """
        Get weather history for a city.

        Args:
            city: City name
            hours: How many hours of history to fetch

        Returns:
            List of weather observations
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM weather_data
            WHERE city = ?
            AND timestamp >= datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp DESC
        """,
            (city, hours),
        )

        rows = cursor.fetchall()
        conn.close()

        # Convert to list of dictionaries
        return [dict(row) for row in rows]

    def get_statistics(self, city: str, hours: int = 24) -> Dict:
        """
        Calculate simple statistics for a city.

        Args:
            city: City name
            hours: Time period for statistics

        Returns:
            Dictionary with min, max, average temperatures
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                MIN(temperature) as min_temp,
                MAX(temperature) as max_temp,
                AVG(temperature) as avg_temp,
                COUNT(*) as observation_count
            FROM weather_data
            WHERE city = ?
            AND timestamp >= datetime('now', '-' || ? || ' hours')
        """,
            (city, hours),
        )

        result = cursor.fetchone()
        conn.close()

        if result and result[3] > 0:  # If we have observations
            return {
                "min_temperature": round(result[0], 1) if result[0] else None,
                "max_temperature": round(result[1], 1) if result[1] else None,
                "avg_temperature": round(result[2], 1) if result[2] else None,
                "observation_count": result[3],
            }
        else:
            return {
                "min_temperature": None,
                "max_temperature": None,
                "avg_temperature": None,
                "observation_count": 0,
            }


# Create a single instance to use throughout the app
weather_db = WeatherDatabase()
