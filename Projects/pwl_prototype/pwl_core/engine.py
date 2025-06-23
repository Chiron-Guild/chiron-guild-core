"""The core engine for the Personal Work Ledger application."""

# Standard library imports
import queue
import sqlite3
import threading
import time
from typing import Dict, Optional, Any

# Third-party library imports
from pynput import keyboard, mouse

# Local application/module imports
from pwl_core.core_logger import logger
from pwl_core.data_capture.window_monitor import get_active_window_info

DATABASE_PATH = "pwl_ledger.db"


class PWLEngine:
    """Manages input listeners, data processing, and database writing."""

    def __init__(self, db_path: str = DATABASE_PATH):
        """Initializes the engine, event queue, and database connection.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self._event_queue = queue.Queue()
        self._db_path = db_path
        self._is_running = threading.Event()

        # CORRECTED: Initialize database and get connection in one step
        self._db_conn = self._initialize_database()

        self._keyboard_listener: Optional[keyboard.Listener] = None
        self._mouse_listener: Optional[mouse.Listener] = None

    def _initialize_database(self) -> sqlite3.Connection:
        """Ensures the database and 'events' table exist, returns connection.

        Returns:
            sqlite3.Connection: An active connection to the database.
        """
        logger.info(f"Initializing database at: {self._db_path}")
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        cursor = conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            app_name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_details TEXT
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        logger.info("Database initialized successfully.")
        return conn

    def _on_press(self, key: Any) -> Optional[bool]:
        """Callback for keyboard press events."""
        window_info = get_active_window_info()
        event_data = {
            # Use a REAL type for more precise timestamps
            "timestamp": time.time(),
            "app_name": window_info.get("process_name", "Unknown") if window_info else "Unknown",
            "event_type": "key_press",
            "event_details": {"key": str(key)},
        }
        self._event_queue.put(event_data)

        if key == keyboard.Key.esc:
            logger.info("Escape key detected, signaling shutdown.")
            self.stop()
            return False
        return None

    def _on_click(self, x: int, y: int, button: Any, pressed: bool) -> None:
        """Callback for mouse click events."""
        if pressed:
            window_info = get_active_window_info()
            event_data = {
                "timestamp": time.time(),
                "app_name": window_info.get("process_name", "Unknown") if window_info else "Unknown",
                "event_type": "mouse_click",
                "event_details": {"button": str(button), "x": x, "y": y},
            }
            self._event_queue.put(event_data)

    def _database_writer(self) -> None:
        """The consumer thread that writes events from the queue to the DB."""
        logger.info("Database writer thread started.")
        cursor = self._db_conn.cursor()
        while self._is_running.is_set() or not self._event_queue.empty():
            try:
                event = self._event_queue.get(timeout=1)
                cursor.execute(
                    """
                    INSERT INTO events (timestamp, app_name, event_type, event_details)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        event["timestamp"],
                        event["app_name"],
                        event["event_type"],
                        # Using str() is fine for this prototype
                        str(event["event_details"]),
                    ),
                )
                self._db_conn.commit()
                logger.debug(f"Logged event to DB: {event['event_type']}")
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Database writer error: {e}", exc_info=True)
        logger.info("Database writer thread finished.")

    def start(self) -> None:
        """Starts the input listeners and the database writer thread."""
        logger.info("Starting PWL Engine...")
        self._is_running.set()

        self._writer_thread = threading.Thread(target=self._database_writer, daemon=True)
        self._writer_thread.start()

        self._keyboard_listener = keyboard.Listener(on_press=self._on_press)
        self._mouse_listener = mouse.Listener(on_click=self._on_click)
        self._keyboard_listener.start()
        self._mouse_listener.start()

        logger.info("PWL Engine running. Press 'Esc' to stop.")

    def stop(self) -> None:
        """Stops the engine and ensures all threads are joined."""
        if not self._is_running.is_set():
            return
        logger.info("Stopping PWL Engine...")
        self._is_running.clear()

        if self._mouse_listener and self._mouse_listener.is_alive():
            self._mouse_listener.stop()

        self._writer_thread.join()
        if self._db_conn:
            self._db_conn.close()
        logger.info("PWL Engine stopped cleanly.")