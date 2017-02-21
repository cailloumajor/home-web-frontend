<template>
  <v-alert class="mx-4 mt-4" error :value="true">
    <slot></slot>
    <br>
    Voir la console pour plus de détails.
  </v-alert>
</template>
