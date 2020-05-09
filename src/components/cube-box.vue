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
import { Cube } from '@/cube/cube';

export default {
    name: 'CubeBox',
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
            cubeObj: new Cube()
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
            this.cubeObj.takeOperation(op_name);
        },
        async goBack() {
            this.cubeObj.goBack();
        },
        async shuffle() {
            this.cubeObj.shuffle();
        },
        async resetCube() {
            this.cubeObj.reset();
        },
        async recoverCube() {
            while (!this.cubeObj.isReset()) {
                this.cubeObj.goBack();
                await new Promise(resolve => {
                    setTimeout(() => {
                        resolve();
                    }, 200);
                });
            }
        }
    },
    computed: {
        adjustRotation() {
            return `transform: translate(-50%, -50%) rotateX(${this.rotateX}deg) rotateY(${this.rotateY}deg) rotateZ(${this.rotateZ}deg);`;
        },
        cube() {
            return this.cubeObj.cube;
        }
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