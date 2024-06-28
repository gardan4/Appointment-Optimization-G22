import sys
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

# tested with Gurobi v10.0.3
class Timeslot():
    def __init__(self, name, cap, depot):
        self.name = name
        self.cap = cap
        self.depot = depot

    def __str__(self):
        return f"Timeslot: {self.name}\n  Capacity: {self.cap}\n  Depot: {self.depot}"

class Job():
    def __init__(self, name, duration, coveredBy):
        self.name = name
        self.duration = duration
        self.coveredBy = coveredBy

    def __str__(self):
        about = f"ClientJob: {self.name}\n  Duration: {self.duration}\n  Covered by: "
        about += ", ".join([t.name for t in self.coveredBy])
        return about
    
class Client():
    def __init__(self, name, loc, job, tStart, tEnd, tDue):
        self.name = name
        self.loc = loc
        self.job = job
        self.tStart = tStart
        self.tEnd = tEnd
        self.tDue = tDue

    def __str__(self):
        coveredBy = ", ".join([t.name for t in self.job.coveredBy])
        return f"Client: {self.name}\n  Location: {self.loc}\n  ClientJob: {self.job.name}\n  Duration: {self.job.duration}\n  Covered by: {coveredBy}\n  Start time: {self.tStart}\n  End time: {self.tEnd}\n  Due time: {self.tDue}"


# Read Excel workbook
excel_file ="https://github.com/gardan4/Appointment-Optimization-G22/raw/main/Data/Sample%20Data%20for%20MILP.xlsx"
df = pd.read_excel(excel_file, sheet_name='Timeslots full')
df = df.rename(columns={df.columns[0]: "name", df.columns[1]: "cap", df.columns[2]: "depot"})

df1 = df.drop(df.columns[3:], axis=1).drop(df.index[[0]])
# Create Timeslot objects
timeslots = [Timeslot(*row) for row in df1.itertuples(index=False, name=None)]
# print(df1)

# Read job data
jobs=[]
for j in range(3, len(df.columns)):
    coveredBy = [t for i, t in enumerate(timeslots) if df.iloc[1+i,j]==1]
    thisJob = Job(df.iloc[1:,j].name, df.iloc[0,j], coveredBy)
    jobs.append(thisJob)

# Read location data
df_locations = pd.read_excel(excel_file, sheet_name='Locations', index_col=0) #, skiprows=1, index_col=0)

# Extract locations and initialize distance dictionary
locations = df_locations.index
dist = {(l, l): 0 for l in locations}

# Populate distance dictionary
for i, l1 in enumerate(locations):
    for j, l2 in enumerate(locations):
        if i < j:
            dist[l1, l2] = df_locations.iloc[i, j]
            dist[l2, l1] = dist[l1, l2]

# Read client data
df_clients = pd.read_excel(excel_file, sheet_name='Clients')

clients = []
for i, c in enumerate(df_clients.iloc[:, 0]):
    job_name = df_clients.iloc[i, 2]

    # Find the corresponding Job object
    matching_job = next((job for job in jobs if job.name == job_name), None)

    if matching_job is not None:
        # Create Client object using corresponding Job object
        this_client = Client(c, df_clients.iloc[i, 1], matching_job, *df_clients.iloc[i, 3:])
        clients.append(this_client)

def solve_trs0(timeslots, clients, dist):
    # Build useful data structures
    K = [k.name for k in timeslots]
    C = [j.name for j in clients]
    J = [j.loc for j in clients]
    L = list(set([l[0] for l in dist.keys()]))
    D = list(set([t.depot for t in timeslots]))
    cap = {k.name: k.cap for k in timeslots}
    loc = {j.name: j.loc for j in clients}
    depot = {k.name: k.depot for k in timeslots}
    canCover = {j.name: [k.name for k in j.job.coveredBy] for j in clients}
    dur = {j.name: j.job.duration for j in clients}
    tStart = {j.name: j.tStart for j in clients}
    tEnd = {j.name: j.tEnd for j in clients}


    ### Create model
    m = gp.Model("trs0")

    m.setParam('Seed', 22)
    m.setParam('Threads', 1)
    #m.setParam('PoolSolutions', 10)

    ### Decision variables
    # Client-timeslot assignment
    x = m.addVars(C, K, vtype=GRB.BINARY, name="x")

    # Timeslot assignment
    u = m.addVars(K, vtype=GRB.BINARY, name="u")

    # Edge-route assignment
    y = m.addVars(L, L, K, vtype=GRB.BINARY, name="y")

    # Start time of service
    t = m.addVars(L, ub=480, name="t")

    tr = m.addVars(L,L,K, vtype = GRB.CONTINUOUS, name= "tr")
    ### Constraints

    # A timeslot must be assigned to a job (1)
    m.addConstrs((gp.quicksum(x[j, k] for k in canCover[j]) == 1 for j in C), name="assignToJob")

    # Timselot capacity constraints (2)
    capLHS = {k: gp.quicksum(dur[j] * x[j, k] for j in C) + \
                 gp.quicksum(dist[i, j] * y[i, j, k] for i in L for j in L) for k in K}
    m.addConstrs((capLHS[k] <= cap[k] * u[k] for k in K), name="timeslotCapacity")

    # Timeslot tour constraints (3 and 4)
    m.addConstrs((y.sum('*', loc[j], k) == x[j, k] for k in K for j in C), \
                 name="timeslotTour1")
    m.addConstrs((y.sum(loc[j], '*', k) == x[j, k] for k in K for j in C), \
                 name="timeslotTour2")
    
    # Travel time constraint (5)
    M = {(i, j): 480 + dist[loc[i], loc[j]] for i in C for j in C}
    m.addConstrs((tr[loc[i],loc[j],k] >= dist[loc[i],loc[j]] - M[i,j] * (1-gp.quicksum(y[loc[i],loc[j],k] for k in K))\
                 for k in K for i in C for j in C), \
                 name="traveltime1")

    # Same depot constraints (6 and 7)
    m.addConstrs((gp.quicksum(y[j, depot[k], k] for j in J) == u[k] for k in K), \
                 name="sameDepot1")
    m.addConstrs((gp.quicksum(y[depot[k], j, k] for j in J) == u[k] for k in K), \
                 name="sameDepot2")
    
    # Temporal constraints (8) for customer locations
    M = {(i, j): 480 + dur[i] + dist[loc[i], loc[j]] for i in C for j in C}
    m.addConstrs((t[loc[j]] >= t[loc[i]] + dur[i] + dist[loc[i], loc[j]] \
                  - M[i, j] * (1 - gp.quicksum(y[loc[i], loc[j], k] for k in K)) \
                  for i in C for j in C), name="tempoCustomer")

    # Temporal constraints (8) for depot locations
    M = {(i, j): 480 + dist[i, loc[j]] for i in D for j in C}
    m.addConstrs((t[loc[j]] >= t[i] + dist[i, loc[j]] \
                  - M[i, j] * (1 - y.sum(i, loc[j], '*')) for i in D for j in C), \
                 name="tempoDepot")
    
    # Time window constraints (9 and 10)
    m.addConstrs((t[loc[j]] >= tStart[j] for j in C), name="timeWinA")
    m.addConstrs((t[loc[j]] <= tEnd[j] for j in C), name="timeWinB")

    ### Objective function
    M = 6100

    m.setObjective(gp.quicksum(0.01 * M * tr[i,j,k] for i in L for j in L for k in K), GRB.MINIMIZE)
    m.write("TRS0.lp")
    m.optimize()

    status = m.Status
    if status in [GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED]:
        print("Model is either infeasible or unbounded.")
        sys.exit(0)
    elif status != GRB.OPTIMAL:
        print("Optimization terminated with status {}".format(status))
        sys.exit(0)

    ### Print results
    # Assignments
    print("")
    for j in clients:
        for k in K:
            if x[j.name, k].X > 0.5:
                jobStr = f"{k} assigned to {j.name} ({j.job.name}) in {j.loc}. Start at t={t[j.loc].X:.2f}."
        print(jobStr)
    # Timeslots
    print("")
    for k in timeslots:
        if u[k.name].X > 0.5:
            cur = k.depot
            route = k.depot
            while True:
                for j in clients:
                    if y[cur,j.loc,k.name].X > 0.5:
                        route += (f" -> {j.loc} (dist={dist[cur, j.loc]}, t={t[j.loc].X:.2f},"
                                  f" proc={j.job.duration}, a={tStart[j.name]}, b={tEnd[j.name]})")
                        cur = j.loc
                for i in D:
                    if y[cur,i,k.name].X > 0.5:
                        route += " -> {} (dist={})".format(i,dist[cur, i])
                        cur = i
                        break
                if cur == k.depot:
                    break
            print("{}'s route: {}".format(k.name, route))
        else:
            print("{} is not used".format(k.name))

            
    # Utilization
    print("")
    for k in K:
        used = capLHS[k].getValue()
        total = cap[k]
        util = used / cap[k] if cap[k] > 0 else 0
        print("{}'s utilization is {:.2%} ({:.2f}/{:.2f})".format(k, util, used, cap[k]))
    totUsed = sum(capLHS[k].getValue() for k in K)
    totCap = sum(cap[k] for k in K)
    totUtil = totUsed / totCap if totCap > 0 else 0
    print("Total timeslot utilization is {:.2%} ({:.2f}/{:.2f})".format(totUtil, totUsed, totCap))
        
    m.dispose()
    gp.disposeDefaultEnv()

def printScen(scenStr):
    sLen = len(scenStr)
    print("\n" + "*"*sLen + "\n" + scenStr + "\n" + "*"*sLen + "\n")

if __name__ == "__main__":
    # Base model
    printScen("Solving base scenario model")
    solve_trs0(timeslots, clients, dist)
