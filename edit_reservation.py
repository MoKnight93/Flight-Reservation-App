import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import database
from datetime import datetime

class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller
        self.reservation_id = None

        # Navbar
        navbar = tk.Frame(self, bg="#333333", height=50)
        navbar.pack(fill="x")
        tk.Label(navbar, text="Leaving On A Jet Plane", fg="white", bg="#333333",
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=50, pady=10)

        btn_style = {"font": ("Helvetica", 12), "bg": "#4CAF50", "fg": "white", "bd": 0, "activebackground": "#45a049"}
        tk.Button(navbar, text="Home", **btn_style,
                  command=lambda: controller.show_frame("HomePage")).pack(side="right", padx=25)
        # show_frame already refreshes the reservations list
        tk.Button(navbar, text="Reservations", **btn_style,
                  command=lambda: controller.show_frame("ReservationsPage")).pack(side="right", padx=10)

        # Page Title
        tk.Label(self, text="Edit Reservation", font=("Helvetica", 20, "bold"),
                 bg="#f2f2f2").pack(pady=20)

        # Form
        form_frame = tk.Frame(self, bg="#f2f2f2")
        form_frame.pack(pady=20)

        label_style = {"font": ("Helvetica", 12), "bg": "#f2f2f2"}
        entry_style = {"font": ("Helvetica", 12), "bd": 1, "relief": "solid", "width": 25}

        self.fields = {}
        field_names = ["Name", "Flight Number", "Departure", "Destination", "Seat Number"]

        for i, label in enumerate(field_names):
            tk.Label(form_frame, text=label, **label_style).grid(row=i, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(form_frame, **entry_style)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.fields[label] = entry

        # Date picker
        tk.Label(form_frame, text="Date", **label_style).grid(row=5, column=0, padx=10, pady=8, sticky="e")
        self.date_entry = DateEntry(form_frame, date_pattern='yyyy-mm-dd', width=22)
        self.date_entry.grid(row=5, column=1, padx=10, pady=8)

        # Update Button
        tk.Button(self, text="Update Reservation", font=("Helvetica", 14, "bold"),
                  bg="#2196F3", fg="white", width=20, activebackground="#1976D2",
                  command=self.update_reservation).pack(pady=30)

    @staticmethod
    def _parse_date(text):
        """Accept YYYY-MM-DD and older formats such as 2025/9/10."""
        text = str(text).strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                pass
        return datetime.today().date()

    def load_reservation(self, reservation):
        """Load a reservation row (straight from the database) into the fields."""
        self.reservation_id = reservation[0]
        values = {
            "Name": reservation[1],
            "Flight Number": reservation[2],
            "Departure": reservation[3],
            "Destination": reservation[4],
            "Seat Number": reservation[6],
        }
        for key, value in values.items():
            self.fields[key].delete(0, tk.END)
            self.fields[key].insert(0, str(value))
        self.date_entry.set_date(self._parse_date(reservation[5]))

    def update_reservation(self):
        if self.reservation_id is None:
            messagebox.showerror("Error", "No reservation loaded")
            return
        for key, entry in self.fields.items():
            if not entry.get().strip():
                messagebox.showerror("Error", f"{key} is required")
                return
        date_text = self.date_entry.get()
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please select a valid date (YYYY-MM-DD).")
            return
        try:
            database.update_reservation(
                self.reservation_id,
                self.fields["Name"].get(),
                self.fields["Flight Number"].get(),
                self.fields["Departure"].get(),
                self.fields["Destination"].get(),
                date_text,
                self.fields["Seat Number"].get()
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Success", "Reservation updated successfully!")
        self.controller.show_frame("ReservationsPage")
