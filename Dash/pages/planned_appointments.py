from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import dash_ag_grid as dag
import dash
import pandas as pd
import json


@callback(
    Output('planned_appointments', 'rowData'),
    Input('session-store', 'data'),
)
def generate_planned_appointments_layout(user_data):
    with open("./Data/planned_appointments.json", mode='r') as json_file:
        data = json.load(json_file)
        planned_appointments = pd.DataFrame(data)
        planned_appointments = planned_appointments[planned_appointments['username'] == user_data['username']]
        planned_appointments = planned_appointments.to_dict('records')
        print(planned_appointments)
        return planned_appointments

layout = html.Div(
    children=[
        html.Button("Delete Selected", id="del_button", style={"margin": "auto", "display": "block"}),
        #dash aggrid
        dag.AgGrid(
            id='planned_appointments',
            columnDefs=[

                {'field': 'username', 'headerName': 'Username', "checkboxSelection": True, "headerCheckboxSelection": True},
                {'field': 'location', 'headerName': 'location'},
                {'field': 'appointment_date', 'headerName': 'Appointment Date'},
            ],
            rowData=[],
            defaultColDef={"autoHeaderHeight": True, },
            columnSize="sizeToFit",
            style={'height': '500px', 'width': '50%', 'margin': 'auto'},
            dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
        ),
    ],
    id='planned_appointments'
)

@callback(
    Output("planned_appointments", "deleteSelectedRows"),
    Input("del_button", "n_clicks"),
    State("planned_appointments", "selectedRows"),
    prevent_initial_call=True
)
def selected(_, rows):
    # delete selected rows from json file
    with open("./Data/planned_appointments.json", mode='r') as json_file:
        data = json.load(json_file)
        print(data)
        print(rows)
        for row in rows:
            data.remove(row)
        with open("./Data/planned_appointments.json", mode='w') as json_file:
            json.dump(data, json_file)

    return True

dash.register_page(
    __name__,
    path='/planned_appointments',
    # redirect_from=['/'],
    title='Planned Appointments',
    layout=layout,
)
