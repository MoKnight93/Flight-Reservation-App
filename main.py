import tkinter as tk
from home import HomePage
from booking import BookingPage
from reservation_list import ReservationsPage
from edit_reservation import EditReservationPage


class FlightApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Reservation System")
        # Fit smaller screens instead of forcing a fixed 1480px width
        width = min(1100, self.winfo_screenwidth() - 80)
        height = min(600, self.winfo_screenheight() - 120)
        self.geometry(f"{width}x{height}")
        self.minsize(800, 500)
        self.resizable(True, True)
        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start at Home Page
        self.show_frame("HomePage")

    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]

        # If page has set_data, pass kwargs to it
        if hasattr(frame, "set_data"):
            frame.set_data(**kwargs)

        # Force refresh of reservations list whenever ReservationsPage is shown
        if page_name == "ReservationsPage" and hasattr(frame, "refresh_reservations"):
            frame.refresh_reservations()

        frame.tkraise()


if __name__ == "__main__":
    app = FlightApp()
    app.mainloop()
