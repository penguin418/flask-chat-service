const path = require('path')

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5555',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
