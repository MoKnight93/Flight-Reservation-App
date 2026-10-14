import tkinter as tk
from tkinter import ttk, messagebox
import database

class ReservationsPage(tk.Frame):
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
        tk.Button(navbar, text="Book a Flight", **btn_style,
                  command=lambda: controller.show_frame("BookingPage")).pack(side="right", padx=10)

        # Page Heading
        tk.Label(self, text="Your Reservations", font=("Helvetica", 20, "bold"),
                 bg="#f2f2f2").pack(pady=20)

        # Treeview Table
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Flight", "Departure", "Destination", "Date", "Seat"),
                                 show="headings", height=10)
        self.tree.pack(pady=10, padx=40, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#f2f2f2")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Edit Selected", bg="#2196F3", fg="white", width=18, font=("Helvetica", 12),
                  activebackground="#1976D2", command=self.edit_selected).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Delete Selected", bg="#f44336", fg="white", width=18, font=("Helvetica", 12),
                  activebackground="#d32f2f", command=self.delete_selected).pack(side="left", padx=10)

        self.refresh_reservations()

    def refresh_reservations(self):
        """Reload reservations into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in database.get_reservations():
            # iid = database id, so we never rely on the display values
            self.tree.insert("", "end", iid=str(r[0]), values=r)

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a reservation to edit")
            return
        # Re-fetch the raw row: the Treeview turns values like "0123" into 123
        reservation = database.get_reservation(int(selected[0]))
        if reservation is None:
            messagebox.showerror("Error", "That reservation no longer exists")
            self.refresh_reservations()
            return
        self.controller.frames["EditReservationPage"].load_reservation(reservation)
        self.controller.show_frame("EditReservationPage")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a reservation to delete")
            return
        res_id = int(selected[0])
        name = self.tree.set(selected[0], "Name")
        if messagebox.askyesno("Confirm Delete", f"Delete reservation for {name}?"):
            database.delete_reservation(res_id)
            self.refresh_reservations()
