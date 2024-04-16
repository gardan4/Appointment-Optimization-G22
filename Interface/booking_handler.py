from models import Appointment
from Scheduler.optimizer import optimize_schedule

def handle_booking_request(client_id, requested_slot, location):
    # Create an appointment and optimize the schedule
    new_appointment = Appointment(client_id, location, requested_slot.start_time, requested_slot.end_time)
    optimize_schedule(new_appointment)
    return new_appointment
