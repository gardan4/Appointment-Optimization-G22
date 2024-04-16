import json

class BookingHandler:
    def __init__(self, file_path="appointments.json"):
        self.file_path = file_path

    def save_appointment(self, appointment):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(vars(appointment))

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def offer_time_slots(self, client_id, location):
        # Example slots, you will eventually want these generated based on actual availability
        slots = {
            "morning": f"{location} - 09:00 to 12:00",
            "afternoon": f"{location} - 13:00 to 16:00"
        }
        return slots

