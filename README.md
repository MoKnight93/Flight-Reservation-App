# Leaving On A Jet Plane – Flight Reservation System

A desktop **Flight Reservation System** built with **Python**, **Tkinter** and **SQLite**.
Book, view, edit and delete flight reservations through a simple GUI.

## Requirements
- Python 3.13 (the version the project is built and tested with)
- Tkinter and sqlite3 (bundled with Python; on Linux install `python3-tk`)
- `tkcalendar` (date picker) and `pyinstaller` (only for building the `.exe`)

```bash
pip install -r requirements.txt
```

## Run from source
```bash
git clone https://github.com/MoKnight93/Flight_Reservation_App.git
cd Flight_Reservation_App
pip install -r requirements.txt
python main.py
```

## Build the executable
```bash
pyinstaller main.spec
```
The exe is created in `dist/main.exe`. The spec already includes the `babel.numbers`
hidden import that `tkcalendar` needs. Test the exe on a machine without Python.

Unsigned PyInstaller executables may trigger Windows SmartScreen or antivirus
warnings. This is expected; choose "More info" > "Run anyway".

## Where is the data stored?
- From source: `flights.db` next to `main.py`.
- Built exe: `%APPDATA%\FlightReservation\flights.db`.

The database is created automatically on first launch. It is not shipped with the app.

## How to use
- **Home** – go to Book Flight or View Reservations.
- **Book a Flight** – fill in Name, Flight Number, Departure, Destination, Date and Seat Number, then **Submit**. All fields are required, and the same seat on the same flight and date can't be booked twice.
- **View Reservations** – table of all bookings. Select a row, then **Edit Selected** or **Delete Selected** (deleting asks for confirmation).
- **Edit** – change the details and click **Update Reservation**.

## File structure
```
├── main.py              # Entry point and page navigation
├── database.py          # SQLite access and validation
├── home.py              # Home page
├── booking.py           # Booking form
├── reservation_list.py  # Reservations table, edit/delete actions
├── edit_reservation.py  # Edit form
├── main.spec            # PyInstaller build config
├── flight.ico           # Application icon
├── requirements.txt
└── .gitignore
```
