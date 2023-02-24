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


machines = [
    [4, 3, 5, 2, 7, 3, 6, 7, 5],
    [8, 5, 2, 4, 3, 7, 6, 8, 9],
    [3, 7, 4, 7, 5, 6, 6, 8, 3],
]
exemple = Td2H1(machines)
print(" -> ".join(f"J{x + 1}" for x in exemple.order))