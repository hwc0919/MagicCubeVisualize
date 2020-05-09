import copy
import random

from .cube_matrix import detailed_cube, adjacent_corners, adjacent_edges


class Cube(object):
    functions = ['rotate_{}_{}'.format(face, direction)
                 for face in ['back', 'front', 'left', 'right', 'top', 'bottom', 'XY', 'YZ', 'XZ']
                 for direction in ['clock', 'anti']]

    op_names = ['B0', 'B1', 'F0', 'F1', 'L0', 'L1', 'R0', 'R1', 'T0', 'T1', 'Z0', 'Z1']
    # op_names = ['B0', 'B1', 'F0', 'F1', 'L0', 'L1', 'R0', 'R1', 'T0', 'T1', 'Z0', 'Z1',
    #             'XY0', 'XY1', 'YZ0', 'YZ1', 'XZ0', 'XZ1']
    operations = {op: func for op, func in zip(op_names, functions)}

    def __init__(self):
        self.cube = detailed_cube()
        self.original_cube = detailed_cube()

        # Adjacent corners
        self.corners = adjacent_corners()
        # Adjacent edges
        self.edges = adjacent_edges()
        # Record operation history
        self.history = []

    def is_valid(self):
        """Check if the cube is in valid state"""
        cube = self.cube
        # Check block type
        for f in range(6):
            for r in range(3):
                for c in range(3):
                    state = cube[f][r][c]
                    # check face center
                    if r == c == 1:
                        if state[0] != 'F' or state[-1] != str(f):
                            print('error at ({},{},{}), should be {}, but {}'.format(
                                f, r, c, 'F*' + str(f), state))
                            return False
                    elif (r + c) & 1:
                        if state[0] != 'B':
                            print('error at ({},{},{}), should be {}, but {}'.format(
                                f, r, c, 'B*' + str(f), state))
                            return False
                    else:
                        if state[0] != 'A':
                            print('error at ({},{},{}), should be {}, but {}'.format(
                                f, r, c, 'A*' + str(f), state))
                            return False

        # Check adjacent corner blocks
        for i, corner in enumerate(self.corners):
            f0, r0, c0 = corner[0]
            for f, r, c in corner[1:]:
                if not cube[f0][r0][c0][:2] == cube[f][r][c][:2]:
                    print("error at ({},{},{})  corner doesn't match".format(f, r, c))
                    return False

        # Check adjacent edge blocks:
        for i, edge in enumerate(self.edges):
            (f0, r0, c0), (f1, r1, c1) = edge
            if not cube[f0][r0][c0][:2] == cube[f1][r1][c1][:2]:
                print("error at ({},{},{}) edge doesn't match".format(f0, r0, c0))
                return False

        return True

    def reset(self):
        """Reset cube to original state"""
        self.history.clear()
        self.cube = copy.deepcopy(self.original_cube)

    def is_reset(self):
        """Check if cube has been reset"""
        return self.cube == self.original_cube

    def shuffle(self, times=20):
        """Shuffle cube"""
        for i in range(times):
            op_name = random.choice(Cube.op_names)
            self.take_action(op_name)
        return True

    @staticmethod
    def to_string(cube):
        res = ''
        for f in range(6):
            for r in range(3):
                res += ''.join(cube[f][r])
        return res

    @staticmethod
    def reverse_op(op):
        """Get the name of reversed op"""
        return op[:-1] + str(1 - int(op[-1]))

    def recover(self):
        """Recover the cube along operation history"""
        reverse_history = [Cube.reverse_op(op) for op in self.history[::-1]]
        self.history.clear()
        for reverse_op in reverse_history:
            self.take_action(reverse_op, record=False)
        if self.is_reset():
            print('Recover success')
            return True
        else:
            raise Exception('Recover failed')

    def go_back(self):
        """Go back for 1 step"""
        if not self.history:
            return False
        reverse_op = Cube.reverse_op(self.history.pop())
        self.take_action(reverse_op, record=False)
        if self.is_reset():
            self.history.clear()
        return True

    # ######################### #
    #     Rotate Operations     #
    # ######################### #

    @staticmethod
    def rotate_clock(f):
        """Rotate certain face in clockwise direction"""
        f[0][0], f[0][1], f[0][2], f[1][2], f[2][2], f[2][1], f[2][0], f[1][0] = \
            f[2][0], f[1][0], f[0][0], f[0][1], f[0][2], f[1][2], f[2][2], f[2][1]

    @staticmethod
    def rotate_anti(f):
        """Rotate certain face in anti-clockwise direction"""
        f[0][0], f[0][1], f[0][2], f[1][2], f[2][2], f[2][1], f[2][0], f[1][0] = \
            f[0][2], f[1][2], f[2][2], f[2][1], f[2][0], f[1][0], f[0][0], f[0][1]

    def take_action(self, op_name, record=True):
        if op_name not in Cube.op_names:
            return False
        if record:
            if self.history and self.history[-1] == Cube.reverse_op(op_name):
                self.history.pop()
            else:
                self.history.append(op_name)
        getattr(self, Cube.operations[op_name])()
        return True

    #
    # Rotate Back
    #

    def rotate_back_clock(self):
        """B0: Rotate back face in clockwise direction"""

        # Back, Left, Right, Top, Bottom
        B, L, R, T, Z = self.cube[0], self.cube[1], self.cube[3], self.cube[4], self.cube[5]

        # Rotate back face
        Cube.rotate_clock(B)

        # Rotate adjacent blocks
        (
            L[0][0], L[1][0], L[2][0],
            Z[2][0], Z[2][1], Z[2][2],
            R[2][2], R[1][2], R[0][2],
            T[0][2], T[0][1], T[0][0]
        ) = (
            T[0][2], T[0][1], T[0][0],
            L[0][0], L[1][0], L[2][0],
            Z[2][0], Z[2][1], Z[2][2],
            R[2][2], R[1][2], R[0][2]
        )

    def rotate_back_anti(self):
        """B1: Rotate back face in anti-clockwise direction"""

        # Back, Left, Right, Top, Bottom
        B, L, R, T, Z = self.cube[0], self.cube[1], self.cube[3], self.cube[4], self.cube[5]

        # Rotate back face
        Cube.rotate_anti(B)

        # Rotate adjacent blocks
        (
            L[0][0], L[1][0], L[2][0],
            Z[2][0], Z[2][1], Z[2][2],
            R[2][2], R[1][2], R[0][2],
            T[0][2], T[0][1], T[0][0]
        ) = (
            Z[2][0], Z[2][1], Z[2][2],
            R[2][2], R[1][2], R[0][2],
            T[0][2], T[0][1], T[0][0],
            L[0][0], L[1][0], L[2][0]
        )

    #
    # Rotate Front
    #

    def rotate_front_clock(self):
        """F0: Rotate front face in clockwise direction"""

        L, F, R, T, Z = self.cube[1], self.cube[2], self.cube[3], self.cube[4], self.cube[5]

        # Rotate front face
        Cube.rotate_clock(F)

        # Rotate adjacent blocks
        (
            T[2][0], T[2][1], T[2][2],
            R[0][0], R[1][0], R[2][0],
            Z[0][2], Z[0][1], Z[0][0],
            L[2][2], L[1][2], L[0][2]
        ) = (
            L[2][2], L[1][2], L[0][2],
            T[2][0], T[2][1], T[2][2],
            R[0][0], R[1][0], R[2][0],
            Z[0][2], Z[0][1], Z[0][0]
        )

    def rotate_front_anti(self):
        """F1: Rotate front face in anti-clockwise direction"""

        L, F, R, T, Z = self.cube[1], self.cube[2], self.cube[3], self.cube[4], self.cube[5]

        # Rotate front face
        Cube.rotate_anti(F)

        # Rotate adjacent blocks
        (
            T[2][0], T[2][1], T[2][2],
            R[0][0], R[1][0], R[2][0],
            Z[0][2], Z[0][1], Z[0][0],
            L[2][2], L[1][2], L[0][2]
        ) = (
            R[0][0], R[1][0], R[2][0],
            Z[0][2], Z[0][1], Z[0][0],
            L[2][2], L[1][2], L[0][2],
            T[2][0], T[2][1], T[2][2]
        )

    #
    # Rotate Left
    #

    def rotate_left_clock(self):
        """L0: Rotate left face in clockwise direction"""

        B, L, F, T, Z = self.cube[0], self.cube[1], self.cube[2], self.cube[4], self.cube[5]

        # Rotate left face
        Cube.rotate_clock(L)

        # Rotate adjacent blocks
        (
            T[0][0], T[1][0], T[2][0],
            F[0][0], F[1][0], F[2][0],
            Z[0][0], Z[1][0], Z[2][0],
            B[2][2], B[1][2], B[0][2],
        ) = (
            B[2][2], B[1][2], B[0][2],
            T[0][0], T[1][0], T[2][0],
            F[0][0], F[1][0], F[2][0],
            Z[0][0], Z[1][0], Z[2][0]
        )

    def rotate_left_anti(self):
        """L1: Rotate left face in anti-clockwise direction"""

        B, L, F, T, Z = self.cube[0], self.cube[1], self.cube[2], self.cube[4], self.cube[5]

        # Rotate left face
        Cube.rotate_anti(L)

        # Rotate adjacent blocks
        (
            T[0][0], T[1][0], T[2][0],
            F[0][0], F[1][0], F[2][0],
            Z[0][0], Z[1][0], Z[2][0],
            B[2][2], B[1][2], B[0][2]
        ) = (
            F[0][0], F[1][0], F[2][0],
            Z[0][0], Z[1][0], Z[2][0],
            B[2][2], B[1][2], B[0][2],
            T[0][0], T[1][0], T[2][0]
        )

    #
    # Rotate Right
    #

    def rotate_right_clock(self):
        """R0: Rotate right face in clockwise direction"""

        B, F, R, T, Z = self.cube[0], self.cube[2], self.cube[3], self.cube[4], self.cube[5]

        # Rotate left face
        Cube.rotate_clock(R)

        # Rotate adjacent blocks
        (
            Z[2][2], Z[1][2], Z[0][2],
            F[2][2], F[1][2], F[0][2],
            T[2][2], T[1][2], T[0][2],
            B[0][0], B[1][0], B[2][0]
        ) = (
            B[0][0], B[1][0], B[2][0],
            Z[2][2], Z[1][2], Z[0][2],
            F[2][2], F[1][2], F[0][2],
            T[2][2], T[1][2], T[0][2]
        )

    def rotate_right_anti(self):
        """R1: Rotate right face in anti-clockwise direction"""

        B, F, R, T, Z = self.cube[0], self.cube[2], self.cube[3], self.cube[4], self.cube[5]

        # Rotate left face
        Cube.rotate_anti(R)

        # Rotate adjacent blocks
        (
            Z[2][2], Z[1][2], Z[0][2],
            F[2][2], F[1][2], F[0][2],
            T[2][2], T[1][2], T[0][2],
            B[0][0], B[1][0], B[2][0]
        ) = (
            F[2][2], F[1][2], F[0][2],
            T[2][2], T[1][2], T[0][2],
            B[0][0], B[1][0], B[2][0],
            Z[2][2], Z[1][2], Z[0][2]
        )

    #
    # Rotate Top
    #

    def rotate_top_clock(self):
        """T0: Rotate top face in clockwise direction"""

        B, L, F, R, T = self.cube[0], self.cube[1], self.cube[2], self.cube[3], self.cube[4]

        # Rotate top face
        Cube.rotate_clock(T)

        # Rotate adjacent blocks
        (
            F[0][2], F[0][1], F[0][0],
            L[0][2], L[0][1], L[0][0],
            B[0][2], B[0][1], B[0][0],
            R[0][2], R[0][1], R[0][0]
        ) = (
            R[0][2], R[0][1], R[0][0],
            F[0][2], F[0][1], F[0][0],
            L[0][2], L[0][1], L[0][0],
            B[0][2], B[0][1], B[0][0]
        )

    def rotate_top_anti(self):
        """T1: Rotate top face in anti-clockwise direction"""

        B, L, F, R, T = self.cube[0], self.cube[1], self.cube[2], self.cube[3], self.cube[4]

        # Rotate top face
        Cube.rotate_anti(T)

        # Rotate adjacent blocks
        (
            F[0][2], F[0][1], F[0][0],
            L[0][2], L[0][1], L[0][0],
            B[0][2], B[0][1], B[0][0],
            R[0][2], R[0][1], R[0][0]
        ) = (
            L[0][2], L[0][1], L[0][0],
            B[0][2], B[0][1], B[0][0],
            R[0][2], R[0][1], R[0][0],
            F[0][2], F[0][1], F[0][0]
        )

    #
    # Rotate Bottom
    #

    def rotate_bottom_clock(self):
        """Z0: Rotate bottom face in clockwise direction"""

        B, L, F, R, Z = self.cube[0], self.cube[1], self.cube[2], self.cube[3], self.cube[5]

        # Rotate bottom face
        Cube.rotate_clock(Z)

        # Rotate adjacent blocks
        (
            F[2][0], F[2][1], F[2][2],
            R[2][0], R[2][1], R[2][2],
            B[2][0], B[2][1], B[2][2],
            L[2][0], L[2][1], L[2][2]
        ) = (
            L[2][0], L[2][1], L[2][2],
            F[2][0], F[2][1], F[2][2],
            R[2][0], R[2][1], R[2][2],
            B[2][0], B[2][1], B[2][2]
        )

    def rotate_bottom_anti(self):
        """Z1: Rotate bottom face in anti-clockwise direction"""

        B, L, F, R, Z = self.cube[0], self.cube[1], self.cube[2], self.cube[3], self.cube[5]

        # Rotate bottom face
        Cube.rotate_anti(Z)

        # Rotate adjacent blocks
        (
            F[2][0], F[2][1], F[2][2],
            R[2][0], R[2][1], R[2][2],
            B[2][0], B[2][1], B[2][2],
            L[2][0], L[2][1], L[2][2]
        ) = (
            R[2][0], R[2][1], R[2][2],
            B[2][0], B[2][1], B[2][2],
            L[2][0], L[2][1], L[2][2],
            F[2][0], F[2][1], F[2][2]
        )

    # Following operations are redundant

    # #
    # # Rotate XY-Center
    # #

    # def rotate_XY_clock(self):
    #     self.rotate_top_anti()
    #     self.rotate_bottom_clock()

    # def rotate_XY_anti(self):
    #     self.rotate_top_clock()
    #     self.rotate_bottom_anti()

    # #
    # # Rotate XZ-Center
    # #

    # def rotate_XZ_clock(self):
    #     self.rotate_left_anti()
    #     self.rotate_right_clock()

    # def rotate_XZ_anti(self):
    #     self.rotate_left_clock()
    #     self.rotate_right_anti()

    # #
    # # Rotate YZ-Center
    # #

    # def rotate_YZ_clock(self):
    #     self.rotate_front_anti()
    #     self.rotate_back_clock()

    # def rotate_YZ_anti(self):
    #     self.rotate_front_clock()
    #     self.rotate_back_anti()


# Test
if __name__ == '__main__':
    c = Cube()
    print('operations:', Cube.operations)
    print('valid:', c.is_valid())

    for op in Cube.operations.values():
        print('\n{} 4 times'.format(op))
        for i in range(4):
            getattr(c, op)()
            print('valid:', c.is_valid())
        print('reset:', c.is_reset())

    for _ in range(1000):
        op = random.choice(list(Cube.operations.keys()))
        reverse_op = op[:-1] + str(1 - int(op[-1]))
        getattr(c, Cube.operations[op])
        assert c.is_valid()
        getattr(c, Cube.operations[reverse_op])
        assert c.is_valid()
        assert c.is_reset()

    print('\nShuffle 100 times:')
    c.shuffle(100)
    print('valid:', c.is_valid())

    print('\nRecover:')
    c.recover()
