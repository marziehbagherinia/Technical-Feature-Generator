def cross_line_from_bottom(column, line):
    crossed = [0] * len(column)
    for i in range(1, len(column)):
        if column[i-1] <= line[i-1] and column[i] > line[i]:
            crossed[i] = 1

    return crossed

def cross_line_from_above(column, line):
    crossed = [0] * len(column)
    for i in range(1, len(column)):
        if column[i-1] >= line[i-1] and column[i] < line[i]:
            crossed[i] = 1

    return crossed