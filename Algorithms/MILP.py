import gurobipy as gp
from gurobipy import GRB
import random

# Data
num_clients = 10
num_days = 7
timeslots_per_day = 2
clients = list(range(1, num_clients + 1))
days = list(range(1, num_days + 1))
timeslots = list(range(1, timeslots_per_day + 1))

# Random travel times between clients
travel_times = {(i, j): random.randint(10, 60) for i in clients for j in clients if i != j}

# Gurobi model
model = gp.Model("client_scheduling")

# Decision variables
x = {}  # Client assignment variable
t = {}  # Travel time variable

for i in clients:
    for d in days:
        for time_slot in timeslots:
            x[i, d, time_slot] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{d}_{time_slot}")
    for j in clients:
        if i != j:
            t[i, j] = model.addVar(vtype=GRB.CONTINUOUS, name=f"t_{i}_{j}")

# Constraints
for i in clients:
    model.addConstr(gp.quicksum(x[i, d, time_slot] for d in days for time_slot in timeslots) == 1)

for d in days:
    for time_slot in timeslots:
        model.addConstr(gp.quicksum(x[i, d, time_slot] for i in clients) <= 1)

for i in clients:
    for j in clients:
        if i != j:
            for d in days:
                for time_slot in timeslots:
                    model.addConstr(t[i, j] >= travel_times[i, j] * (x[i, d, time_slot] + x[j, d, time_slot] - 1))

# Objective Function
model.setObjective(gp.quicksum(t[i, j] for i in clients for j in clients if i != j), GRB.MINIMIZE)

# Solve the optimization problem
model.optimize()

if model.status == GRB.OPTIMAL:
    print("Optimal solution found!")
    for i in clients:
        for d in days:
            for time_slot in timeslots:
                if x[i, d, time_slot].x > 0.5:
                    print(f"Client {i} scheduled on day {d}, timeslot {time_slot}")
else:
    print("No optimal solution found.")



