const path = require('path');

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:5555',
        ws: true,
        changeOrigin: true,
      },
    },
  },
};
