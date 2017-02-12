<template>
  <v-tabs id="heating-tabs">
    <v-tab-item
      v-for="zone in zones"
      :href="'#zone-tab-' + zone.num"
      slot="activators">
      {{ 'Zone ' + zone.num }}
    </v-tab-item>
    <v-tab-content
      v-for="zone in zones"
      :id="'zone-tab-' + zone.num"
      :style="{ height: tabsItemsHeight + 'px' }"
      slot="content">
    </v-tab-content>
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

<style lang="stylus">
#heating-tabs .tabs__tabs
  height: 2.8rem
</style>
