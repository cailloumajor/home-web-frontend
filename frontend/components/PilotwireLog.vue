<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération du journal."
  >
    <v-data-table
      :headers="headers"
      :items="fetchData"
      hide-actions
    >
      <template slot="items" scope="props">
        <td
          v-for="field in headers.map(el => el.value)"
          v-text="props.item[field]"
          :class="`${logColors[props.item.level]}--text`"
        ></td>
      </template>
    </v-data-table>
  </loading-layout>
</template>

<script>
import Fetching from '~/mixins/Fetching'
import LoadingLayout from '~components/LoadingLayout'

export default {

  name: 'pilotwire-log',

  components: {
    LoadingLayout
  },

  mixins: [Fetching],

  props: ['isActive'],

  data () {
    return {
      headers: [
        { text: 'Date/Heure', value: 'timestamp', left: true },
        { text: 'Niveau', value: 'level', left: true },
        { text: 'Message', value: 'message', left: true }
      ],
      logColors: {
        INFO: 'green',
        WARNING: 'orange',
        ERROR: 'red'
      }
    }
  },

  watch: {
    isActive (newVal) {
      if (newVal) {
        this.fetch('/heating/pilotwirelog/')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
/* satisfy stylelint */
</style>
