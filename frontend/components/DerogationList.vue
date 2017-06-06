<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération des dérogations"
  >
    <table>
      <thead>
        <tr>
          <th v-for="col in staticColumns">{{ col.text }}</th>
          <th v-for="zone in zones">{{ `Z${zone.num}` }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="derog in fetchData"
          :class="{ outdated: derog.outdated }"
          @click.stop="derogationClick(derog)"
        >
          <template v-for="col in staticColumns">
            <td v-if="typeof derog[col.value] === 'boolean'">
              <v-icon v-if="derog[col.value]" class="primary--text">
                check
              </v-icon>
            </td>
            <td v-else :style="cellStyle(derog, col)">
              {{ parseField(derog[col.value]) }}
            </td>
          </template>
          <td v-for="zone in zones">
            <v-icon v-if="derog.zones.includes(zone.url)" class="primary--text">
              check
            </v-icon>
          </td>
        </tr>
      </tbody>
    </table>
    <derogation-form
      v-model="formActive"
      :create="formCreate"
      :formData="formDerogation"
      :schemaURL="fetchURL"
      @success="fetch(fetchURL)"
    ></derogation-form>
  </loading-layout>
</template>

<script>
import Fetching from '~/mixins/Fetching'
import LoadingLayout from '~components/LoadingLayout'

export default {

  name: 'derogation-list',

  components: {
    'derogation-form': () => import('~components/DerogationForm'),
    LoadingLayout
  },

  mixins: [Fetching],

  data () {
    return {
      fetchURL: '/heating/derogations/',
      formActive: false,
      formCreate: false,
      formDerogation: null,
      modes: {
        E: { text: 'Eco.', color: '#B3FF7E' },
        H: { text: 'Hors-gel', color: '#B3B3CA' },
        A: { text: 'Arrêt', color: '#FFB37E' }
      },

      staticColumns: [
        { text: 'Active', value: 'active' },
        { text: 'Création', value: 'creation_dt' },
        { text: 'Prise d\'effet', value: 'start_dt' },
        { text: 'Fin d\'effet', value: 'end_dt' },
        { text: 'Mode', value: 'mode' }
      ]
    }
  },

  computed: {
    zones () { return this.$store.state.heating.zones }
  },

  methods: {
    cellStyle (derogation, column) {
      return {
        backgroundColor: column.value === 'mode' &&
          this.modes[derogation.mode].color
      }
    },

    derogationClick (derogation) {
      this.formCreate = false
      this.formDerogation = derogation
      this.formActive = true
    },

    parseField (str) {
      const dt = new Date(str)
      if (!isNaN(dt)) {
        const options = {
          weekday: 'short',
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }
        return dt.toLocaleString(undefined, options)
      }
      if (this.modes[str]) return this.modes[str].text
      return str
    }
  },

  mounted () {
    this.fetch(this.fetchURL)
  }
}
</script>

<style lang="stylus" scoped>
table
  border-collapse: collapse
  margin: 0 auto 5px
  text-align: center

  thead
    color: rgba(0, 0, 0, 0.54)
    font-size: 12px
    font-weight: 500

  tbody
    color: rgba(0, 0, 0, 0.87)
    font-size: 13px
    font-weight: 400

    tr
      cursor: pointer

      &.outdated
        color: rgba(0, 0, 0, 0.2)

      &:hover
        background-color: #EF9A9A

  th
  td
    border-bottom: 1px solid grey
    padding: 10px 20px

.icon
  font-size: 16px
</style>
