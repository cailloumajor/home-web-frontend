<template>
  <v-tabs v-model="activeTab" :scrollable="false" dark>
    <v-tabs-bar slot="activators">
      <v-tabs-slider></v-tabs-slider>
      <v-tabs-item
        v-for="zone in zones"
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
      v-for="zone in zones"
      :id="'zone-tab-' + zone.num"
      :key="zone.num"
    >
      <h6 class="zone-desc">{{ zone.desc }}</h6>
      <slots-table :zone="zone"></slots-table>
    </v-tabs-content>
    <v-tabs-content id="derogations-tab">
      <derogation-list></derogation-list>
    </v-tabs-content>
    <v-tabs-content id="pilotwire-log-tab">
      <pilotwire-log :is-active="activeTab === 'pilotwire-log-tab'">
      </pilotwire-log>
    </v-tabs-content>
  </v-tabs>
</template>

<script>
import DerogationList from '~components/DerogationList'
import LoadingLayout from '~components/LoadingLayout'
import PilotwireLog from '~components/PilotwireLog'
import SlotsTable from '~components/SlotsTable'

export default {

  components: {
    DerogationList,
    LoadingLayout,
    PilotwireLog,
    SlotsTable
  },

  data () {
    return {
      activeTab: null
    }
  },

  computed: {
    zones () { return this.$store.state.heating.zones }
  },

  async fetch ({ store }) {
    const { data } = await store.$axios.get('/heating/zones/?format=json')
    store.commit('heating/setZones', data)
  },

  head () {
    return {
      title: 'Chauffage - Home Web'
    }
  }
}
</script>

<style lang="scss" scoped>
.tabs__bar { /* stylelint-disable selector-class-pattern */
  height: 2.8rem;
}

.right-tab {
  margin-left: auto;
}

.zone-desc {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  padding-top: 0.3rem;
  text-align: center;
}
</style>
