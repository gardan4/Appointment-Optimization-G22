import math

import pandas as pd
import numpy as np
import os

from Algorithms.client import Client


def to_hours(minutes):
    hours = math.floor(minutes / 60)
    mins = int(minutes - (hours * 60))

    return f"{hours}h{mins}min"


class ClarkeWright:
    def __init__(self, clients):
        self.depot = Client('depot', 'Mierlo', None)
        self.clients = clients

        self.route = None
        self.distances = None
        self.total_distance = 0

    def compute_savings(self, clients, path):
        '''
        Calculates the savings according to the original Clarke-Wright Savings Algorithm
        :param clients: List of clients for which we want to compute the savings
        :param path: Directory where the distance matrix is stored
        :return: Dataframe with the savings for each start and end point, sorted in decreasing order
        '''
        self.distances = pd.read_csv(path, index_col=0)

        start = []
        end = []
        s = []

        for client_1 in clients:
            # skip the depot
            if client_1 is self.depot:
                continue
            for client_2 in clients:
                # skip the depot
                if client_2 is self.depot:
                    continue
                elif client_2 in start:
                    continue

                # calculate savings for each pair of clients
                if client_1 is not client_2:

                    # print(client_1.get_location())
                    dist_1 = self.distances[self.depot.get_location()].loc[client_1.get_location()]
                    dist_2 = self.distances[self.depot.get_location()].loc[client_2.get_location()]
                    dist_clients = self.distances[client_1.get_location()].loc[client_2.get_location()]

                    s.append(dist_1 + dist_2 - dist_clients)
                    start.append(client_1)
                    end.append(client_2)

        # build dataframe
        savings = pd.DataFrame(data={'Start': start, 'End': end, 'Savings': s})
        savings.sort_values(by='Savings', ascending=False, inplace=True)

        return savings

    def solve(self, timeslot, path):
        '''
        Solves the original Clarke-Wright Savings Algorithm
        :param timeslot: string of the timeslot for which we want to compute the route
        :param path: directory where the distance matrix is stored
        :return: the schedule for the timeslot, and the total travel time of this route
        '''
        # get list of clients with availability in timeslot
        clients = []
        for client in self.clients:
            if timeslot in client.get_availability():
                clients.append(client)

        # If there is only one client, create a direct route
        if len(clients) == 1:
            # Load distances
            self.distances = pd.read_csv(path, index_col=0)
            single_route = [self.depot, clients[0], self.depot]
            clients[0].set_scheduled(timeslot)
            self.route = single_route
            self.compute_route_length()
            return self.route

        # compute savings for clients
        savings = self.compute_savings(clients, path)
        # print(savings)

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

        for client in final_route[1:len(final_route) - 1]:
            # print(client)
            client.set_scheduled(timeslot)

        self.route = final_route
        self.compute_route_length()

        return self.route

    def compute_route_length(self):
        '''
        Computes the duration required to complete a route
        :return: the sum of total travel times, including the time spent at each client
        '''
        length = 0

        for i in range(len(self.route) - 1):
            length += self.distances[self.route[i].get_location()].loc[self.route[i+1].get_location()]

            if self.route[i] is not self.depot:
                length += 60

        self.total_distance = length

        return self.total_distance

    def get_solution(self):
        return self.get_route(), to_hours(self.compute_route_length())

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

    def solve_2(self, customer, current_route, path):
        '''
        Solves the modified Clarke-Wright Savings Algorithm, adapted for online arrival of clients
        Needs to be solved for every timeslot in the client's availability
        :param customer: Client object to be scheduled
        :param current_route: Ordered list of the current schedule
        :param path: directory where the distance matrix is stored
        :return: Ordered list of the current schedule, including the new client
        '''
        self.distances = pd.read_csv(path, index_col=0)

        if len(current_route) == 2:
            current_route.insert(1, customer)
            self.route = current_route
            return current_route

        best_s, index = self.compute_savings_new(customer, current_route)

        #if best_s >= 0:
        current_route.insert(index, customer)

        self.route = current_route

        return current_route

    def compute_savings_new(self, customer, current_route):
        '''
        Computes the savings for the online adaptation of the Clarke-Wright Savings Algorithm
        :param customer: Client object to compute savings for
        :param current_route: Ordered list of the current schedule
        :return: Preferred savings and location in the current schedule
        '''
        if current_route is None:
            return 0, 1

        best_s = float('-inf')
        location = None

        for i in range(len(current_route) - 1):
            d_depot = self.distances[current_route[0].get_location()].loc[customer.get_location()]
            d_before = self.distances[current_route[i].get_location()].loc[customer.get_location()]
            d_after = self.distances[current_route[i + 1].get_location()].loc[customer.get_location()]
            d_neighbours = self.distances[current_route[i].get_location()].loc[current_route[i+1].get_location()]

            s = 2 * d_depot + d_neighbours - (d_before + d_after)

            if s >= best_s:
                best_s = s
                location = i + 1

        return best_s, location

    def is_recommended(self, customer, current_route):
        best_s, _ = self.compute_savings_new(customer, current_route)

        return best_s >= 0

if __name__ == "__main__":
    clients = []
    clients.append(Client('Wade White', 'Asten Heusden Ommel', ['2024-06-06_evening']))
    clients.append(Client('Wade Whasdite', 'Asten Heusden Ommel', ['2024-06-06_evening']))
    # clients.append(Client('Wade xc', 'Someren', ['2024-06-02_morning']))
    # clients.append(Client('b', 'Helmond', ['2024-05-16_morning', '2024-05-16_evening']))
    # clients.append(Client('c', 'Someren', ['2024-05-16_morning']))
    # clients.append(Client('d', 'Deurne Vlierden', ['2024-05-16_morning', '2024-05-16_evening']))
    # algo = ClarkeWright(['Mierlo', 'Geldrop', 'Helmond', 'Someren', 'Deurne Vlierden'])
    algo = ClarkeWright(clients)

    #algo.solve('2024-05-16_morning', '..\\Data\\distance_matrix.csv')
    # algo.solve('2024-05-16_morning', '..\\Data\\distance_matrix.csv')
    client_1 = Client('a', 'Someren', None)
    client_2 = Client('b', 'Geldrop', None)
    client_3 = Client('c', 'Helmond', None)
    solution = algo.solve_2(client_1, [algo.depot, algo.depot], '..\\Data\\distance_matrix.csv')
    print(algo.get_solution())
    solution = algo.solve_2(client_2, solution, '..\\Data\\distance_matrix.csv')
    print(algo.get_solution())
    solution = algo.solve_2(client_3, solution, '..\\Data\\distance_matrix.csv')

    algo.solve('2024-06-06_evening', '..\Data\distance_matrix.csv')

    print(algo.get_solution())
