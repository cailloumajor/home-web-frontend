<template>
  <div v-if="status === 'loading'" class="centering">
    <v-progress-circular :size="progressSize" :width="6" indeterminate>
    </v-progress-circular>
  </div>
  <div v-else-if="status === 'loaded'">
    <slot></slot>
  </div>
  <v-alert v-else-if="status === 'error'" class="mx-4 mt-4" error :value="true">
    {{ errorText }}
    <br>
    Voir la console pour plus de détails.
  </v-alert>
  <div v-else class="centering">
    <v-icon x-large>help_outline</v-icon>
  </div>
</template>

<script>
export default {

  name: 'loading-layout',

  props: ['errorText', 'status'],

  data () {
    return {
      progressSize: 50
    }
  }
}
</script>

<style lang="stylus" scoped>
.centering
  display: flex
  height: 100%
  align-items: center
  justify-content: center
</style>
