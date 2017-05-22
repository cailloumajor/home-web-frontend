import Vue from 'vue'
import Heating from '@/pages/Heating'

describe('Heating.vue page', function () {
  it('should set the correct default data', function () {
    expect(Heating.data).to.be.a('function')
    const defaultData = Heating.data()
    expect(defaultData.activeTab).to.be.null()
  })

  it('should have a `mounted` hook', function () {
    expect(Heating.mounted).to.be.a('function')
    const vm = new Vue(Heating)
    sinon.stub(vm, 'fetch')
    vm.$mount()
    expect(vm.fetch).to.have.been.called()
  })
})
