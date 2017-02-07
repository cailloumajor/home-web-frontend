import Vue from 'vue' // eslint-disable-line no-unused-vars
import Heating from 'src/pages/Heating'

describe('Heating.vue page', function () {
  // Inspect component data
  it('should set the correct default data', function () {
    expect(Heating.data).to.be.a('function')
    const defaultData = Heating.data()
    expect(defaultData.tabsItemsHeight).to.be.above(0)
    expect(defaultData.zones).to.be.instanceof(Array).that.is.empty
  })
})
