from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import dash
import datetime
from Algorithms.disabled_timeslots import get_disabled_timeslots


# Assuming you have a function to generate the dates for the current and next week
def generate_dates_for_weeks():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    dates = [start + datetime.timedelta(days=d) for d in range(14)]  # two weeks
    return dates


# Assuming generate_dates_for_weeks function is defined as previously mentioned
@callback(
    Output('time-slot-selection', 'children'),
    Input('session-store', 'data'),
)
def generate_time_slot_layout(user_data):
    dates = generate_dates_for_weeks()
    this_week = dates[:7]
    next_week = dates[7:]

    # Helper function to create a day column
    def create_day_column(day, date, disable):
        return html.Div(className='day-column', children=[
            html.Div(f"{day} {date.strftime('%m-%d')}", className='week-title', style={'color': 'white'}),
            dcc.Checklist(
                options=[
                    {'label': 'Morning slot: 09:00 - 12:00', 'value': f'{date.strftime("%Y-%m-%d")}_morning', 'disabled': disable[0]},
                ],
                value=[],
                id={'type': 'checklist', 'index': date.strftime('%Y-%m-%d')},
                className="timeslot"
            ),
            dcc.Checklist(
                options=[
                    {'label': 'Evening slot: 01:00 - 17:00', 'value': f'{date.strftime("%Y-%m-%d")}_evening', 'disabled': disable[1]},
                ],
                value=[],
                id={'type': 'checklist', 'index': date.strftime('%Y-%m-%d')},
                className="timeslot"
            )
        ])

    disabled = get_disabled_timeslots(dates, location=user_data['location'])

    # Generate columns for each day
    this_week_columns = []
    next_week_columns = []
    counter = 0

    for date in this_week:
        this_week_columns.append(create_day_column(date.strftime('%A'), date, disabled[counter]))
        counter += 1
    for date in next_week:
        next_week_columns.append(create_day_column(date.strftime('%A'), date, disabled[counter]))
        counter += 1



    layout = html.Div(children=[
        html.Div('This week', className='week-title', style={'color': 'white'}),
        html.Div(this_week_columns, className='week-container'),
        html.Div('Next week', className='week-title', style={'color': 'white'}),
        html.Div(next_week_columns, className='week-container'),
        html.Div(
            html.Button('Select timeslots and press OK', id='confirm-selection', className="button-confirm"),
            className='confirm-button-container'
        )
    ])

    return layout


# Combine everything into the final layout
layout = html.Div(
    children=[],
    id='time-slot-selection'
)

dash.register_page(
    __name__,
    path='/plan_appointment',
    # redirect_from=['/'],
    title='Plan Appointment',
    layout=layout,
)
