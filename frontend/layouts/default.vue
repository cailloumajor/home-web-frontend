<template>
  <v-app top-toolbar>
    <header>
      <v-toolbar light>
        <v-menu class="hidden-sm-and-up">
          <v-btn dark icon slot="activator">
            <v-icon>menu</v-icon>
          </v-btn>
          <v-list>
            <v-list-item v-for="link in links" :key="link.text">
              <v-list-tile :href="link.href" :router="link.router">
                <v-list-tile-title>{{ link.text }}</v-list-tile-title>
              </v-list-tile>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-toolbar-logo class="pl-3">
          <div class="mr-2" id="logo-back">
            <a href="/">
              <img src="~assets/home_logo.png" alt="Home Web logo">
            </a>
          </div>
          Home Web
        </v-toolbar-logo>
        <v-toolbar-items class="hidden-sm-and-down">
          <v-toolbar-item
            v-for="link in links"
            :href="link.href"
            :key="link.text"
            :router="link.router"
          >
            {{ link.text }}
          </v-toolbar-item>
        </v-toolbar-items>
      </v-toolbar>
    </header>
    <main>
      <v-container fluid>
        <nuxt/>
      </v-container>
    </main>
  </v-app>
</template>

<script>
export default {

  data () {
    return {
      links: [
        { text: 'Chauffage', href: '/heating', router: true },
        { text: 'Admin', href: '/admin' }
      ]
    }
  },

  middleware: 'redirect_root'
}
</script>

<style lang="stylus">
header .toolbar
  align-items: center
  height: 3.5rem

  img
    max-height: 1.75rem

.toolbar__logo
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
