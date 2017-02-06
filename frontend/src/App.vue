<template>
  <v-app top-navbar>
    <header>
      <v-navbar>
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
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      items: [
        { text: 'Chauffage', href: '/heating', router: true },
        { text: 'Admin', href: '/admin' }
      ]
    }
  },
  mounted () {
    this.$vuetify.init()
    this.$router.replace('/heating')
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

.content
  padding: 1rem 3rem 0
</style>
