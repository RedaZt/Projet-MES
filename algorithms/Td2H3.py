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