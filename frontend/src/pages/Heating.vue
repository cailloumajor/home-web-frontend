<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération des zones"
  >
    <v-tabs v-model="activeTab" id="heating-tabs" light>
      <v-tabs-bar slot="activators">
        <v-tabs-slider></v-tabs-slider>
        <v-tabs-item
          v-for="zone in fetchData"
          :href="'#zone-tab-' + zone.num"
          :key="zone.num"
        >
          {{ 'Zone ' + zone.num }}
        </v-tabs-item>
        <v-tabs-item href="#derogations-tab">
          Dérogations
        </v-tabs-item>
        <v-tabs-item class="right-tab" href="#pilotwire-log-tab">
          Journal
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-content
        v-for="zone in fetchData"
        :id="'zone-tab-' + zone.num"
        :key="zone.num"
      >
        <h6 class="zone-desc">{{ zone.desc }}</h6>
        <slots-table :zone="zone"></slots-table>
      </v-tabs-content>
      <v-tabs-content id="derogations-tab">
        <derogation-list :zones="fetchData"></derogation-list>
      </v-tabs-content>
      <v-tabs-content id="pilotwire-log-tab">
        <pilotwire-log :is-active="activeTab === 'pilotwire-log-tab'">
        </pilotwire-log>
      </v-tabs-content>
    </v-tabs>
  </loading-layout>
</template>

<script>
import Fetching from '@/mixins/Fetching'
import DerogationList from '@/components/DerogationList'
import LoadingLayout from '@/components/LoadingLayout'
import PilotwireLog from '@/components/PilotwireLog'
import SlotsTable from '@/components/SlotsTable'

export default {

  name: 'heating',

  components: {
    DerogationList,
    LoadingLayout,
    PilotwireLog,
    SlotsTable
  },

  mixins: [Fetching],

  data () {
    return {
      activeTab: null
    }
  },

  mounted () {
    this.fetch('/api/heating/zones/')
  }
}
</script>

<style lang="stylus" scoped>
.tabs__bar
  height: 2.8rem

.right-tab
  margin-left: auto

.zone-desc
  font-size: 1rem
  margin-bottom: 0.5rem
  margin-top: 0.3rem
  text-align: center
</style>
