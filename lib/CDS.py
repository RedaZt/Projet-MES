from .Johnson import Johnson
from .utils import calculateMakespan
# from Johnson import Johnson
# from utils import calculateMakespan
import pprint

class CDS:
    def __init__(self, machines) -> None:
        self.machines = machines
        self.order = self.fun()

    def fun(self):
        nMachines = len(self.machines)
        nJobs = len(self.machines[0]) 
        d = {}
        for k in range(1, nMachines):
            fictitiousMachine1 = [0 for _ in range(nJobs)]
            fictitiousMachine2 = [0 for _ in range(nJobs)]
            for machine in range(k):
                for job in range(nJobs):
                    fictitiousMachine1[job] += self.machines[machine][job]

            for machine in range(nMachines - k, nMachines):
                for job in range(nJobs):
                    fictitiousMachine2[job] += self.machines[machine][job]

            solution = Johnson([fictitiousMachine1, fictitiousMachine2])

            orderedMachines = []
            for i in range(len(self.machines)):
                orderedJobs = []
                for j in solution.order:
                    orderedJobs += self.machines[i][j],
                orderedMachines += orderedJobs,
            cmax = calculateMakespan(orderedMachines, nMachines - 1, nJobs - 1) + orderedMachines[-1][-1]
            d[cmax] = solution.order
            # print(cmax, solution.order)
        #     print(cmax)
        #     print("---------")
        # pprint.pprint(d)
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
# machines = [
#     [11, 13, 20, 9, 11],
#     [12, 15, 10, 12, 18],
#     [20, 18, 12, 20, 15],
# ]     
# machines = [
#     [54, 83, 15, 71, 77, 36, 53, 38, 27, 87, 76, 91, 14, 29, 12, 77, 32, 87, 68, 94],
#     [79, 3, 11, 99, 56, 70, 99, 60, 5, 56, 3, 61, 73, 75, 47, 14, 21, 86, 5, 77],
#     [16, 89, 49, 15, 89, 45, 60, 23, 57, 64, 7, 1, 63, 41, 63, 47, 26, 75, 77, 40],
#     [66, 58, 31, 68, 78, 91, 13, 59, 49, 85, 85, 9, 39, 41, 56, 40, 54, 77, 51, 31],
#     [58, 56, 20, 85, 53, 35, 53, 41, 69, 13, 86, 72, 8, 49, 47, 87, 58, 18, 68, 28],
# ]
# # 1314
# machines = [
#     [4, 3, 1, 3],
#     [3, 7, 2, 4],
#     [7, 2, 4, 3],
#     [2, 8, 3, 7],
#     [8, 5, 7, 2],
# ]
# example = CDS(machines)
# print(example.order)
