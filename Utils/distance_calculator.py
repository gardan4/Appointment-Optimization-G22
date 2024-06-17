import requests
class DistanceCalculator:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_travel_time(self, origin, destination):
        if origin == destination:
            return 0

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={self.api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data['status'] == 'OK':
            try:
                travel_time = data['rows'][0]['elements'][0]['duration'][
                                  'value'] / 60  # Convert from seconds to minutes
                return travel_time
            except (IndexError, KeyError) as e:
                print(f"Error retrieving travel time between {origin} and {destination}: {e}")
                return float('inf')  # Return a large number to indicate an error in travel time
        else:
            print(f"Error fetching data from API: {data}")
            return float('inf')  # Return a large number to indicate an error in fetching data
