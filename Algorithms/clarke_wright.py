import math

import pandas as pd
import numpy as np

from Algorithms.client import Client


def to_hours(minutes):
    hours = math.floor(minutes / 60)
    mins = int(minutes - (hours * 60))

    return f"{hours}h{mins}min"


class ClarkeWright:
    def __init__(self, clients):
        self.depot = clients[0]
        clients.pop(0)
        self.clients = clients

        self.route = None
        self.savings = None
        self.distances = None
        self.total_distance = 0

    def compute_savings(self):
        self.distances = pd.read_csv('..//Data//distance_matrix.csv', index_col=0)

        start = []
        end = []
        s = []

        for client_1 in self.clients:
            # skip the depot
            if client_1 is self.depot:
                continue
            for client_2 in self.clients:
                # skip the depot
                if client_2 is self.depot:
                    continue
                elif client_2 in start:
                    continue

                # calculate savings for each pair of clients
                if client_1 is not client_2:

                    print(client_1.get_location())
                    dist_1 = self.distances[self.depot.get_location()].loc[client_1.get_location()]
                    dist_2 = self.distances[self.depot.get_location()].loc[client_2.get_location()]
                    dist_clients = self.distances[client_1.get_location()].loc[client_2.get_location()]

                    s.append(dist_1 + dist_2 - dist_clients)
                    start.append(client_1)
                    end.append(client_2)

        # build dataframe
        savings = pd.DataFrame(data={'Start': start, 'End': end, 'Savings': s})
        savings.sort_values(by='Savings', ascending=False, inplace=True)

        # store
        self.savings = savings

        return self.savings

    def solve(self):
        savings = self.compute_savings()
        print(savings)

        routes = []

        for _, row in savings.iterrows():

            start_point = None
            end_point = None
            skip = False

            # check in which routes start and end are endpoints
            for i in range(len(routes)):
                if row['Start'] in routes[i] and row['End'] in routes[i]:
                    skip = True
                if routes[i][0] is row['Start'] or routes[i][-1] is row['Start']:
                    start_point = i

                if routes[i][0] is row['End'] or routes[i][-1] is row['End']:
                    end_point = i

            # if both are included in one route, skip
            if skip:
                continue
            # if both are not included, add new route
            if start_point is None and end_point is None:
                new_route = [row['Start'], row['End']]

                routes.append(new_route)

            # if one is not included, then add to existing route (only if route is not full yet)
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

            # if included in different routes, merge them
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
                elif merged_route[start_point][-1] is row['Start'] and routes[end_point][-1] is row['End']:
                    merged_route = routes[start_point] + routes[end_point][::-1]
                elif merged_route[start_point][-1] is row['End'] and routes[end_point][-1] is row['Start']:
                    merged_route = routes[start_point] + routes[end_point][::-1]

                # routes cannot contain more than 3 customers
                if 3 >= len(merged_route) > 0:
                    routes.append(merged_route)
                    routes.pop(start_point)
                    routes.pop(end_point)

        # final_route = []
        for route in routes:
            # final_route += route
            route.append(self.depot)
            route.insert(0, self.depot)

        # final_route.append(self.depot)
        # final_route.insert(0, self.depot)

        final_route = routes[0]
        routes.pop(0)

        # TODO: how to decide on final route if multiple (currently, take longest)
        for route in routes:
            if len(route) > len(final_route):
                final_route = route

        for client in final_route[1:len(final_route)-1]:
            print(client)
            client.set_scheduled()

        self.route = final_route
        self.compute_route_length()

        return self.route

    def compute_route_length(self):
        length = 0

        for i in range(len(self.route) - 1):
            length += self.distances[self.route[i].get_location()].loc[self.route[i+1].get_location()]

            if self.route[i].get_location() is not self.depot:
                length += 60

        self.total_distance = length

        return self.total_distance

    def get_solution(self):
        return self.get_route(), to_hours(self.total_distance)

    def get_route(self):
        route = []

        for client in self.route:
            route.append(client.get_location())

        return route

    def is_feasible(self, client):
        # init
        old_clients = self.clients
        self.clients.append(client)

        # solve
        solution = self.solve()

        # reset
        self.clients = old_clients

        return client in solution


if __name__ == "__main__":
    clients = []
    clients.append(Client('depot', 'Mierlo', None))
    clients.append(Client('a', 'Geldrop', None))
    clients.append(Client('b', 'Helmond', None))
    clients.append(Client('c', 'Someren', None))
    clients.append(Client('d', 'Deurne Vlierden', None))
    # algo = ClarkeWright(['Mierlo', 'Geldrop', 'Helmond', 'Someren', 'Deurne Vlierden'])
    algo = ClarkeWright(clients)
    algo.solve()
    print(algo.get_solution())
