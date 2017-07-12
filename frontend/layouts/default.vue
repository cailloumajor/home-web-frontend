<template>
  <v-app footer light toolbar>
    <v-navigation-drawer v-model="drawer" temporary light>
      <v-list>
        <v-list-tile
          v-for="link in links"
          :href="link.href"
          :key="link.text"
          :nuxt="link.nuxt"
          :to="link.to"
        >
          <v-list-tile-content >
            <v-list-tile-title>{{ link.text }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar id="main-toolbar" class="primary" dark>
      <v-toolbar-side-icon
        @click.native.stop="drawer = !drawer"
        class="hidden-sm-and-up"
      ></v-toolbar-side-icon>
      <v-toolbar-title class="pl-3">
        <div id="logo-back">
          <a href="/">
            <img src="~assets/home_logo.png" alt="Home Web logo">
          </a>
        </div>
      </v-toolbar-title>
      <v-toolbar-title>Home Web</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down links">
        <v-btn
          v-for="link in links"
          :href="link.href"
          :key="link.text"
          :nuxt="link.nuxt"
          :to="link.to"
          tag="a"
          flat
        >
          {{ link.text }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <main>
      <v-container fluid>
        <nuxt></nuxt>
      </v-container>
    </main>
    <v-footer></v-footer>
  </v-app>
</template>

<script>
export default {

  data () {
    return {
      drawer: false,
      links: [
        { text: 'Chauffage', to: '/heating', nuxt: true },
        { text: 'Admin', href: '/admin' }
      ]
    }
  },

  middleware: 'redirect_root'
}
</script>

<style lang="scss">
#main-toolbar {
  img {
    max-height: 1.75rem;
  }

  .toolbar__title {
    font-size: 1.25rem;
  }

  .links {
    .btn {
      color: rgba(255, 255, 255, 0.7);
    }

    .btn--active {
      color: #fff;
    }
  }
}

#logo-back {
  $width: 2.5rem;

  background-color: #fff;
  height: $width;
  width: $width;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    display: flex;
    align-self: center;
  }
}
</style>
