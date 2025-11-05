let publicPath = process.env.NODE_ENV === 'production' ? './' : './';

module.exports = {
  publicPath,
  productionSourceMap: false,
  devServer: {
    proxy: 'http://frontend.snap-aspi'
  }
};
