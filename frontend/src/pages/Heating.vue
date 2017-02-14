<template>
  <v-tabs v-if="zonesReady" id="heating-tabs">
    <v-tab-item
      v-for="zone in zones"
      :href="'#zone-tab-' + zone.num"
      slot="activators"
    >
      {{ 'Zone ' + zone.num }}
    </v-tab-item>
    <v-tab-content
      v-for="zone in zones"
      :id="'zone-tab-' + zone.num"
      :style="{ height: tabsItemsHeight + 'px' }"
      slot="content"
    >
    </v-tab-content>
  </v-tabs>
  <error v-else-if="zonesError">
    Erreur de récupération des zones.
  </error>
</template>

<script>
import axios from 'axios'
import Error from 'components/Error'

export default {

  name: 'heating',

  components: {
    Error
  },

  data () {
    return {
      tabsItemsHeight: 300,
      zones: [],
      zonesError: false,
      zonesReady: false
    }
  },

  created () {
    axios.get('/api/heating/zones/')
      .then(response => {
        this.zones = response.data
        this.zonesReady = true
      })
      .catch(error => {
        console.error(error)
        this.zonesError = true
      })
  }
}
</script>

<style lang="stylus">
#heating-tabs .tabs__tabs
  height: 2.8rem
</style>
