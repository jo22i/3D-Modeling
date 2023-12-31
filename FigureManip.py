from math import sin, cos, pi

def ChangeVector(change_matrix: list, vector: list):
    new_vector = [0]*len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return new_vector


def get_vector(dots: list):
    return [dots[0], dots[1], dots[2], 1]


def ToRadian(angle: float):
    return (angle * pi) / 180


def get_move_matrix(dx: float = 0, dy: float = 0, dz: float = 0):
    return [[1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]


def get_scale_matrix(kx: float = 0, ky: float = 0, kz: float = 0):
    return [[kx, 0, 0, 0],
            [0, ky, 0, 0],
            [0, 0, kz, 0],
            [0, 0, 0, 1]]


def get_rotate_matrix_X(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)
        
    return  [[1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]]


def get_rotate_matrix_Y(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)

    return [[cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]]


def get_rotate_matrix_Z(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)

    return [[cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0 , 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]