from .Johnson import Johnson
from .utils import calculateM
# from Johnson import Johnson
# from utils import calculateM

class CDS:
    def __init__(self, machines) -> None:
        self.machines = machines
        self.order = self.fun()

    def fun(self):
        nMachines = len(self.machines)
        nJobs = len(self.machines[0])
        d = {}
        for k in range(1, nMachines):
            fictitiousMachine1 = [0 for i in range(nJobs)]
            fictitiousMachine1 = [0 for i in range(nJobs)]
            for machine in range(k):
                for job in range(nJobs):
                    fictitiousMachine1[job] += self.machines[machine][job]

            for machine in range(nMachines - k, nMachines):
                for job in range(nJobs):
                    fictitiousMachine1[job] += self.machines[machine][job]

            solution = Johnson([fictitiousMachine1, fictitiousMachine1])
            # print(" -> ".join(f"J{x + 1}" for x in solution.order))

            orderedMachines = []
            for i in range(len(self.machines)):
                orderedJobs = []
                for j in solution.order:
                    orderedJobs += self.machines[i][j],
                orderedMachines += orderedJobs,

            results = []
            for i in range(nMachines):
                result = []
                for j in range(nJobs):
                    result += ((calculateM(orderedMachines, i, j), orderedMachines[i][j]),)
                    # result += ((self.calculateM(orderedMachines, i, j), orderedMachines[i][j]),)
                results += (result,)
            # print(results[-1][-1][0] + results[-1][-1][1])
            cmax = results[-1][-1][0] + results[-1][-1][1]
            d[cmax] = solution.order
        # print(d)
        # exit()
        return d[min(d.keys())]


# machines = [
#     [5, 2, 3, 6, 7],
#     [2, 4, 4, 5, 3],
#     [3, 2, 5, 4, 2],
# ]     
# machines = [
#     [16, 14, 13, 19, 15],
#     [18, 10, 20, 15, 16],
#     [12, 11, 15, 19, 16],
# ]     
# example = CDS(machines)
# print(example.order)
