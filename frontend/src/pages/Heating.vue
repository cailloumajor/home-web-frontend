<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération des zones"
  >
    <v-tabs v-model="activeTab" id="heating-tabs">
      <v-tab-item
        v-for="zone in fetchData"
        :href="'#zone-tab-' + zone.num"
        :key="zone.num"
        slot="activators"
      >
        {{ 'Zone ' + zone.num }}
      </v-tab-item>
      <v-tab-item class="right-tab" href="#pilotwire-log-tab" slot="activators">
        Journal
      </v-tab-item>
      <v-tab-content
        v-for="zone in fetchData"
        :id="'zone-tab-' + zone.num"
        :key="zone.num"
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
  </loading-layout>
</template>

<script>
import Fetching from '@/mixins/Fetching'
import LoadingLayout from '@/components/LoadingLayout'
import PilotwireLog from '@/components/PilotwireLog'

export default {

  name: 'heating',

  components: {
    LoadingLayout,
    PilotwireLog
  },

  mixins: [Fetching],

  data () {
    return {
      activeTab: null,
      tabsItemsHeight: 300
    }
  },

  computed: {
    fetchURL () {
      return '/api/heating/zones/'
    }
  },

  mounted () {
    this.fetch()
  },

  updated () /* istanbul ignore next */ {
    const tabBar = this.$el.querySelector('.tabs__tabs')
    if (tabBar) tabBar.style.height = '2.8rem'
  }
}
</script>

<style lang="stylus" scoped>
.right-tab
  margin-left: auto
</style>
