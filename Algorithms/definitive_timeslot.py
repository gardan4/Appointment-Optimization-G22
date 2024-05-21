import json
from datetime import datetime

from Algorithms.clarke_wright import ClarkeWright
from Algorithms.client import Client

def get_definitive_timeslot_clarke(selected_slots, user_data):
    """
    :param selected_slots:
    :param user_data:
    :return:  The definitive timeslot based on the selected slots and user data and update the json file
    """
    #get all the  appointments in a list
    appointments_in_slot = []
    clients = []

    appointments_in_slot.append({
        "username": user_data['username'],
        "location": user_data['location'],
        "appointment_date": selected_slots
    })
    with open("./Data/planned_appointments.json", mode='r') as json_file:
        data = json.load(json_file)
        solutions = []
        for slot in selected_slots:
            #get all the appointments for the selected slot from the json file
            for row in data:
                if row['appointment_date'][0] == slot:
                    appointments_in_slot.append(row)

            #create all the clients in a list
            clients = [Client(appointment['username'], appointment['location'], appointment['appointment_date']) for appointment in appointments_in_slot]
            clarke = ClarkeWright(clients)
            clarke.solve(slot, ".\Data\distance_matrix.csv")
            solutions.append(clarke.get_solution())
        print(solutions)

    return ""

def get_definitive_timeslot_milp(selected_slots, user_data):
    return ""