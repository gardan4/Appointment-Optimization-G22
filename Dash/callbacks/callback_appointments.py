from Dash.index import app
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL


# Example callback to handle time slot selections
@app.callback(
    Output('confirm-selection', 'children'),
    [Input('confirm-selection', 'n_clicks')],
    [State({'type': 'checklist', 'index': ALL}, 'value')],
    prevent_initial_call=True
)
def update_selected_timeslots(n_clicks, selected_timeslots):
    if n_clicks > 0:
        # Logic to handle the selected time slots
        # For now, just print them out
        print(selected_timeslots)
        # Logic to grey out certain timeslots will go here

        # Return the value for a label or store it in dcc.Store
        return 'You have selected: ' + ', '.join(str(slot) for sublist in selected_timeslots for slot in sublist)
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