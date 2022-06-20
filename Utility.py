import math


def calculate_angle(x1, y1, x2, y2):
    angle = math.acos((x1 * x2 + y1 * y2) / (
                (math.sqrt(math.pow(x1, 2) + math.pow(y1, 2))) * (math.sqrt(math.pow(x2, 2) + math.pow(y2, 2)))))
    return math.degrees(angle)


def calculate_percentage(y):
    # forwards
    if 0 < y <= 2047:
        percentage_pos = math.floor(((y) / 2047) * 100)
        output = math.floor(percentage_pos)
    # backwards
    elif -400 > y >= -2047:
        percentage_pos = math.floor(((y + 400) / 1647) * 100)
        output = math.floor(percentage_pos)

        return output
