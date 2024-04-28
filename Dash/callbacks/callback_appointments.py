from Dash.index import app
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL


# Example callback to handle time slot selections
@app.callback(
    Output('confirm-selection', 'children'),
    Input('confirm-selection', 'n_clicks'),
    State({'type': 'checklist', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def update_selected_timeslots(n_clicks, selected_timeslots):
    # Debugging print statement
    print(f"Raw selected timeslots: {selected_timeslots}")

    if n_clicks and n_clicks > 0:
        # Flatten the list of selected timeslots and filter out any empty selections
        selected_slots = [slot for sublist in selected_timeslots for slot in sublist if sublist]

        # Debugging print statement
        print(f"Processed selected timeslots: {selected_slots}")

        if not selected_slots:
            # If no slots were selected, inform the user
            return 'No timeslots selected, please try again.'

        selected_slots_text = ', '.join(selected_slots)

        # Update the button text to reflect the selected timeslots
        return f"You have selected: {selected_slots_text}"
    return 'Select timeslots and press OK'


# Callback to update selection field style

@app.callback(
    Output({'type': 'selection-field', 'day': MATCH, 'slot': MATCH}, 'className'),
    [Input({'type': 'timeslot-checklist', 'day': MATCH, 'slot': MATCH}, 'value')],
    prevent_initial_call=True
)
def update_selection_style(selected_values, day, slot):
    base_class = 'selection-field'
    if selected_values:
        return f'{base_class} selected'
    return base_class