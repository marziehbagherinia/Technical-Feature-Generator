def bottom_of_interval(column, upper, lower, percentage = 20):
    located_in_interval_bottom = [0]*len(column)
    
    for i in range(len(column)):
        if column[i] < lower[i]:
            located_in_interval_bottom[i] = 1
            continue
        dist_from_bottom = (column[i] - lower[i])/(upper[i] - lower[i])
        located_in_interval_bottom[i] = 1 if dist_from_bottom < (percentage / 100) else 0

    return located_in_interval_bottom

def top_of_interval(column, upper, lower, percentage = 20):
    located_in_interval_top = [0]*len(column)
    
    for i in range(len(column)):
        if column[i] > upper[i]:
            located_in_interval_top[i] = 1
            continue
        dist_from_top = (upper[i] - column[i])/(upper[i] - lower[i])
        located_in_interval_top[i] = 1 if dist_from_top < (percentage / 100) else 0

    return located_in_interval_top

def interval_position(column, upper, lower):
    interval_position = [0]*len(column)
    
    for i in range(len(column)):
        if column[i] > upper[i] and column[i] > lower[i]:
            interval_position[i] = 1
        elif column[i] < upper[i] and column[i] < lower[i]:
            interval_position[i] = -1

    return interval_position