import json
from Scheduler.optimizer import read_appointments, finalize_appointments

class BookingHandler:
    def __init__(self, file_path="appointments.json"):
        self.file_path = file_path

    def save_appointment(self, appointment):
        # Existing method for saving appointments
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(vars(appointment))

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def process_optimization(self, date):
        """Process optimization for all appointments on a given date."""
        appointments = read_appointments(self.file_path, date)
        if not appointments:
            print("No appointments found for this date.")
            return
        optimized_schedule = finalize_appointments(appointments)
        with open(self.file_path, "w") as file:
            json.dump(optimized_schedule, file, indent=4)
        return optimized_schedule
