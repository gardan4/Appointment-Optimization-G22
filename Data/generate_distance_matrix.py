import requests
import pandas as pd
import time

def get_distance_matrix(locations, api_key):
    n = len(locations)
    distance_matrix = pd.DataFrame(index=locations, columns=locations)

    # Helper function to get the distance between two locations
    def fetch_distance(origins, destinations):
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origins}&destinations={destinations}&key={api_key}"
        response = requests.get(url).json()
        if response['status'] == 'OK':
            rows = response['rows']
            distances = []
            for row in rows:
                elements = row['elements']
                for element in elements:
                    if element['status'] == 'OK':
                        distances.append(element['distance']['value'])
                    else:
                        distances.append(float('inf'))  # If no route found, set distance to infinity
            return distances
        else:
            raise Exception(f"Error fetching data from API: {response['error_message']}")

    # Iterate over all pairs of locations to fill the distance matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                distance_matrix.iloc[i, j] = 0  # Distance from a location to itself is 0
            elif pd.isna(distance_matrix.iloc[i, j]):
                origins = locations[i]
                destinations = locations[j]
                distance = fetch_distance(origins, destinations)[0]
                distance_matrix.iloc[i, j] = distance
                distance_matrix.iloc[j, i] = distance
                time.sleep(1)  # To respect API usage limits

    return distance_matrix

def save_distance_matrix_to_csv(locations, api_key, filename):
    distance_matrix = get_distance_matrix(locations, api_key)
    distance_matrix.to_csv(filename)


if __name__ == "__main__":
    locations = [
        "Asten Heusden Ommel", "Deurne Vlierden", "Geldrop", "Gemert Handel",
        "Helmond", "Helmond Brandevoort", "Mierlo", "Nuenen Gerwen Nederwetten", "Someren"
    ]
    api_key = ""
    save_distance_matrix_to_csv(locations, api_key, "..//Data//distance_matrix_google.csv")
