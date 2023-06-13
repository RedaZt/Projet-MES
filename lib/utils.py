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

def calculateMakespanWithPreparation(machines, preparation, order, i, j):
    if j == 0:
        if i == 0:
            return preparation[i][order[j]][order[j]]
        return max(
            preparation[i][order[j]][order[j]],
            calculateMakespanWithPreparation(machines, preparation, order, i - 1, 0) + machines[i - 1][0]
        )
    else:
        if i == 0:
            return calculateMakespanWithPreparation(machines, preparation, order, i, j - 1) + machines[i][j - 1] + preparation[i][order[j - 1]][order[j]]
        return max(
            calculateMakespanWithPreparation(machines,preparation, order, i - 1, j) + machines[i - 1][j],
            calculateMakespanWithPreparation(machines,preparation, order, i, j - 1) + machines[i][j - 1] + preparation[i][order[j - 1]][order[j]],
        )
    
def prep(machines, preparation, order, i, j):
    if j == 0:
        if i == 0:
            return 0
        return max(
            0,
            calculateMakespanWithPreparation(machines, preparation, order, i - 1, 0) + machines[i - 1][0] - preparation[i][order[j]][order[j]]
        )
    else:
        if i == 0:
            return calculateMakespanWithPreparation(machines, preparation, order, i, j - 1) + machines[i][j - 1]
        return max(
            calculateMakespanWithPreparation(machines,preparation, order, i - 1, j) + machines[i - 1][j] - preparation[i][order[j - 1]][order[j]],
            calculateMakespanWithPreparation(machines,preparation, order, i, j - 1) + machines[i][j - 1],
        )

# def calculateMakespanWithBlockage(machines, preparation, order, i, j):
#     if j == 0:
#         if i == 0:
#             return 0
#         return calculateMakespanWithBlockage(machines, preparation, order, i - 1, j) + machines[i - 1][j]
#     else:
#         if i == 0:
#             return calculateMakespanWithBlockage(machines, preparation, order, i + 1, j - 1)
#         elif i != len(machines) - 1:
#             return max(
#                 calculateMakespanWithBlockage(machines,preparation, order, i - 1, j) + machines[i - 1][j],
#                 calculateMakespanWithBlockage(machines,preparation, order, i + 1, j - 1),
#             )
#         return max(
#                 calculateMakespanWithBlockage(machines,preparation, order, i, j - 1) + machines[i][j - 1],
#                 calculateMakespanWithBlockage(machines,preparation, order, i - 1, j) + machines[i - 1][j],
#         )
    
def calculateMakespanWithBlockage(machines, preparation, order, i, j):
    if j == 0:
        if i == 0:
            return preparation[i][order[j]][order[j]]
        return max(
            preparation[i][order[j]][order[j]],
            calculateMakespanWithBlockage(machines, preparation, order, i - 1, j) + machines[i - 1][j]
        )
    else:
        if i == 0:
            return max(
                calculateMakespanWithBlockage(machines, preparation, order, i + 1, j - 1) + preparation[i][order[j - 1]][order[j]],
                calculateMakespanWithBlockage(machines, preparation, order, i, j - 1) + machines[i][j - 1] + preparation[i][order[j - 1]][order[j]],  
            )
        elif i != len(machines) - 1:
            return max(
                calculateMakespanWithBlockage(machines,preparation, order, i - 1, j) + machines[i - 1][j],
                calculateMakespanWithBlockage(machines,preparation, order, i + 1, j - 1) + preparation[i][order[j - 1]][order[j]],
            )
        return max(
                calculateMakespanWithBlockage(machines,preparation, order, i, j - 1) + machines[i][j - 1] + preparation[i][order[j - 1]][order[j]],
                calculateMakespanWithBlockage(machines,preparation, order, i - 1, j) + machines[i - 1][j],
        )
    
def prepBlo(machines, preparation, order, i, j):
    if j == 0:
        if i == 0:
            return 0
        return max(
            0,
            calculateMakespanWithBlockage(machines, preparation, order, i - 1, j) + machines[i - 1][j] - preparation[i][order[j]][order[j]]
        )
    else:
        if i == 0:
            return max(
                calculateMakespanWithBlockage(machines, preparation, order, i + 1, j - 1),
                calculateMakespanWithBlockage(machines, preparation, order, i, j - 1) + machines[i][j - 1],  
            )
        elif i != len(machines) - 1:
            return max(
                calculateMakespanWithBlockage(machines,preparation, order, i - 1, j) + machines[i - 1][j] - preparation[i][order[j - 1]][order[j]],
                calculateMakespanWithBlockage(machines,preparation, order, i + 1, j - 1),
            )
        return max(
                calculateMakespanWithBlockage(machines,preparation, order, i, j - 1) + machines[i][j - 1],
                calculateMakespanWithBlockage(machines,preparation, order, i - 1, j) + machines[i - 1][j] - preparation[i][order[j - 1]][order[j]],
        )