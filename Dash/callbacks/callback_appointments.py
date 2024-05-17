from Dash.index import app
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from Algorithms.definitive_timeslot import get_definitive_timeslot_clarke


# Example callback to handle time slot selections
@app.callback(
    Output('selected_timeslots_text', 'children'),
    Output('definitive_timeslot_text', 'children'),
    Input('confirm-selection', 'n_clicks'),
    State({'type': 'checklist', 'index': ALL}, 'value'),
    State('session-store', 'data'),
    prevent_initial_call=True
)
def update_selected_timeslots(n_clicks, selected_timeslots, user_data):
    if n_clicks and n_clicks > 0:
        # Flatten the list of selected timeslots and filter out any empty selections
        selected_slots = [slot for sublist in selected_timeslots for slot in sublist if sublist]

        if not selected_slots:
            # If no slots were selected, inform the user
            return 'No timeslots selected, please try again.', ""

        definitive_slot = get_definitive_timeslot_clarke(selected_slots, user_data)

        selected_slots_text = ', '.join(selected_slots)

        # Update the button text to reflect the selected timeslots
        return f"You have selected: {selected_slots_text}", definitive_slot
    return 'Select timeslots and press OK', ""

