<template>
    <div class="cube-face">
        <div class="line" v-for="i in 3" :key="`${face}-line-${i}`">
            <span v-for="j in 3" class="cell" :key="`${face}-${i}${j}`"
                  :style="{'background-color': bgcolor(matx[i - 1][j - 1])}">
                <span class="center" v-if="i == 2 && j == 2">{{ face }}</span>
            </span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CubeFace',
    props: ['face', 'matx'],
    methods: {
        bgcolor(str) {
            switch (parseInt(str[str.length - 1])) {
                case 0:
                    return 'green';
                case 1:
                    return 'blue';
                case 2:
                    return 'red';
                case 3:
                    return 'orange';
                case 4:
                    return 'white';
                case 5:
                    return 'yellow';
            }
        }
    }
};
</script>

<style scoped>
.cube-face {
    position: absolute;
    width: 182px;
    height: 182px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 2px;
    border-radius: 4px;
    flex-wrap: wrap;
    background-color: #dfe6e9;
    transform-origin: 50% 50% 50%;
}

.line {
    display: flex;
    justify-content: space-around;
    width: 100%;
}

.cell {
    display: inline-block;
    margin: 2px;
    width: 52px;
    height: 52px;
    border-radius: 6px;
    line-height: 52px;
}

.center {
    font-size: 20px;
    font-weight: bolder;
    color: black;
    text-shadow: 2px 1px 0px white;
}
</style>