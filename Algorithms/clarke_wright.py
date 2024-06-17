import pandas as pd
from Algorithms.client import Client
from Utils.distance_calculator import DistanceCalculator

class ClarkeWright:
    def __init__(self, clients, api_key):
        self.depot = Client('depot', 'Mierlo', None)
        self.clients = clients
        self.route = None
        self.total_distance = 0
        self.distance_calculator = DistanceCalculator(api_key)

    def compute_savings(self, clients):
        start = []
        end = []
        s = []

        for client_1 in clients:
            if client_1 is self.depot:
                continue
            for client_2 in clients:
                if client_2 is self.depot or client_2 in start:
                    continue
                if client_1 is not client_2:
                    dist_1 = self.distance_calculator.get_travel_time(self.depot.get_location(), client_1.get_location())
                    dist_2 = self.distance_calculator.get_travel_time(self.depot.get_location(), client_2.get_location())
                    dist_clients = self.distance_calculator.get_travel_time(client_1.get_location(), client_2.get_location())

                    s.append(dist_1 + dist_2 - dist_clients)
                    start.append(client_1)
                    end.append(client_2)

        savings = pd.DataFrame(data={'Start': start, 'End': end, 'Savings': s})
        savings.sort_values(by='Savings', ascending=False, inplace=True)
        return savings

    def solve(self, timeslot):
        clients = [client for client in self.clients if timeslot in client.get_availability()]

        if len(clients) == 1:
            single_route = [self.depot, clients[0], self.depot]
            clients[0].set_scheduled(timeslot)
            self.route = single_route
            self.compute_route_length()
            return self.route

        savings = self.compute_savings(clients)
        routes = []

        for _, row in savings.iterrows():
            start_point = end_point = None
            skip = False

            for i in range(len(routes)):
                if row['Start'] in routes[i] and row['End'] in routes[i]:
                    skip = True
                if routes[i][0] is row['Start'] or routes[i][-1] is row['Start']:
                    start_point = i
                if routes[i][0] is row['End'] or routes[i][-1] is row['End']:
                    end_point = i

            if skip:
                continue
            if start_point is None and end_point is None:
                new_route = [row['Start'], row['End']]
                routes.append(new_route)
            elif start_point is None or end_point is None:
                if start_point is None:
                    if routes[end_point][0] is row['End'] and len(routes[end_point]) < 3:
                        routes[end_point].insert(0, row['Start'])
                    elif len(routes[end_point]) < 3:
                        routes[end_point].append(row['Start'])
                elif routes[start_point][0] is row['Start'] and len(routes[start_point]) < 3:
                    routes[start_point].insert(0, row['End'])
                elif len(routes[start_point]) < 3:
                    routes[start_point].append(row['End'])
                else:
                    new_route = [row['Start'], row['End']]
                    routes.append(new_route)
            elif start_point is not end_point:
                merged_route = []
                if routes[start_point][-1] is row['Start'] and routes[end_point][0] is row['End']:
                    merged_route = routes[start_point] + routes[end_point]
                elif routes[end_point][-1] is row['Start'] and routes[start_point][0] is row['End']:
                    merged_route = routes[end_point] + routes[start_point]
                elif routes[start_point][-1] is row['End'] and routes[end_point][0] is row['Start']:
                    merged_route = routes[start_point] + routes[end_point]
                elif routes[end_point][-1] is row['End'] and routes[start_point][0] is row['Start']:
                    merged_route = routes[end_point] + routes[start_point]
                elif routes[start_point][0] is row['Start'] and routes[end_point][0] is row['End']:
                    merged_route = routes[start_point][::-1] + routes[end_point]
                elif routes[start_point][0] is row['End'] and routes[end_point][0] is row['Start']:
                    merged_route = routes[start_point][::-1] + routes[end_point]
                elif routes[start_point][-1] is row['Start'] and routes[end_point][-1] is row['End']:
                    merged_route = routes[start_point] + routes[end_point][::-1]
                elif routes[start_point][-1] is row['End'] and routes[end_point][-1] is row['Start']:
                    merged_route = routes[start_point] + routes[end_point][::-1]
                if 3 >= len(merged_route) > 0:
                    routes.append(merged_route)
                    routes.pop(start_point)
                    routes.pop(end_point)

        for route in routes:
            route.append(self.depot)
            route.insert(0, self.depot)

        final_route = routes[0]
        routes.pop(0)
        for route in routes:
            if len(route) > len(final_route):
                final_route = route

        for client in final_route[1:len(final_route) - 1]:
            client.set_scheduled(timeslot)

        self.route = final_route
        self.compute_route_length()
        return self.route

    def compute_route_length(self):
        length = 0

        for i in range(len(self.route) - 1):
            length += self.distance_calculator.get_travel_time(self.route[i].get_location(), self.route[i + 1].get_location())

            if self.route[i].get_location() is not self.depot:
                length += 60  # Add fixed time per stop, if needed

        self.total_distance = length
        return self.total_distance

    def get_solution(self):
        return self.get_route(), self.total_distance

    def get_route(self):
        return [client.get_location() for client in self.route]

    def is_feasible(self, client):
        old_clients = self.clients
        self.clients.append(client)
        solution = self.solve()
        self.clients = old_clients
        return client in solution

if __name__ == "__main__":
    clients = [
        Client('Wade White', 'Someren', ['2024-06-02_morning']),
        # Add more clients as needed
    ]
    api_key = "AIzaSyAn6k7bgguxLTkSCeZg5VAQVx9cZo8_Czo"
    algo = ClarkeWright(clients, api_key)
    algo.solve('2024-06-02_morning')
    print(algo.get_solution())
