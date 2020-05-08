<template>
    <div id="app">
        <cube></cube>
    </div>
</template>

<script>
import Cube from '@/components/cube';

export default {
    name: 'App',
    components: {
        Cube
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
