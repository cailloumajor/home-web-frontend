export const state = () => ({
  zones: []
})

export const mutations = {
  setZones (state, zones) {
    state.zones = zones
  }
}
