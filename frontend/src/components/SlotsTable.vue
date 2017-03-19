<template>
  <loading-layout
    :status="fetchStatus"
    error-text="Erreur de récupération des créneaux"
  >
    <svg height="230" width="1020">
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
      <g
        v-for="s in slotSpecs"
        class="slot-group"
        :class="{ 'hover-stroke': s.mode !== 'C' }"
        :stroke="slotColor(s)"
        :fill="slotColor(s)"
      >
        <rect
          v-for="(d, index) in days"
          v-if="s[d]"
          :x="slotStartX(s)"
          :y="refY + gapY * index"
          :height="slotHeight"
          :width="slotWidth(s)"
        >{{ index }}</rect>
      </g>
    </svg>
  </loading-layout>
</template>

<script>
import _ from 'lodash'
import Fetching from '@/mixins/Fetching'
import LoadingLayout from '@/components/LoadingLayout'

const initialSlots = [{
  mode: 'C',
  start_time: '00:00',
  end_time: '24:00',
  mon: true,
  tue: true,
  wed: true,
  thu: true,
  fri: true,
  sat: true,
  sun: true
}]

function timeScale (timeString) {
  const timeArray = timeString.split(':')
  const hours = parseInt(timeArray[0], 10)
  const minutes = parseInt(timeArray[1], 10)
  return (hours + minutes / 60) * 4
}

export default {

  name: 'slots-table',

  components: {
    LoadingLayout
  },

  mixins: [Fetching],

  props: ['zoneNum'],

  computed: {
    slotSpecs () {
      return initialSlots.concat(this.fetchData || [])
    }
  },

  data () {
    return {
      days: ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],
      hours: _.range(25),
      refX: 38.5,
      refY: 24.5,
      gapX: 10,
      gapY: 30,
      slotHeight: 15
    }
  },

  methods: {
    hourText (hour) {
      return _.padStart(hour, 2, '0') + ':00'
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
    this.fetch(`/api/heating/slots/?zone=${this.zoneNum}`)
  }
}
</script>

<style lang="stylus" scoped>
svg
  border: 1px solid black
  display: block
  font-size: 12px
  font-weight: 500
  margin: auto

g.slot-group
  fill-opacity: 0.3
  stroke-width: 0

  &:hover
    cursor: pointer

    &.hover-stroke
      stroke-width: 2
</style>
