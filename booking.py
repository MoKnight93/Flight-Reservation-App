import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import database
from datetime import datetime

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller

        # Navbar
        navbar = tk.Frame(self, bg="#333333", height=50)
        navbar.pack(fill="x")
        tk.Label(navbar, text="Leaving On A Jet Plane", fg="white", bg="#333333",
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=50, pady=10)

        btn_style = {"font": ("Helvetica", 12), "bg": "#4CAF50", "fg": "white", "bd": 0, "activebackground": "#45a049"}
        tk.Button(navbar, text="Home", **btn_style,
                  command=lambda: controller.show_frame("HomePage")).pack(side="right", padx=25)
        tk.Button(navbar, text="View Reservations", **btn_style,
                  command=lambda: controller.show_frame("ReservationsPage")).pack(side="right", padx=10)

        # Title
        tk.Label(self, text="Book a Flight", font=("Helvetica", 20, "bold"),
                 bg="#f2f2f2").pack(pady=20)

        form_frame = tk.Frame(self, bg="#f2f2f2")
        form_frame.pack(pady=10)

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

        # Submit Button
        tk.Button(self, text="Submit", font=("Helvetica", 14, "bold"), bg="#2196F3", fg="white",
                  activebackground="#1976D2", width=15, command=self.submit_reservation).pack(pady=30)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            messagebox.showerror("Invalid Date", "Please select a valid date (YYYY-MM-DD).")
            return False

    def clear_form(self):
        for entry in self.fields.values():
            entry.delete(0, tk.END)
        self.date_entry.set_date(datetime.today())

    def submit_reservation(self):
        for key, entry in self.fields.items():
            if not entry.get().strip():
                messagebox.showerror("Error", f"{key} is required")
                return
        date_text = self.date_entry.get()
        if not self.validate_date(date_text):
            return
        try:
            database.add_reservation(
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
        messagebox.showinfo("Success", "Reservation added successfully!")
        self.clear_form()
        self.controller.show_frame("ReservationsPage")
