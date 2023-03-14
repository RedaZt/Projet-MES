def calculateMakespan(machines, i, j):
    if j == 0:
        if i == 0:
            return 0
        return calculateMakespan(machines, i - 1, 0) + machines[i - 1][0]
    else:
        if i == 0:
            return machines[i][j - 1] + calculateMakespan(machines, i, j - 1)
        return max(
            calculateMakespan(machines, i - 1, j) + machines[i - 1][j],
            calculateMakespan(machines, i, j - 1) + machines[i][j - 1],
        )