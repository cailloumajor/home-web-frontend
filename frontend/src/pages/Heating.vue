<template>
  <v-tabs ref="tabs">
    <v-tabs-tabs>
      <v-tab-item
          v-for="zone in zones"
          :item="{ text: 'Zone ' + zone.num, href: '#zone-tab-' + zone.num }">
      </v-tab-item>
    </v-tabs-tabs>
    <v-tabs-items :style="{ height: tabsItemsHeight + 'px' }">
      <v-tabs-item
          v-for="zone in zones"
          :id="'zone-tab-' + zone.num">
      </v-tabs-item>
    </v-tabs-items>
  </v-tabs>
</template>

<script>
export default {

  name: 'heating',

  data () {
    return {
      tabsItemsHeight: 300,
      zones: []
    }
  }
}
</script>

<style lang="stylus" scoped>
.tabs__tabs
  height: 2.8rem
</style>
