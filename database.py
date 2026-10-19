from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "voyage_beyond.db"


def get_connection():
    """Return a SQLite connection with named-row access."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create application tables if they do not exist yet."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL CHECK(score >= 0),
                total_questions INTEGER NOT NULL CHECK(total_questions > 0),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_quiz_attempt(player_name, score, total_questions):
    """Validate and save one quiz attempt; return its new ID."""
    name = " ".join(str(player_name).split())
    if not name:
        raise ValueError("Player name is required.")
    if total_questions <= 0 or score < 0 or score > total_questions:
        raise ValueError("Score must be between zero and total questions.")
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO quiz_attempts (player_name, score, total_questions) VALUES (?, ?, ?)",
            (name[:60], int(score), int(total_questions)),
        )
        return cursor.lastrowid


def get_quiz_summary():
    """Return aggregate quiz statistics and the ten best attempts."""
    with get_connection() as connection:
        summary = connection.execute(
            "SELECT COUNT(*) AS attempts, COALESCE(AVG(100.0 * score / total_questions), 0) AS average_percent FROM quiz_attempts"
        ).fetchone()
        leaderboard = connection.execute(
            "SELECT player_name, score, total_questions, created_at, ROUND(100.0 * score / total_questions, 1) AS percent FROM quiz_attempts ORDER BY (1.0 * score / total_questions) DESC, score DESC, created_at ASC LIMIT 10"
        ).fetchall()
    return {"attempts": summary["attempts"], "average_percent": round(summary["average_percent"], 1), "leaderboard": [dict(row) for row in leaderboard]}
