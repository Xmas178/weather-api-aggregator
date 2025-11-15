"""
Weather data analytics module.

Uses Pandas for data analysis:
- Temperature trends
- Source comparisons
- Simple statistics
"""

import pandas as pd
import sqlite3
from typing import Dict, List
from datetime import datetime, timedelta


class WeatherAnalytics:
    """Analytics service for weather data."""

    def __init__(self, db_path: str = "weather_data.db"):
        """
        Initialize analytics service.

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path

    def get_dataframe(self, city: str, hours: int = 168) -> pd.DataFrame:
        """
        Load weather data as Pandas DataFrame.

        Args:
            city: City name
            hours: Hours of history (default: 168 = 1 week)

        Returns:
            DataFrame with weather observations
        """
        conn = sqlite3.connect(self.db_path)

        query = """
            SELECT * FROM weather_data
            WHERE city = ?
            AND timestamp >= datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp ASC
        """

        df = pd.read_sql_query(query, conn, params=(city, hours))
        conn.close()

        # Convert timestamp to datetime
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        return df

    def get_temperature_trend(self, city: str, hours: int = 24) -> Dict:
        """
        Calculate temperature trend (warming/cooling).

        Args:
            city: City name
            hours: Time period

        Returns:
            Dictionary with trend information
        """
        df = self.get_dataframe(city, hours)

        if df.empty or len(df) < 2:
            return {"trend": "insufficient_data", "change": 0, "observations": len(df)}

        # Calculate temperature change (last - first)
        first_temp = df.iloc[0]["temperature"]
        last_temp = df.iloc[-1]["temperature"]
        change = round(last_temp - first_temp, 1)

        # Determine trend
        if change > 0.5:
            trend = "warming"
        elif change < -0.5:
            trend = "cooling"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "change": change,
            "first_temperature": first_temp,
            "last_temperature": last_temp,
            "observations": len(df),
        }

    def compare_sources(self, city: str, hours: int = 24) -> Dict:
        """
        Compare temperature data from different sources.

        Args:
            city: City name
            hours: Time period

        Returns:
            Dictionary with source comparison
        """
        df = self.get_dataframe(city, hours)

        if df.empty:
            return {"error": "No data available"}

        # Group by source and calculate statistics
        comparison = {}

        for source in df["source"].unique():
            source_data = df[df["source"] == source]

            comparison[source] = {
                "count": len(source_data),
                "avg_temperature": round(source_data["temperature"].mean(), 1),
                "min_temperature": round(source_data["temperature"].min(), 1),
                "max_temperature": round(source_data["temperature"].max(), 1),
            }

        return comparison

    def get_hourly_averages(self, city: str, hours: int = 24) -> List[Dict]:
        """
        Get hourly average temperatures for visualization.

        Args:
            city: City name
            hours: Time period

        Returns:
            List of hourly data points
        """
        df = self.get_dataframe(city, hours)

        if df.empty:
            return []

        # Extract hour from timestamp
        df["hour"] = df["timestamp"].dt.hour

        # Group by hour and calculate average
        hourly = df.groupby("hour")["temperature"].mean().reset_index()

        # Convert to list of dictionaries for API response
        result = []
        for _, row in hourly.iterrows():
            result.append(
                {
                    "hour": int(row["hour"]),
                    "avg_temperature": round(row["temperature"], 1),
                }
            )

        return result


# Single instance for the app
analytics = WeatherAnalytics()
