<template>
  <v-tabs v-if="zonesReady" v-model="activeTab" id="heating-tabs">
    <v-tab-item
      v-for="zone in zones"
      :href="'#zone-tab-' + zone.num"
      slot="activators"
    >
      {{ 'Zone ' + zone.num }}
    </v-tab-item>
    <v-tab-item class="right-tab" href="#pilotwire-log-tab" slot="activators">
      Journal
    </v-tab-item>
    <v-tab-content
      v-for="zone in zones"
      :id="'zone-tab-' + zone.num"
      :style="{ height: tabsItemsHeight + 'px' }"
      slot="content"
    >
    </v-tab-content>
    <v-tab-content
      id="pilotwire-log-tab"
      slot="content"
      :style="{ height: tabsItemsHeight + 'px' }"
    >
      <pilotwire-log :is-active="activeTab === 'pilotwire-log-tab'">
      </pilotwire-log>
    </v-tab-content>
  </v-tabs>
  <error v-else-if="zonesError">
    Erreur de récupération des zones.
  </error>
</template>

<script>
import axios from 'axios'
import Error from '@/components/Error'
import PilotwireLog from '@/components/PilotwireLog'

export default {

  name: 'heating',

  components: {
    Error,
    PilotwireLog
  },

  data () {
    return {
      activeTab: null,
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
  },

  updated () {
    const tabBar = this.$el.querySelector('.tabs__tabs')
    if (tabBar) tabBar.style.height = '2.8rem'
  }
}
</script>

<style lang="stylus" scoped>
.right-tab
  margin-left: auto
</style>
