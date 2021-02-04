import Vue from 'vue';
import VueMaterial from 'vue-material';
import VueAxios from 'vue-axios';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

Vue.config.productionTip = false;

Vue.use(VueMaterial);
Vue.use(VueAxios, axios);
Vue.use(require('vue-cookies'));

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
