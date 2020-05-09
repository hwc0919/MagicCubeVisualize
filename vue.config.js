module.exports = {
    publicPath: '/MagicCubeVisualize',
    outputDir: './docs',
    configureWebpack: {
        resolve: { extensions: ['.ts', '.tsx', '.js', '.json'] },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    loader: 'ts-loader',
                    exclude: /node_modules/,
                    options: {
                        appendTsSuffixTo: [/\.vue$/]
                    }
                }
            ]
        }
    }
};
