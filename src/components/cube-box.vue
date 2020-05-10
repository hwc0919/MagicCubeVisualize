<template>
    <div
        class="cube-wrapper"
        @mousedown.self="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @mouseleave="handleMouseLeave"
    >
        <!-- Cube Box -->
        <div
            :class="['cube', { 'rotate-animation': resetRotating }]"
            :style="adjustRotation"
            @mousedown="handleMouseDown"
        >
            <cube-face v-for="(f, ind) in faces" :class="f" :face="f" :key="f" :matx="cube[ind]"></cube-face>
        </div>

        <!-- Scale Toolbar -->
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
                <label>interval: {{ interval }}ms</label>
                <input type="range" v-model.number="interval" :min="0" :max="1000" />
            </div>
        </div>

        <!-- Operation Button Groups -->
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
        let cubeObj = new Cube();
        return {
            rotateX: -30,
            rotateY: 30,
            oldRotate: {
                x: 0,
                y: 0
            },
            resetRotating: false,
            rotating: false,
            interval: 200,
            faces: ['B', 'L', 'F', 'R', 'T', 'Z'],
            opNames: ['B0', 'B1', 'L0', 'L1', 'F0', 'F1', 'R0', 'R1', 'T0', 'T1', 'Z0', 'Z1'],
            cubeObj: cubeObj,
            cube: cubeObj.cube
        };
    },
    methods: {
        resetRotation() {
            this.resetRotating = true;
            this.rotateX = -30;
            this.rotateY = 30;
            setTimeout(() => {
                this.resetRotating = false;
            }, 500);
        },
        takeOperation(opName) {
            this.cubeObj.takeOperation(opName);
        },
        goBack() {
            this.cubeObj.goBack();
        },
        shuffle() {
            this.cubeObj.shuffle();
        },
        resetCube() {
            this.cubeObj.reset();
        },
        async recoverCube() {
            while (true) {
                this.cubeObj.goBack();
                await new Promise(resolve => {
                    setTimeout(() => {
                        resolve();
                    }, this.interval);
                });
                if (this.cubeObj.isReset()) {
                    alert('Finish');
                    break;
                }
            }
        },

        // Rotating by mouse dragging
        handleMouseDown(event) {
            this.rotating = true;
            this.oldRotate.x = this.rotateX;
            this.oldRotate.y = this.rotateY;
            this.startX = event.clientX;
            this.startY = event.clientY;
        },
        handleMouseMove(event) {
            if (this.rotating) {
                this.rotateX = this.oldRotate.x - (event.clientY - this.startY);
                this.rotateY = this.oldRotate.y + event.clientX - this.startX;

                if (this.rotateX > 180) {
                    this.startY -= 360;
                } else if (this.rotateX < -180) {
                    this.startY += 360;
                }
                if (this.rotateY > 180) {
                    this.startX += 360;
                } else if (this.rotateY < -180) {
                    this.startX -= 360;
                }
            }
        },
        handleMouseUp(event) {
            this.rotating = false;
        },
        handleMouseLeave(event) {
            this.rotating = false;
        }
    },
    computed: {
        adjustRotation() {
            return `transform: translate(-50%, -50%) rotateX(${this.rotateX}deg) rotateY(${this.rotateY}deg);`;
        }
    },
    watch: {
        cubeObj: {
            handler() {
                this.cube = JSON.parse(JSON.stringify(this.cubeObj.cube));
            },
            deep: true
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
    width: 220px;
    flex-direction: column;
    align-items: flex-start;
    margin-left: 30px;
    margin-top: 30px;
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

.cube-wrapper {
    width: 100%;
    height: 100%;
}

.cube {
    position: absolute;
    width: 180px;
    height: 180px;
    left: 50%;
    top: 50%;
    transform-style: preserve-3d;
    /* perspective: 1000px; */
    /* transform: Computed Attribute */
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
    display: flex;
    flex-wrap: wrap;
    width: 180px;
    margin-top: 10px;
    margin-left: 50px;
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