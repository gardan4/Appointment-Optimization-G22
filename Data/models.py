class Location:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates


class Appointment:
    def __init__(self, client_id, location, start_time, end_time, date):
        self.client_id = client_id
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
