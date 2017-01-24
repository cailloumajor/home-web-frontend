<template>
  <v-app top-fixed-navbar>
    <header>
      <v-navbar fixed>
        <v-btn class="hidden-md-and-up mx-2 white--text transparent" icon v-dropdown:menu>
          <v-icon>menu</v-icon>
        </v-btn>
        <v-dropdown id="menu" :items="items"></v-dropdown>
        <v-navbar-logo class="pl-3">
          <div class="mr-2" id="logo-back">
            <a href="/"><img  src="~assets/home_logo.png" alt="Home Web logo"></a>
          </div>
          Home Web
        </v-navbar-logo>
        <v-navbar-items :items="items" class="hidden-md-and-down"></v-navbar-items>
      </v-navbar>
    </header>
  </v-app>
</template>

<script>
import Hello from './components/Hello'

export default {
  name: 'app',
  components: {
    Hello
  },
  data () {
    return {
      items: [
        {text: 'Chauffage'},
        {text: 'Admin', href: '/admin'}
      ]
    }
  },
  mounted () {
    this.$vuetify.init()
  }
}
</script>

<style lang="stylus">
@import '~vuetify/src/stylus/main'

header .navbar
  align-items: center
  height: 3.5rem

  img
    max-height: 1.75rem

.navbar__logo
  font-size: 1.25rem

#logo-back
  background-color: #FFF
  height: 2.5rem
  width: @height
  border-radius: 50%
  display: flex
  align-items: center
  justify-content: center

  img
    display: flex
    align-self: center
</style>
