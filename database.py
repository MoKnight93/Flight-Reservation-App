import os
import sqlite3
import sys
from contextlib import closing


def _app_dir():
    """Folder for the database.

    Frozen (PyInstaller) builds extract to a temp folder that is wiped on exit,
    so the DB lives in the user's data folder instead. From source it stays
    next to the code.
    """
    if getattr(sys, "frozen", False):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = os.path.join(base, "FlightReservation")
    else:
        path = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(path, exist_ok=True)
    return path


DB_NAME = os.path.join(_app_dir(), "flights.db")


def _connect():
    return closing(sqlite3.connect(DB_NAME))


def init_db():
    """Create the reservations table if it doesn't exist."""
    with _connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL
            )
        ''')
        conn.commit()


def clean(*values):
    """Strip whitespace from every value; raise ValueError if any is empty."""
    labels = ["Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"]
    cleaned = [str(v).strip() for v in values]
    for label, v in zip(labels, cleaned):
        if not v:
            raise ValueError(f"{label} is required")
    return cleaned


def _seat_taken(conn, flight_number, date, seat_number, exclude_id=None):
    row = conn.execute(
        '''SELECT id FROM reservations
           WHERE flight_number = ? COLLATE NOCASE AND date = ?
             AND seat_number = ? COLLATE NOCASE AND id IS NOT ?''',
        (flight_number, date, seat_number, exclude_id)).fetchone()
    return row is not None


def add_reservation(name, flight_number, departure, destination, date, seat_number):
    """Insert a new reservation. Raises ValueError on invalid or duplicate data."""
    name, flight_number, departure, destination, date, seat_number = clean(
        name, flight_number, departure, destination, date, seat_number)
    with _connect() as conn:
        if _seat_taken(conn, flight_number, date, seat_number):
            raise ValueError(
                f"Seat {seat_number} on flight {flight_number} on {date} is already booked.")
        conn.execute('''
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, flight_number, departure, destination, date, seat_number))
        conn.commit()


def get_reservations():
    """Fetch all reservations, newest first."""
    with _connect() as conn:
        return conn.execute('SELECT * FROM reservations ORDER BY id DESC').fetchall()


def get_reservation(res_id):
    """Fetch one reservation by ID (or None)."""
    with _connect() as conn:
        return conn.execute('SELECT * FROM reservations WHERE id = ?', (res_id,)).fetchone()


def delete_reservation(res_id):
    """Delete a reservation by ID."""
    with _connect() as conn:
        conn.execute('DELETE FROM reservations WHERE id = ?', (res_id,))
        conn.commit()


def update_reservation(res_id, name, flight_number, departure, destination, date, seat_number):
    """Update a reservation. Raises ValueError on invalid or duplicate data."""
    name, flight_number, departure, destination, date, seat_number = clean(
        name, flight_number, departure, destination, date, seat_number)
    with _connect() as conn:
        if _seat_taken(conn, flight_number, date, seat_number, exclude_id=res_id):
            raise ValueError(
                f"Seat {seat_number} on flight {flight_number} on {date} is already booked.")
        conn.execute('''
            UPDATE reservations
            SET name=?, flight_number=?, departure=?, destination=?, date=?, seat_number=?
            WHERE id=?
        ''', (name, flight_number, departure, destination, date, seat_number, res_id))
        conn.commit()


# Auto-run database initialization when this file is imported
init_db()
