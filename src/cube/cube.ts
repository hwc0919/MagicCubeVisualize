import { detailed_cube, adjacent_corners, adjacent_edges } from './cube_matrix';

export class Cube {
    cube: Array<Array<Array<string>>>;
    originalCube: Array<Array<Array<string>>>;
    corners: Array<Array<Array<number>>>;
    edges: Array<Array<Array<number>>>;
    history: Array<string>;
    static opNames: Array<string> = ['B0', 'B1', 'F0', 'F1', 'L0', 'L1', 'R0', 'R1', 'T0', 'T1', 'Z0', 'Z1'];
    static operations: Object = {
        B0: 'rotateBackClock',
        B1: 'rotateBackAnti',
        F0: 'rotateFrontClock',
        F1: 'rotateFrontAnti',
        L0: 'rotateLeftClock',
        L1: 'rotateLeftAnti',
        R0: 'rotateRightClock',
        R1: 'rotateRightAnti',
        T0: 'rotateTopClock',
        T1: 'rotateTopAnti',
        Z0: 'rotateBottomClock',
        Z1: 'rotateBottomAnti'
    };

    public constructor() {
        this.cube = detailed_cube();
        this.originalCube = detailed_cube();

        // Adjacent corners
        this.corners = adjacent_corners();
        this.edges = adjacent_edges();
        this.history = [];
    }

    /**
     *  Reset cube to original state
     */
    public reset(): void {
        this.cube = detailed_cube();
    }

    /**
     *  Check if the cube is valid
     */
    public isValid(): boolean {
        let cube = this.cube;
        for (let f = 0; f < 6; f++) {
            for (let r = 0; r < 3; r++) {
                for (let c = 0; c < 3; c++) {
                    let state: string = cube[f][r][c];
                    // check face center
                    if (r == 1 && c == 1) {
                        if (state[0] !== 'F' || state[2] !== String(f)) {
                            console.log(`error at (${f},${r},${c}), should be ${'F*' + f}, but ${state}`);
                            return false;
                        }
                    }
                    // check edges
                    else if ((r + c) & 1) {
                        if (state[0] !== 'B') {
                            console.log(`error at (${f},${r},${c}), should be ${'B*' + f}, but ${state}`);
                            return false;
                        }
                    }
                    // check corners
                    else {
                        if (state[0] !== 'A') {
                            console.log(`error at (${f},${r},${c}), should be ${'A*' + f}, but ${state}`);
                            return false;
                        }
                    }
                }
            }
        }
        // Check adjacent corner blocks
        for (let corner of this.corners) {
            let [f0, r0, c0] = corner[0];
            for (let [f, r, c] of corner.slice(1)) {
                if (cube[f0][r0][c0].slice(0, 2) !== cube[f][r][c].slice(0, 2)) {
                    console.log(`error at (${f},${r},${c})  corner doesn't match`);
                    return false;
                }
            }
        }
        // Check adjacent edge blocks:
        for (let [[f0, r0, c0], [f1, r1, c1]] of this.edges) {
            if (cube[f0][r0][c0].slice(0, 2) !== cube[f1][r1][c1].slice(0, 2)) {
                console.log(`error at (${f0},${r0},${c0}) edge doesn't match`);
                return false;
            }
        }
        return true;
    }

    /**
     *  Reset cube to original state
     */
    public isReset(): boolean {
        for (let f = 0; f < 6; f++) {
            for (let r = 0; r < 3; r++) {
                for (let c = 0; c < 3; c++) {
                    if (this.cube[f][r][c] !== this.originalCube[f][r][c]) return false;
                }
            }
        }
        return true;
    }

    /**
     *  Get the name of reversed operation
     */
    public static reverseOp(opName: string): string {
        return opName.slice(0, -1) + String(1 - Number(opName.slice(-1)));
    }

    public takeOperation(opName: string, record: boolean = true): boolean {
        if (Cube.operations[opName] === undefined) {
            return false;
        }
        if (record) {
            if (this.history.length > 0 &&
                this.history[this.history.length - 1] === Cube.reverseOp(opName)) {
                this.history.pop();
            } else {
                this.history.push(opName);
            }
        }
        this[Cube.operations[opName]]();
        return true;
    }

    public shuffle(times: number = 20): void {
        for (let i: number = 0; i < times; i++) {
            let index = Math.floor((Math.random() * Cube.opNames.length));
            this.takeOperation(Cube.opNames[index], true);
        }
    }

    public recover(): boolean {
        while (this.history.length > 0) {
            this.goBack();
        }
        return true;
    }

    public goBack(): boolean {
        if (this.history.length < 1) {
            return false;
        }
        let reverseOp = Cube.reverseOp(this.history.pop());
        this.takeOperation(reverseOp, false);
        if (this.isReset()) this.history.splice(0, 0);
        return true;
    }

    /**
     *  Rotate Operations
     */

    // Rotate certain face in clockwise direction
    public static rotateClock(f: Array<Array<string>>): void {
        [f[0][0], f[0][1], f[0][2], f[1][2], f[2][2], f[2][1], f[2][0], f[1][0]] =
            [f[2][0], f[1][0], f[0][0], f[0][1], f[0][2], f[1][2], f[2][2], f[2][1]];
    }

    // Rotate certain face in anti-clockwise direction
    public static rotateAnti(f: Array<Array<string>>): void {
        [f[0][0], f[0][1], f[0][2], f[1][2], f[2][2], f[2][1], f[2][0], f[1][0]] =
            [f[0][2], f[1][2], f[2][2], f[2][1], f[2][0], f[1][0], f[0][0], f[0][1]];
    }

    public rotateBackClock(): void {
        let cube = this.cube;
        let [B, L, R, T, Z] = [cube[0], cube[1], cube[3], cube[4], cube[5]];
        Cube.rotateClock(B);
        [
            L[0][0], L[1][0], L[2][0],
            Z[2][0], Z[2][1], Z[2][2],
            R[2][2], R[1][2], R[0][2],
            T[0][2], T[0][1], T[0][0]
        ] = [
                T[0][2], T[0][1], T[0][0],
                L[0][0], L[1][0], L[2][0],
                Z[2][0], Z[2][1], Z[2][2],
                R[2][2], R[1][2], R[0][2]
            ];
    }
    public rotateBackAnti(): void {
        let cube = this.cube;
        let [B, L, R, T, Z] = [cube[0], cube[1], cube[3], cube[4], cube[5]];
        Cube.rotateAnti(B);
        [
            L[0][0], L[1][0], L[2][0],
            Z[2][0], Z[2][1], Z[2][2],
            R[2][2], R[1][2], R[0][2],
            T[0][2], T[0][1], T[0][0]
        ] = [
                Z[2][0], Z[2][1], Z[2][2],
                R[2][2], R[1][2], R[0][2],
                T[0][2], T[0][1], T[0][0],
                L[0][0], L[1][0], L[2][0]
            ];
    }

    public rotateFrontClock(): void {
        let cube = this.cube;
        let [L, F, R, T, Z] = [cube[1], cube[2], cube[3], cube[4], cube[5]];

        // Rotate front face
        Cube.rotateClock(F);

        // Rotate adjacent blocks
        [
            T[2][0], T[2][1], T[2][2],
            R[0][0], R[1][0], R[2][0],
            Z[0][2], Z[0][1], Z[0][0],
            L[2][2], L[1][2], L[0][2]
        ] = [
                L[2][2], L[1][2], L[0][2],
                T[2][0], T[2][1], T[2][2],
                R[0][0], R[1][0], R[2][0],
                Z[0][2], Z[0][1], Z[0][0]
            ];
    }
    public rotateFrontAnti(): void {
        let cube = this.cube;
        let [L, F, R, T, Z] = [cube[1], cube[2], cube[3], cube[4], cube[5]];

        // Rotate front face
        Cube.rotateAnti(F);

        // Rotate adjacent blocks
        [
            T[2][0], T[2][1], T[2][2],
            R[0][0], R[1][0], R[2][0],
            Z[0][2], Z[0][1], Z[0][0],
            L[2][2], L[1][2], L[0][2]
        ] = [
                R[0][0], R[1][0], R[2][0],
                Z[0][2], Z[0][1], Z[0][0],
                L[2][2], L[1][2], L[0][2],
                T[2][0], T[2][1], T[2][2]
            ];
    }
    public rotateLeftClock(): void {
        let cube = this.cube;
        let [B, L, F, T, Z] = [cube[0], cube[1], cube[2], cube[4], cube[5]];

        // Rotate left face
        Cube.rotateClock(L);

        // Rotate adjacent blocks
        [
            T[0][0], T[1][0], T[2][0],
            F[0][0], F[1][0], F[2][0],
            Z[0][0], Z[1][0], Z[2][0],
            B[2][2], B[1][2], B[0][2],
        ] = [
                B[2][2], B[1][2], B[0][2],
                T[0][0], T[1][0], T[2][0],
                F[0][0], F[1][0], F[2][0],
                Z[0][0], Z[1][0], Z[2][0]
            ];
    }
    public rotateLeftAnti(): void {
        let cube = this.cube;
        let [B, L, F, T, Z] = [cube[0], cube[1], cube[2], cube[4], cube[5]];

        // Rotate left face
        Cube.rotateAnti(L);

        // Rotate adjacent blocks
        [
            T[0][0], T[1][0], T[2][0],
            F[0][0], F[1][0], F[2][0],
            Z[0][0], Z[1][0], Z[2][0],
            B[2][2], B[1][2], B[0][2]
        ] = [
                F[0][0], F[1][0], F[2][0],
                Z[0][0], Z[1][0], Z[2][0],
                B[2][2], B[1][2], B[0][2],
                T[0][0], T[1][0], T[2][0]
            ];
    }
    public rotateRightClock(): void {
        let cube = this.cube;
        let [B, F, R, T, Z] = [cube[0], cube[2], cube[3], cube[4], cube[5]];

        // Rotate left face
        Cube.rotateClock(R);

        // Rotate adjacent blocks
        [
            Z[2][2], Z[1][2], Z[0][2],
            F[2][2], F[1][2], F[0][2],
            T[2][2], T[1][2], T[0][2],
            B[0][0], B[1][0], B[2][0]
        ] = [
                B[0][0], B[1][0], B[2][0],
                Z[2][2], Z[1][2], Z[0][2],
                F[2][2], F[1][2], F[0][2],
                T[2][2], T[1][2], T[0][2]
            ];
    }
    public rotateRightAnti(): void {
        let cube = this.cube;
        let [B, F, R, T, Z] = [cube[0], cube[2], cube[3], cube[4], cube[5]];

        // Rotate left face
        Cube.rotateAnti(R);

        // Rotate adjacent blocks
        [
            Z[2][2], Z[1][2], Z[0][2],
            F[2][2], F[1][2], F[0][2],
            T[2][2], T[1][2], T[0][2],
            B[0][0], B[1][0], B[2][0]
        ] = [
                F[2][2], F[1][2], F[0][2],
                T[2][2], T[1][2], T[0][2],
                B[0][0], B[1][0], B[2][0],
                Z[2][2], Z[1][2], Z[0][2]
            ];
    }
    public rotateTopClock(): void {
        let cube = this.cube;
        let [B, L, F, R, T] = [cube[0], cube[1], cube[2], cube[3], cube[4]];

        // Rotate top face
        Cube.rotateClock(T);

        // Rotate adjacent blocks
        [
            F[0][2], F[0][1], F[0][0],
            L[0][2], L[0][1], L[0][0],
            B[0][2], B[0][1], B[0][0],
            R[0][2], R[0][1], R[0][0]
        ] = [
                R[0][2], R[0][1], R[0][0],
                F[0][2], F[0][1], F[0][0],
                L[0][2], L[0][1], L[0][0],
                B[0][2], B[0][1], B[0][0]
            ];
    }
    public rotateTopAnti(): void {
        let cube = this.cube;
        let [B, L, F, R, T] = [cube[0], cube[1], cube[2], cube[3], cube[4]];

        // Rotate top face
        Cube.rotateAnti(T);

        // Rotate adjacent blocks
        [
            F[0][2], F[0][1], F[0][0],
            L[0][2], L[0][1], L[0][0],
            B[0][2], B[0][1], B[0][0],
            R[0][2], R[0][1], R[0][0]
        ] = [
                L[0][2], L[0][1], L[0][0],
                B[0][2], B[0][1], B[0][0],
                R[0][2], R[0][1], R[0][0],
                F[0][2], F[0][1], F[0][0]
            ];
    }
    public rotateBottomClock(): void {
        let cube = this.cube;
        let [B, L, F, R, Z] = [cube[0], cube[1], cube[2], cube[3], cube[5]];

        // Rotate bottom face
        Cube.rotateClock(Z);

        // Rotate adjacent blocks
        [
            F[2][0], F[2][1], F[2][2],
            R[2][0], R[2][1], R[2][2],
            B[2][0], B[2][1], B[2][2],
            L[2][0], L[2][1], L[2][2]
        ] = [
                L[2][0], L[2][1], L[2][2],
                F[2][0], F[2][1], F[2][2],
                R[2][0], R[2][1], R[2][2],
                B[2][0], B[2][1], B[2][2]
            ];
    }
    public rotateBottomAnti(): void {
        let cube = this.cube;
        let [B, L, F, R, Z] = [cube[0], cube[1], cube[2], cube[3], cube[5]];

        // Rotate bottom face
        Cube.rotateAnti(Z);

        // Rotate adjacent blocks
        [
            F[2][0], F[2][1], F[2][2],
            R[2][0], R[2][1], R[2][2],
            B[2][0], B[2][1], B[2][2],
            L[2][0], L[2][1], L[2][2]
        ] = [
                R[2][0], R[2][1], R[2][2],
                B[2][0], B[2][1], B[2][2],
                L[2][0], L[2][1], L[2][2],
                F[2][0], F[2][1], F[2][2]
            ];
    }
}
