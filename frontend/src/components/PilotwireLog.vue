<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération du journal."
  >
    <table>
      <thead><tr>
        <th
          v-for="header in headers"
          :style="{ width: header.width + 'px' }"
          class="centered-cell"
        >
          {{ header.text }}
        </th>
      </tr></thead>
      <tbody :style="{ height: tbodyHeight + 'px' }">
        <template v-for="entry in fetchData">
          <tr :class="logColors[entry.level] + '--text'">
            <td v-text="new Date(entry.timestamp).toLocaleString()"></td>
            <td class="centered-cell">{{ entry.level }}</td>
            <td :style="{ width: messageColWidth + 'px' }">
              {{ entry.message }}
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </loading-layout>
</template>

<script>
import _ from 'lodash'
import Fetching from '@/mixins/Fetching'
import LoadingLayout from '@/components/LoadingLayout'

export default {

  name: 'pilotwire-log',

  components: {
    LoadingLayout
  },

  mixins: [Fetching],

  data () {
    return {
      headers: [
        { text: 'Date/Heure', width: null },
        { text: 'Niveau', width: null },
        { text: 'Message', width: null }
      ],
      logColors: {
        INFO: 'green',
        WARNING: 'orange',
        ERROR: 'red'
      },
      messageColWidth: null,
      tbodyHeight: null
    }
  },

  methods: {
    resize () {
      const thead = this.$el.querySelector('thead')
      const tbody = this.$el.querySelector('tbody')
      const tbodyColumns = this.$el.querySelectorAll('tbody tr:first-child td')
      const columnWidths = [].map.call(tbodyColumns, el => el.offsetWidth)
      const lastColWidth = this.$el.offsetWidth - _.sum(_.initial(columnWidths))
      let scrollBarWidth

      // Resize tbody height
      this.tbodyHeight = (
        this.$el.parentElement.offsetHeight - thead.offsetHeight
      )

      // Resize columns width
      this.$nextTick(() => {
        scrollBarWidth = thead.scrollWidth - tbody.scrollWidth
        columnWidths.splice(-1, 1, lastColWidth)
        columnWidths.map((width, index) => {
          this.headers[index].width = width
        })
        this.$nextTick(() => {
          this.messageColWidth = _.last(columnWidths) - scrollBarWidth
        })
      })
    }
  },

  props: ['isActive'],

  watch: {
    isActive () {
      if (this.isActive) {
        this.fetch('/api/heating/pilotwirelog/')
      }
    },

    fetchStatus () {
      if (this.fetchStatus === 'loaded') {
        this.$nextTick(() => {
          setTimeout(this.resize, 0)
        })
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
table
  thead
  tbody
    display: block

  tbody
    overflow-y: auto

    td
      padding-top: 4px
      padding-bottom: 4px

.centered-cell
  text-align: center
</style>
