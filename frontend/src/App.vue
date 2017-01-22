<template>
  <div id="app">
    <img src="./assets/logo.png">
    <hello></hello>
  </div>
</template>

<script>
import Hello from './components/Hello'

export default {
  name: 'app',
  components: {
    Hello
  },
  mounted () {
    this.$vuetify.init()
  }
}
</script>

<style lang="stylus">
@import '~vuetify/src/stylus/main'
</style>
