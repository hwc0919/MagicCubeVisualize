# ###################################### #
#          Cube Representation           #
# ###################################### #
#
#
# Unfold the cube to 2D:
#
#              Top
#
# Back  Left  Front  Right
#
#             Bottom
#
#
#                 A B A
#                 B * B
#                 A B A
#
# A B A   A B A   A B A   A B A
# B * B   B * B   B * B   B * B
# A B A   A B A   A B A   A B A
#
#                 A B A
#                 B * B
#                 A B A
#
#
# Use 3-dimensional array of str to represent a cube with details
# detail_cube[i][j][k] = s:
# On face i, line j, index k
# s[0]: A, B or F. A represents corner block, B represents edge block, F represents face center
# s[1]: which block in its kind. There are 8 corner blocks, 12 edge blocks, and 6 face blocks
# s[2]: Which face it belongs to, at the beginning.


def detailed_cube():
    return [
        # BACK
        [['A00', 'B00', 'A10'],
         ['B40', 'F00', 'B50'],
         ['A40', 'B80', 'A50']],
        # LEFT
        [['A11', 'B11', 'A21'],
         ['B51', 'F11', 'B61'],
         ['A51', 'B91', 'A61']],
        # FRONT
        [['A22', 'B22', 'A32'],
         ['B62', 'F02', 'B72'],
         ['A62', 'BA2', 'A72']],
        # RIGHT
        [['A33', 'B33', 'A03'],
         ['B73', 'F13', 'B43'],
         ['A73', 'BB3', 'A43']],
        # TOP
        [['A14', 'B04', 'A04'],
         ['B14', 'F24', 'B34'],
         ['A24', 'B24', 'A34']],
        # BOTTOM
        [['A65', 'BA5', 'A75'],
         ['B95', 'F25', 'BB5'],
         ['A55', 'B85', 'A45']]
    ]


def simple_cube():
    return [
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]],
        [[2, 2, 2],
         [2, 2, 2],
         [2, 2, 2]],
        [[3, 3, 3],
         [3, 3, 3],
         [3, 3, 3]],
        [[4, 4, 4],
         [4, 4, 4],
         [4, 4, 4]],
        [[5, 5, 5],
         [5, 5, 5],
         [5, 5, 5]]]


# Corner cells that belongs to the same block
def adjacent_corners():
    return [
        # Initial A0
        [(0, 0, 0), (3, 0, 2), (4, 0, 2)],
        # Initial A1
        [(0, 0, 2), (1, 0, 0), (4, 0, 0)],
        # Initial A2
        [(1, 0, 2), (2, 0, 0), (4, 2, 0)],
        # Initial A3
        [(2, 0, 2), (3, 0, 0), (4, 2, 2)],
        # Initial A4
        [(0, 2, 0), (3, 2, 2), (5, 2, 2)],
        # Initial A5
        [(0, 2, 2), (1, 2, 0), (5, 2, 0)],
        # Initial A6
        [(1, 2, 2), (2, 2, 0), (5, 0, 0)],
        # Initial A7
        [(2, 2, 2), (3, 2, 0), (5, 0, 2)],
    ]


# Edge cells that belongs to the same block
def adjacent_edges():
    return [
        # Initial B0
        [(0, 0, 1), (4, 0, 1)],
        # Initial B1
        [(1, 0, 1), (4, 1, 0)],
        # Initial B2
        [(2, 0, 1), (4, 2, 1)],
        # Initial B3
        [(3, 0, 1), (4, 1, 2)],
        # Initial B4
        [(0, 1, 0), (3, 1, 2)],
        # Initial B5
        [(0, 1, 2), (1, 1, 0)],
        # Initial B6
        [(1, 1, 2), (2, 1, 0)],
        # Initial B7
        [(2, 1, 2), (3, 1, 0)],
        # Initial B8
        [(0, 2, 1), (5, 2, 1)],
        # Initial B9
        [(1, 2, 1), (5, 1, 0)],
        # Initial BA (B10)
        [(2, 2, 1), (5, 0, 1)],
        # Initial BB (B11)
        [(3, 2, 1), (5, 1, 2)],
    ]
