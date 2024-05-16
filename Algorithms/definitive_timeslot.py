import json


def get_definitive_timeslot_clarke(selected_slots, user_data):
    """
    :param selected_slots:
    :param user_data:
    :return:  The definitive timeslot based on the selected slots and user data and update the json file
    """
    clarke = ClarkeWright()
    #get all the  appointments from the json file
    with open("./Data/planned_appointments.json", mode='r') as json_file:
        for slot in selected_slots:
            appointments_in_slot = []
            appointments_in_slot.append(slot)
            #get all the appointments for the selected slot from the json file
            data = json.load(json_file)
            for row in data:
                if row['appointment_date'] == slot:
                    appointments_in_slot.append(row)


            pass
    return ""

def get_definitive_timeslot_milp(selected_slots, user_data):
    # milp = milp()
    # get all the  appointments from the json file
    with open("./Data/planned_appointments.json", mode='r') as json_file:
        for slot in selected_slots:
            appointments_in_slot = []
            appointments_in_slot.append(slot)
            # get all the appointments for the selected slot from the json file
            data = json.load(json_file)
            for row in data:
                if row['appointment_date'] == slot:
                    appointments_in_slot.append(row)

            pass
    return ""