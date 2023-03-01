def calculateM(machines, i, j):
    if j == 0:
        if i == 0:
            return 0
        return calculateM(machines, i - 1, 0) + machines[i - 1][0]
    else:
        if i == 0:
            return machines[i][j - 1] + calculateM(machines, i, j - 1)
        return max(
            calculateM(machines, i - 1, j) + machines[i - 1][j],
            calculateM(machines, i, j - 1) + machines[i][j - 1],
        )