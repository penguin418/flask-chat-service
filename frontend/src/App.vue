<template>
  <div id="app">
    <div>
      <small>Raised</small>
      <md-button class="md-primary" @click="check()">Default</md-button>
    </div>
    <div id="nav">
      <router-link to="/home">Home</router-link>
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
<script>
export default {
  created() {
    this.$cookies.config('1d');
    this.$cookies.set('test', 'test-token');
    // eslint-disable-next-line no-undef
    this.socket = io.connect('localhost:5555');
  },
  mounted() {
    this.socket.on('connect', () => {
      console.log('connected');
    });
  },
  methods: {
    check() {
      console.log('check socketio');
      this.socket.emit('start', { data: 'hello' });
    },
  },
};
</script>
