module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'Home Web',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Home Web' }
    ],
    link: [
      { rel: 'icon', type: 'image/png', href: '/favicon.png' },
      { rel: 'shortcut icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', type: 'text/css', href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLINT on save
    */
    extend (config, ctx) {
      if (ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    },

    vendor: ['lodash', 'vuetify'],

    extractCSS: true,

    analyze: process.env.NODE_ENV === 'development' && {
      analyzerHost: '0.0.0.0'
    }
  },

  css: [
    { src: '~assets/style/app.styl', lang: 'styl' }
  ],

  plugins: [
    '~plugins/vuetify'
  ],

  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/proxy'
  ],

  proxy: process.env.NODE_ENV === 'development' ? [
    'http://django:8000/admin',
    'http://django:8000/api',
    'http://django:8000/django-static'
  ] : undefined
}
