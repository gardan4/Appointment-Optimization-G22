from booking_handler import BookingHandler
from Data.models import Appointment

def main_menu():
    handler = BookingHandler()
    print("Welcome to the Piano Tuning Booking System")
    client_id = input("Please enter your client ID: ")
    location = input("Enter the location for the tuning service: ")

    slots = handler.offer_time_slots(client_id, location)
    print("Available time slots:")
    for slot in slots:
        print(f"{slot} slot: {slots[slot]}")

    chosen_slot = input("Choose a slot (morning/afternoon): ")
    start_time, end_time = slots[chosen_slot].split(" - ")[1].split(" to ")

    new_appointment = Appointment(client_id, location, start_time, end_time)
    handler.save_appointment(new_appointment)
    print("Your appointment has been booked.")

if __name__ == "__main__":
    main_menu()
