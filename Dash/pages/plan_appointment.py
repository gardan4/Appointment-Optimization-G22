from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import dash
import datetime


# Assuming you have a function to generate the dates for the current and next week
def generate_dates_for_weeks():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    dates = [start + datetime.timedelta(days=d) for d in range(14)]  # two weeks
    return dates


# Assuming generate_dates_for_weeks function is defined as previously mentioned
def generate_time_slot_layout():
    dates = generate_dates_for_weeks()
    this_week = dates[:7]
    next_week = dates[7:]

    # Helper function to create a day column
    def create_day_column(day, date):
        print(date)
        return html.Div(className='day-column', children=[
            html.Div(f"{day} {date[0].strftime('%m-%d')}", className='week-title', style={'color': 'white'}),
            dcc.Checklist(
                options=[
                    {'label': 'Morning slot: 09:00 - 12:00', 'value': f'{date[0].strftime("%Y-%m-%d")}_morning'},
                    {'label': 'Evening slot: 01:00 - 17:00', 'value': f'{date[0].strftime("%Y-%m-%d")}_evening'},
                ],
                value=[],
                id={'type': 'checklist', 'index': date[0].strftime('%Y-%m-%d')},
                className="timeslot"
            )
        ])

    # Generate columns for each day
    #also pass the current date to the create_day_column function
    this_week_columns = [create_day_column(date.strftime('%A'), [date]) for date in this_week]
    next_week_columns = [create_day_column(date.strftime('%A'), [date]) for date in next_week]



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
    children=generate_time_slot_layout(),
    id='time-slot-selection'
)

dash.register_page(
    __name__,
    path='/plan_appointment',
    # redirect_from=['/'],
    title='Plan Appointment',
    layout=layout,
)
