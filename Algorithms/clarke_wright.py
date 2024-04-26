import math

import pandas as pd
import numpy as np

class ClarkeWright:
    def __init__(self, clients):
        self.clients = clients
        self.depot = clients[0]

        self.route = None
        self.savings = None
        self.distances = None
        self.total_distance = 0

    def compute_savings(self):
        self.distances = pd.read_csv('..//res//distance_matrix.csv', index_col=0)

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

                    dist_1 = self.distances[self.depot].loc[client_1]
                    dist_2 = self.distances[self.depot].loc[client_2]
                    dist_clients = self.distances[client_1].loc[client_2]

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

            # if one is not included, then add to existing route
            elif start_point is None or end_point is None:
                if start_point is None:
                    if routes[end_point][0] is row['End']:
                        routes[end_point].insert(0, row['Start'])
                    else:
                        routes[end_point].append(row['Start'])

                elif routes[start_point][0] is row['Start']:
                    routes[start_point].insert(0, row['End'])
                else:
                    routes[start_point].append(row['End'])

            # if included in different routes, merge them
            elif start_point is not end_point:
                merged_route
                if routes[start_point][-1] is row['Start'] and routes[end_point][0] is row['End']:
                    merged_route = routes[start_point] + routes[end_point]
                elif routes[end_point][-1] is row['Start'] and routes[start_point][0] is row['End']:
                    merged_route = routes[end_point] + routes[start_point]
                elif routes[start_point][-1] is row['End'] and routes[end_point][0] is row['Start']:
                    merged_route = routes[start_point] + routes[end_point]
                elif routes[end_point][-1] is row['End'] and routes[start_point][0] is row['Start']:
                    merged_route = routes[end_point] + routes[start_point]
                elif routes[start_point][0] is row['Start'] and routes[end_point][0] is row['End']:
                    merged_route = routes[start_point].reverse + routes[end_point]
                elif routes[start_point][0] is row['End'] and routes[end_point][0] is row['Start']:
                    merged_route = routes[start_point].reverse() + routes[end_point]
                elif merged_route[start_point][-1] is row['Start'] and routes[end_point][-1] is row['End']:
                    merged_route = routes[start_point] + routes[end_point].reverse()
                elif merged_route[start_point][-1] is row['End'] and routes[end_point][-1] is row['Start']:
                    merged_route = routes[start_point] + routes[end_point].reverse()

                routes.append(merged_route)
                routes.pop(start_point)
                routes.pop(end_point)

        for route in routes:
            route.append(self.depot)
            route.insert(0, self.depot)

        return routes

    def get_solution(self):
        return self.route, self.total_distance

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
    algo = ClarkeWright(['Mierlo', 'Geldrop', 'Helmond', 'Someren', 'Deurne Vlierden'])
    print(algo.solve())
