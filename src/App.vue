<template>
    <div id="app">
        <cube-box></cube-box>
    </div>
</template>

<script>
import CubeBox from '@/components/cube-box';

export default {
    name: 'App',
    components: {
        CubeBox
    }
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

* {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
}
</style>
