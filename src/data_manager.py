"""
Data Management System
Handles data storage, retrieval, and export functionality
"""

import json
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
import csv
import io


class DataManager:
    """Manages feedback data storage and retrieval"""

    def __init__(
        self, db_path="data/feedback.db", json_backup_path="data/feedback_backup.json"
    ):
        self.db_path = Path(db_path)
        self.json_backup_path = Path(json_backup_path)
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database"""
        # Create data directory
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create database and tables
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    feedback_text TEXT NOT NULL,
                    input_method TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    overall_sentiment REAL,
                    textblob_sentiment REAL,
                    vader_sentiment REAL,
                    keyword_sentiment REAL,
                    subjectivity REAL,
                    confidence REAL,
                    text_length INTEGER,
                    word_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def save_feedback(self, feedback_data):
        """Save feedback to database and JSON backup"""
        try:
            # Extract sentiment analysis data
            sentiment = feedback_data.get("sentiment_analysis", {})

            # Prepare data for database
            db_data = {
                "product_id": feedback_data["product_id"],
                "product_name": feedback_data["product_name"],
                "feedback_text": feedback_data["feedback_text"],
                "input_method": feedback_data["input_method"],
                "timestamp": feedback_data["timestamp"],
                "overall_sentiment": sentiment.get("overall_sentiment", 0),
                "textblob_sentiment": sentiment.get("textblob_sentiment", 0),
                "vader_sentiment": sentiment.get("vader_sentiment", 0),
                "keyword_sentiment": sentiment.get("keyword_sentiment", 0),
                "subjectivity": sentiment.get("subjectivity", 0),
                "confidence": sentiment.get("confidence", 0),
                "text_length": sentiment.get("text_length", 0),
                "word_count": sentiment.get("word_count", 0),
            }

            # Save to SQLite
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO feedback (
                        product_id, product_name, feedback_text, input_method, timestamp,
                        overall_sentiment, textblob_sentiment, vader_sentiment, keyword_sentiment,
                        subjectivity, confidence, text_length, word_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    tuple(db_data.values()),
                )
                conn.commit()

            # Save to JSON backup
            self._save_json_backup(feedback_data)

            return True

        except Exception as e:
            print(f"Error saving feedback: {e}")
            return False

    def _save_json_backup(self, feedback_data):
        """Save feedback to JSON backup file"""
        try:
            # Load existing data
            if self.json_backup_path.exists():
                with open(self.json_backup_path, "r") as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            # Add new feedback
            existing_data.append(feedback_data)

            # Save updated data
            with open(self.json_backup_path, "w") as f:
                json.dump(existing_data, f, indent=2, default=str)

        except Exception as e:
            print(f"Error saving JSON backup: {e}")

    def get_all_feedback(self):
        """Retrieve all feedback from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT * FROM feedback ORDER BY timestamp DESC
                """
                )

                feedback_list = []
                for row in cursor.fetchall():
                    # Reconstruct sentiment analysis data
                    sentiment_analysis = {
                        "overall_sentiment": row["overall_sentiment"],
                        "textblob_sentiment": row["textblob_sentiment"],
                        "vader_sentiment": row["vader_sentiment"],
                        "keyword_sentiment": row["keyword_sentiment"],
                        "subjectivity": row["subjectivity"],
                        "confidence": row["confidence"],
                        "text_length": row["text_length"],
                        "word_count": row["word_count"],
                    }

                    feedback_item = {
                        "id": row["id"],
                        "product_id": row["product_id"],
                        "product_name": row["product_name"],
                        "feedback_text": row["feedback_text"],
                        "input_method": row["input_method"],
                        "timestamp": row["timestamp"],
                        "sentiment_analysis": sentiment_analysis,
                        "created_at": row["created_at"],
                    }
                    feedback_list.append(feedback_item)

                return feedback_list

        except Exception as e:
            print(f"Error retrieving feedback: {e}")
            return []

    def get_feedback_by_product(self, product_id):
        """Get feedback for specific product"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT * FROM feedback WHERE product_id = ? ORDER BY timestamp DESC
                """,
                    (product_id,),
                )

                return [dict(row) for row in cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving product feedback: {e}")
            return []

    def get_feedback_by_date_range(self, start_date, end_date):
        """Get feedback within date range"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT * FROM feedback 
                    WHERE timestamp BETWEEN ? AND ? 
                    ORDER BY timestamp DESC
                """,
                    (start_date, end_date),
                )

                return [dict(row) for row in cursor.fetchall()]

        except Exception as e:
            print(f"Error retrieving feedback by date: {e}")
            return []

    def get_sentiment_statistics(self):
        """Get sentiment analysis statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT 
                        COUNT(*) as total_feedback,
                        AVG(overall_sentiment) as avg_sentiment,
                        AVG(confidence) as avg_confidence,
                        SUM(CASE WHEN overall_sentiment > 0.1 THEN 1 ELSE 0 END) as positive_count,
                        SUM(CASE WHEN overall_sentiment < -0.1 THEN 1 ELSE 0 END) as negative_count,
                        SUM(CASE WHEN overall_sentiment BETWEEN -0.1 AND 0.1 THEN 1 ELSE 0 END) as neutral_count
                    FROM feedback
                """
                )

                row = cursor.fetchone()
                if row:
                    return {
                        "total_feedback": row[0],
                        "avg_sentiment": row[1] or 0,
                        "avg_confidence": row[2] or 0,
                        "positive_count": row[3],
                        "negative_count": row[4],
                        "neutral_count": row[5],
                    }

        except Exception as e:
            print(f"Error getting statistics: {e}")

        return {
            "total_feedback": 0,
            "avg_sentiment": 0,
            "avg_confidence": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
        }

    def export_to_csv(self):
        """Export feedback data to CSV format"""
        try:
            feedback_data = self.get_all_feedback()
            if not feedback_data:
                return ""

            # Flatten the data for CSV export
            flattened_data = []
            for item in feedback_data:
                flat_item = {
                    "id": item["id"],
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "feedback_text": item["feedback_text"],
                    "input_method": item["input_method"],
                    "timestamp": item["timestamp"],
                    "overall_sentiment": item["sentiment_analysis"][
                        "overall_sentiment"
                    ],
                    "textblob_sentiment": item["sentiment_analysis"][
                        "textblob_sentiment"
                    ],
                    "vader_sentiment": item["sentiment_analysis"]["vader_sentiment"],
                    "keyword_sentiment": item["sentiment_analysis"][
                        "keyword_sentiment"
                    ],
                    "subjectivity": item["sentiment_analysis"]["subjectivity"],
                    "confidence": item["sentiment_analysis"]["confidence"],
                    "text_length": item["sentiment_analysis"]["text_length"],
                    "word_count": item["sentiment_analysis"]["word_count"],
                    "created_at": item["created_at"],
                }
                flattened_data.append(flat_item)

            # Convert to CSV
            df = pd.DataFrame(flattened_data)
            return df.to_csv(index=False)

        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return ""

    def export_to_json(self):
        """Export feedback data to JSON format"""
        try:
            feedback_data = self.get_all_feedback()
            return json.dumps(feedback_data, indent=2, default=str)

        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return "{}"

    def clear_all_data(self):
        """Clear all feedback data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM feedback")
                conn.commit()

            # Clear JSON backup
            if self.json_backup_path.exists():
                with open(self.json_backup_path, "w") as f:
                    json.dump([], f)

            return True

        except Exception as e:
            print(f"Error clearing data: {e}")
            return False

    def backup_database(self):
        """Create a backup of the database"""
        try:
            backup_path = (
                self.db_path.parent
                / f"feedback_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )

            # Copy database file
            import shutil

            shutil.copy2(self.db_path, backup_path)

            return str(backup_path)

        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
