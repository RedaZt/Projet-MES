class Johnson:
    def __init__(self, machines) -> None:
        self.machines = machines
        self.order = self.johnson()

    def johnson(self):
        m1, m2 = self.machines
        ncells = len(m1)
        start, end = [], []

        for i in range(ncells):
            minM1 = min(m1)
            minM2 = min(m2)

            if minM1 <= minM2:
                indexMinM = m1.index(minM1)
                start += indexMinM,
            else:    
                indexMinM = m2.index(minM2)
                end += indexMinM,
            
            m1[indexMinM] = m1[indexMinM] + 9**10
            m2[indexMinM] = m2[indexMinM] + 9**10

        order = start + end[::-1]

        return order

# machines = [
#     [5, 2, 3, 6, 7],
#     [2, 4, 4, 5, 3]
# ]
# machines = [
#     [8, 11, 5, 9],
#     [7, 16, 10, 8]
# ]
# example = Johnson(machines)
# print(" -> ".join(f"J{x + 1}" for x in example.order))