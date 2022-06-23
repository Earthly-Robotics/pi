import math


def calculate_angle(x1, y1, x2, y2):
    """
    Calculates the angle between two vectors.

    :param x1: X-coordinate of the first vector.
    :param y1: Y-coordinate of the first vector.
    :param x2: X-coordinate of the second vector.
    :param y2: Y-coordinate of the second vector.
    """
    angle = math.acos((x1 * x2 + y1 * y2) / (
                (math.sqrt(math.pow(x1, 2) + math.pow(y1, 2))) * (math.sqrt(math.pow(x2, 2) + math.pow(y2, 2)))))
    return math.degrees(angle)


def calculate_percentage(y):
    """
    Calculates the percentage of y based on how far it is from the max-value of the y-axis.

    :param y: Y-coordinate of the joystick.
    """
    # forwards
    if 0 < y <= 2047:
        percentage_pos = math.floor((y / 2047) * 100)
        output = math.floor(percentage_pos)
    # backwards
    elif -400 > y >= -2047:
        percentage_pos = math.floor(((y + 400) / 1647) * 100)
        output = math.floor(percentage_pos)

    return output
