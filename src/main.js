import Vue from 'vue';
import App from './App.vue';
import { getCube } from './fetch';

Vue.config.productionTip = false;
Vue.prototype.$getCube = getCube;

new Vue({
    render: function(h) {
        return h(App);
    }
}).$mount('#app');
