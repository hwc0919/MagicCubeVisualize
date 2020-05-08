<template>
    <div>
        <div :class="['cube', { 'rotate-animation': rotating }]" :style="adjustRotation">
            <cube-face v-for="(f, ind) in faces" :class="f" :face="f" :key="f" :matx="cube[ind]"> </cube-face>
        </div>
        <div class="scale-toolbar">
            <button @click="resetRotation">RESET</button>
            <div class="input-group">
                <label>X: {{ rotateX }}°</label>
                <input type="range" v-model.number="rotateX" :min="-180" :max="180" />
            </div>
            <div class="input-group">
                <label>Y: {{ rotateY }}°</label>
                <input type="range" v-model.number="rotateY" :min="-180" :max="180" />
            </div>
            <div class="input-group">
                <label>Z: {{ rotateZ }}°</label>
                <input type="range" v-model.number="rotateZ" :min="-180" :max="180" />
            </div>
        </div>
        <div class="operation-buttons">
            <button class="special-button" @click="resetCube">Reset</button>
            <button class="special-button" @click="recoverCube">Recover</button>
            <button class="special-button" @click="shuffle">Shuffle</button>
            <button class="special-button" @click="goBack">Back</button>
            <button v-for="op in opNames" :key="`${op}-button`" @click="takeOperation(op)">{{ op }}</button>
        </div>
    </div>
</template>

<script>
import CubeFace from '@/components/cube-face';

export default {
    name: 'Cube',
    components: {
        CubeFace
    },
    data() {
        return {
            rotateX: -30,
            rotateY: 30,
            rotateZ: 0,
            rotating: false,
            lock: false,
            faces: ['B', 'L', 'F', 'R', 'T', 'Z'],
            opNames: ['B0', 'B1', 'L0', 'L1', 'F0', 'F1', 'R0', 'R1', 'T0', 'T1', 'Z0', 'Z1'],
            cube: [
                [
                    ['A00', 'B00', 'A10'],
                    ['B40', 'F00', 'B50'],
                    ['A40', 'B80', 'A50']
                ],
                [
                    ['A11', 'B11', 'A21'],
                    ['B51', 'F11', 'B61'],
                    ['A51', 'B91', 'A61']
                ],
                [
                    ['A22', 'B22', 'A32'],
                    ['B62', 'F02', 'B72'],
                    ['A62', 'BA2', 'A72']
                ],
                [
                    ['A33', 'B33', 'A03'],
                    ['B73', 'F13', 'B43'],
                    ['A73', 'BB3', 'A43']
                ],
                [
                    ['A14', 'B04', 'A04'],
                    ['B14', 'F24', 'B34'],
                    ['A24', 'B24', 'A34']
                ],
                [
                    ['A65', 'BA5', 'A75'],
                    ['B95', 'F25', 'BB5'],
                    ['A55', 'B85', 'A45']
                ]
            ]
        };
    },
    methods: {
        resetRotation() {
            this.rotateX = -30;
            this.rotateY = 30;
            this.rotateZ = 0;
            this.rotating = true;
            setTimeout(() => {
                this.rotating = false;
            }, 500);
        },
        async takeOperation(op_name) {
            await this.$getCube(`/api/op/${op_name}`).catch(err => {
                alert(err);
            });
        },
        async goBack() {
            if (this.lock) return;
            this.lock = true;
            await this.$getCube('/api/go-back').catch(err => {
                alert(err);
            });
            this.lock = false;
        },
        async shuffle() {
            if (this.lock) return;
            this.lock = true;
            await this.$getCube('/api/shuffle').catch(err => {
                alert(err);
            });
            this.lock = false;
        },
        async resetCube() {
            if (this.lock) return;
            this.lock = true;
            await this.$getCube('/api/reset').catch(err => {
                alert(err);
            });
            this.lock = false;
        },
        async recoverCube() {
            if (this.lock) return;
            this.lock = true;
            let flag = true;
            while (flag) {
                await this.$getCube('api/go-back').catch(() => {
                    alert('Finish');
                    flag = false;
                });
                await new Promise(resolve => {
                    setTimeout(() => {
                        resolve();
                    }, 200);
                });
            }
            this.lock = false;
        }
    },
    computed: {
        adjustRotation() {
            return `transform: translate(-50%, -50%) rotateX(${this.rotateX}deg) rotateY(${this.rotateY}deg) rotateZ(${this.rotateZ}deg);`;
        }
    },
    mounted() {
        this.$getCube('/api/get-cube').catch(err => {
            alert(err);
        });
    }
};
</script>

<style scoped>
button {
    width: 80px;
    height: 40px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    outline: none;
}

button:active {
    transform: scale(0.96);
}

button:hover {
    background-color: #dfe6e9;
}

.scale-toolbar {
    display: flex;
    width: 240px;
    flex-direction: column;
    align-items: flex-start;
    margin: 30px;
}

.scale-toolbar button {
    align-self: center;
}

.input-group {
    margin: 10px;
}

.input-group label {
    display: inline-block;
    width: 100%;
    text-align: left;
    padding-left: 80px;
}

.input-group input {
    width: 200px;
}

.cube {
    position: absolute;
    width: 180px;
    height: 180px;
    left: 50%;
    top: 50%;
    /* transform: translate(-50%, -50%) rotateX(30deg) rotateY(10deg) rotateZ(10deg); */
    transform-style: preserve-3d;
    /* perspective: 1000px; */
}

.rotate-animation {
    transition: all 0.5s;
}

.B {
    transform: translateZ(-90px) rotateY(180deg);
}

.L {
    transform: translateX(-90px) rotateY(-90deg);
}

.F {
    transform: translateZ(90px);
}

.R {
    transform: translateX(90px) rotateY(90deg);
}

.T {
    transform: translateY(-90px) rotateX(90deg);
}

.Z {
    transform: translateY(90px) rotateX(-90deg);
}

.operation-buttons {
    position: absolute;
    margin-left: 50px;
    display: flex;
    flex-wrap: wrap;
    width: 180px;
    justify-content: space-between;
}

.operation-buttons button {
    margin: 5px;
}

.special-button {
    background-color: #3498db;
    color: white;
}
.special-button:hover {
    background-color: #2980b9;
}
</style>