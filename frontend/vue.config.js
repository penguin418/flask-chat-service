const path = require('path');

module.exports = {
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'http://127.0.0.1:5555',
        ws: true,
        changeOrigin: true,
      },
    },
  },
};
