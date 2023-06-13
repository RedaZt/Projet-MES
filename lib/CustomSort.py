class Td2H1:
    def __init__(self, machines) -> None:
        self.machines = machines
        self.order = self.totalTime()

    def totalTime(self):
        totalTimes = []
        for i in range(len(self.machines[0])):
            total = 0
            for j in range(len(self.machines)):
                total += self.machines[j][i]
            totalTimes += total,
        order = []
        for i in range(len(totalTimes)):
            indexMax = totalTimes.index(max(totalTimes))
            order += indexMax,
            totalTimes[indexMax] = 0
        
        return order


class Td2H2:
    def __init__(self, deadlines) -> None:
        self.deadlines = deadlines
        self.order = self.totalTime()

    def totalTime(self):
        order = []
        for i in range(len(self.deadlines)):
            indexMax = self.deadlines.index(max(self.deadlines))
            order += indexMax,
            self.deadlines[indexMax] = 0
        return order


class Td2H3:
    def __init__(self, machines, deadlines) -> None:
        self.machines = machines
        self.deadlines = deadlines
        self.order = self.totalTime()

    def totalTime(self):
        order = []
        results = []

        for i in range(len(self.machines[0])):
            total = 0
            for j in range(len(self.machines)):
                total += self.machines[j][i]
            results += abs(total - self.deadlines[i]),
        
        for i in range(len(results)):
            indexMax = results.index(max(results))
            order += indexMax,
            results[indexMax] = -1

        return order
    

class TPj:
    def __init__(self, machines, preparations) -> None:
        self.machines = machines
        self.preparations = preparations
        self.order = self.orderMachinesByTPj()
    

    def orderMachinesByTPj(self):
        nMachines = len(self.machines)
        nJobs = len(self.machines[0])
        results = [sum(self.machines[j][i] + self.preparations[j][i][i] for j in range(nMachines)) for i in range(nJobs)]        
        
        order = []
        for i in range(nJobs):
            indexMax = results.index(max(results))
            order += indexMax,
            results[indexMax] = 0
        
        return order


class CustomSort:
    def __init__(self, machines, preparations, order) -> None:
        self.machines = machines
        self.preparations = preparations
        self.order = order


# machines = [
#     [4, 3, 5, 2, 7, 3, 6, 7, 5],
#     [8, 5, 2, 4, 3, 7, 6, 8, 9],
#     [3, 7, 4, 7, 5, 6, 6, 8, 3],
# ]

# deadlines = [15, 10, 20, 21, 22, 17, 16, 8, 13]

# exemple = Td2H1(machines)
# print(" -> ".join(f"J{x + 1}" for x in exemple.order))