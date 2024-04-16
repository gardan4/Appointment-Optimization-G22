import json
from datetime import datetime, timedelta

def read_appointments(file_path, date):
    with open(file_path, "r") as file:
        all_appointments = json.load(file)
    appointments = [
        appt for appt in all_appointments if datetime.strptime(appt['date'], "%Y-%m-%d").date() == datetime.strptime(date, "%Y-%m-%d").date()
    ]
    return appointments

def compute_optimal_path(appointments):
    return sorted(appointments, key=lambda x: datetime.strptime(x['start_time'], "%H:%M"))

def finalize_appointments(appointments):
    optimized_appointments = compute_optimal_path(appointments)
    final_schedule = []
    current_time = datetime.strptime("09:00", "%H:%M")
    for appt in optimized_appointments:
        start_time = current_time.strftime("%H:%M")
        end_time = (current_time + timedelta(hours=1)).strftime("%H:%M")
        appt['start_time'] = start_time
        appt['end_time'] = end_time
        final_schedule.append(appt)
        current_time += timedelta(hours=1)
    return final_schedule

def test_optimizer():
    # Test the optimizer with synthetic data
    test_data = [
        {"client_id": "1", "location": "Location A", "start_time": "09:00", "end_time": "12:00", "date": "2024-04-20"},
        {"client_id": "2", "location": "Location B", "start_time": "13:00", "end_time": "16:00", "date": "2024-04-20"}
    ]
    optimized_schedule = finalize_appointments(test_data)
    for appt in optimized_schedule:
        print(f"Client {appt['client_id']} - {appt['location']} from {appt['start_time']} to {appt['end_time']}")

if __name__ == "__main__":
    test_optimizer()
