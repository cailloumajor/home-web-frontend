<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération des créneaux"
  >
    <svg height="260" width="1020">
      <text
        v-for="h in hours"
        :x="refX + gapX * 4 * h"
        y="14"
        text-anchor="middle"
      >{{ hourText(h) }}</text>
      <text
        v-for="(d, index) in ['lun', 'mar', 'mer', 'jeu', 'ven', 'sam', 'dim']"
        :x="refX - 4"
        :y="refY + slotHeight + gapY * index - 3"
        text-anchor="end"
      >{{ d.toUpperCase() + '.' }}</text>
      <line
        v-for="index in 97"
        :x1="vertBarPosX(index)"
        :y1="vertBarStartY(index)"
        :x2="vertBarPosX(index)"
        :y2="refY + gapY * 6 + slotHeight + 5"
        :stroke="vertBarColor(index)"
      ></line>
      <template v-for="s in legend">
        <rect
          :x="slotStartX(s)"
          :y="refY + gapY * 7"
          :height="slotHeight"
          :width="gapX * 4"
          :fill="slotColor({ mode: 'C' })"
          class="legend"
        ></rect>
        <rect
          v-if="s.mode"
          :x="slotStartX(s)"
          :y="refY + gapY * 7"
          :height="slotHeight"
          :width="gapX * 4"
          :fill="slotColor(s)"
          class="legend"
        ></rect>
        <text
          :x="slotStartX(s) + gapX * 4 + 4"
          :y="refY + gapY * 7 + slotHeight - 3"
          text-anchor="start"
        >{{ s.text }}</text>
      </template>
      <g
        class="slot-group"
        :stroke="slotColor({ mode: 'C' })"
        :fill="slotColor({ mode: 'C' })"
        @click.stop="slotClick(baseSlot)"
      >
        <rect
          v-for="(d, index) in days"
          :x="slotStartX(baseSlot)"
          :y="refY + gapY * index"
          :height="slotHeight"
          :width="slotWidth(baseSlot)"
        ></rect>
      </g>
      <g
        v-for="s in fetchData"
        class="slot-group hover-stroke"
        :stroke="slotColor(s)"
        :fill="slotColor(s)"
        @click.stop="slotClick(s)"
      >
        <rect
          v-for="(d, index) in days"
          v-if="s[d]"
          :x="slotStartX(s)"
          :y="refY + gapY * index"
          :height="slotHeight"
          :width="slotWidth(s)"
        ></rect>
      </g>
    </svg>
    <slot-form
      v-model="formActive"
      :create="formCreate"
      :formData="formSlot"
      :schemaURL="slotsURL"
      :zone="zone"
      @success="fetch(fetchURL)"
    ></slot-form>
  </loading-layout>
</template>

<script>
import _ from 'lodash'
import Days from '../mixins/Days'
import Fetching from '../mixins/Fetching'
import LoadingLayout from '~components/LoadingLayout'
import SlotForm from '~components/SlotForm'

function timeScale (timeString) {
  const timeArray = timeString.split(':')
  const hours = parseInt(timeArray[0], 10)
  const minutes = parseInt(timeArray[1], 10)
  return (hours + minutes / 60) * 4
}

export default {

  name: 'slots-table',

  components: {
    LoadingLayout,
    SlotForm
  },

  mixins: [Days, Fetching],

  props: ['zone'],

  data () {
    return {
      formActive: false,
      formCreate: false,
      formSlot: null,
      hours: _.range(25),
      legend: [
        { start_time: '06:30', text: 'Confort' },
        { start_time: '09:30', text: 'Eco.', mode: 'E' },
        { start_time: '12:30', text: 'Hors-gel', mode: 'H' },
        { start_time: '15:30', text: 'Arrêt', mode: 'A' }
      ],
      refX: 38.5,
      refY: 24.5,
      gapX: 10,
      gapY: 30,
      slotHeight: 15,
      slotsURL: '/heating/slots/'
    }
  },

  computed: {
    baseSlot () {
      let slot = {
        start_time: '00:00',
        end_time: '24:00',
        url: this.slotsURL,
        zone: this.zone.url
      }
      this.days.map(day => {
        slot[day] = false
      })
      return slot
    },

    fetchURL () {
      return `${this.slotsURL}?zone=${this.zone.num}`
    }
  },

  methods: {
    hourText (hour) {
      return _.padStart(hour, 2, '0') + ':00'
    },

    slotClick (slot) {
      this.formCreate = slot === this.baseSlot
      this.formSlot = slot
      this.formActive = true
    },

    slotColor (slot) {
      return { C: 'yellow', E: 'lime', H: 'blue', A: 'red' }[slot.mode]
    },

    slotStartX (slot) {
      return timeScale(slot.start_time) * this.gapX + this.refX
    },

    slotWidth (slot) {
      const endTime = slot.end_time === '00:00' ? '24:00' : slot.end_time
      const scaleWidth = timeScale(endTime) - timeScale(slot.start_time)
      return scaleWidth * this.gapX
    },

    vertBarColor (index) {
      if ((index - 1) % 4 === 0) return 'black'
      else if ((index - 1) % 2 === 0) return '#808080'
      else return '#CCCCCC'
    },

    vertBarPosX (index) {
      return this.refX + this.gapX * (index - 1)
    },

    vertBarStartY (index) {
      if ((index - 1) % 4 === 0) return this.refY - 6
      else if ((index - 1) % 2 === 0) return this.refY - 4
      else return this.refY - 2
    }
  },

  mounted () {
    this.fetch(this.fetchURL)
  }
}
</script>

<style lang="stylus" scoped>
$opacity = 0.3

svg
  border: 1px solid black
  display: block
  font-size: 12px
  font-weight: 500
  margin: 0 auto 1rem

rect.legend
  fill-opacity: $opacity

g.slot-group
  fill-opacity: $opacity
  stroke-width: 0

  &:hover
    cursor: pointer

    &.hover-stroke
      stroke-width: 2
</style>
