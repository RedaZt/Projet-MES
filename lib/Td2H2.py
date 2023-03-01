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