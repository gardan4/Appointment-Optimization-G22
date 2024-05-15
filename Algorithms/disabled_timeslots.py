
def get_disabled_timeslots(dates, location):
    """
    Get the disabled timeslots for 2 weeks
    """
    disabled = []
    for date in dates:
        disable = [False, False]
        for timeslot in ['morning', 'evening']:
            # get current appointments for this date and timeslot
            # check if travel time is possible
            # return True if travel time is not possible
            if timeslot == 'morning' and not get_travel_possible(location, date, timeslot):
                disable[0] = True
            elif timeslot == 'evening' and not get_travel_possible(location, date, timeslot):
                disable[1] = True
        disabled.append(disable)
    return disabled

def get_travel_possible(location, date, timeslot):
    """
    Check if travel time is possible
    """
    return True