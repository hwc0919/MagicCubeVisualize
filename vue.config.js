module.exports = {
    assetsDir: './static',
    indexPath: './templates/index.html',

    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true
            }
        }
    }
};
