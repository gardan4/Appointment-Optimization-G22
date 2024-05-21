import json
from datetime import datetime, time

import numpy as np

from Algorithms.clarke_wright import ClarkeWright
from Algorithms.client import Client


def convert_to_time(time_str):
    # Extract hours and minutes from the string
    parts = time_str.split('h')
    hours = int(parts[0])
    minutes = int(parts[1].replace('min', ''))

    # Create a time object
    return time(hours, minutes)


def get_definitive_timeslot_clarke(selected_slots, user_data):
    """
    :param selected_slots:
    :param user_data:
    :return:  The definitive timeslot based on the selected slots and user data and update the json file
    """
    # get all the  appointments in a list
    appointments_in_slot_new = []
    appointments_in_slot_old = []

    appointments_in_slot_new.append({
        "username": user_data['username'],
        "location": user_data['location'],
        "appointment_date": selected_slots
    })
    with open("./Data/planned_appointments.json", mode='r') as json_file:
        data = json.load(json_file)

        solutions_new = []
        solutions_old = []
        for slot in selected_slots:
            # get all the appointments for the selected slot from the json file
            for row in data:
                if row['appointment_date'][0] == slot:
                    appointments_in_slot_old.append(row)
                    appointments_in_slot_new.append(row)

            # old solutions
            clients_old = [Client(appointment['username'], appointment['location'], appointment['appointment_date']) for
                           appointment in appointments_in_slot_old]
            clarke_old = ClarkeWright(clients_old)
            clarke_old.solve(slot, ".\Data\distance_matrix.csv")
            solutions_old.append([clarke_old.get_solution(), slot])

            # new solutions
            clients_new = [Client(appointment['username'], appointment['location'], appointment['appointment_date']) for
                           appointment in appointments_in_slot_new]
            clarke_new = ClarkeWright(clients_new)
            clarke_new.solve(slot, ".\Data\distance_matrix.csv")
            solutions_new.append([clarke_new.get_solution(), slot])

        # get the route with the smallest time increase
        smallest_time_increase_route = []
        # calculate the time increase for each route per index and select the route with the smallest time increase
        time_increase = np.inf
        for i in range(len(solutions_old)):
            if solutions_new[i][0][1] - solutions_old[i][0][1] < time_increase:
                time_increase = solutions_new[i][0][1] - solutions_old[i][0][1]
                smallest_time_increase_route = solutions_new[i]

    return smallest_time_increase_route[1]


def get_definitive_timeslot_milp(selected_slots, user_data):
    return ""
