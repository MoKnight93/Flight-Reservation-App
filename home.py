import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")

        # Navbar
        navbar = tk.Frame(self, bg="#333333", height=50)
        navbar.pack(fill="x")
        tk.Label(navbar, text="Leaving On A Jet Plane", fg="white", bg="#333333",
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=50, pady=10)

        btn_style = {"font": ("Helvetica", 12), "bg": "#4CAF50", "fg": "white", "bd": 0, "activebackground": "#45a049"}
        tk.Button(navbar, text="Book Flight", **btn_style,
                  command=lambda: controller.show_frame("BookingPage")).pack(side="right", padx=25)
        tk.Button(navbar, text="View Reservations", **btn_style,
                  command=lambda: controller.show_frame("ReservationsPage")).pack(side="right", padx=10)

        # Welcome Heading
        tk.Label(self, text="Welcome to Leaving On A Jet Plane",
                 font=("Helvetica", 25, "bold"), bg="#f2f2f2").pack(pady=40)

        tk.Label(self, text="Best Flight Reservation Experience", font=("Helvetica", 15),
                 bg="#f2f2f2", fg="grey").pack(pady=10)

        # Buttons centered
        btn_frame = tk.Frame(self, bg="#f2f2f2")
        btn_frame.pack(pady=30)

        card_style = {"font": ("Helvetica", 14, "bold"), "width": 15, "height": 3,
                      "bg": "#2196F3", "fg": "white", "activebackground": "#1976D2", "bd": 0}

        tk.Button(btn_frame, text="Book Flight", **card_style,
                  command=lambda: controller.show_frame("BookingPage")).grid(row=0, column=0, padx=30, pady=10)

        tk.Button(btn_frame, text="View Reservations", **card_style,
                  command=lambda: controller.show_frame("ReservationsPage")).grid(row=0, column=1, padx=30, pady=10)
