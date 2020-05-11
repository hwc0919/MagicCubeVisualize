<template>
    <label class="wrapper">
        <input ref="checkbox" :checked="on" type="checkbox" @input="$emit('input', $refs.checkbox.checked)">
        <span class="square" :style="{
            width: `${width}px`,
            height: `${height}px`,
            'border-radius': `${radius}px`,
            '--pseudo-border-radius': `${radius}px`,
            '--pseudo-width': `${height - 2 * margin}px`,
            '--pseudo-margin': `${margin}px`,
            '--pseudo-end-left': `${width - height}px`,
        }">
        </span>
    </label>
</template>

<script>
export default {
    model: {
        prop: 'on',
        event: 'input'
    },
    props: {
        on: {
            type: Boolean,
            default: false
        },
        width: {
            type: Number,
            default: 80
        },
        height: {
            type: Number,
            default: 40
        },
        margin: {
            type: Number,
            default: 4
        },
        radius: {
            type: Number,
            default: 6
        }
    },
    mounted() {
        console.log('this.checked', this.$refs.checkbox.checked);
    }
};
</script>

<style scoped>
.wrapper {
    position: relative;
}

.wrapper input {
    display: none;
}

.square {
    position: relative;
    background: #ccc;
    display: block;
    overflow: hidden;
    cursor: pointer;
    transition: 0.4s;
}

.square::before {
    content: '';
    position: absolute;
    width: var(--pseudo-width);
    height: var(--pseudo-width);
    margin: var(--pseudo-margin);
    left: 0;
    background: white;
    border-radius: var(--pseudo-border-radius);
    transition: 0.3s;
}

.wrapper input:checked + .square {
    background: #03a9f4;
}

.wrapper input:checked + .square::before {
    left: var(--pseudo-end-left);
}
</style>