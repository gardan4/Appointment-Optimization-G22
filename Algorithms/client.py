class Client:
    def __init__(self, name, location, availability):
        self.name = name
        self.location = location
        self.availability = availability

        self.scheduled = False

    def get_number_availability(self):
        return len(self.availability)

    def get_location(self):
        return self.location

    def get_availability(self):
        return self.availability

    def set_scheduled(self, slot):
        self.scheduled = True
        self.availability = [slot]