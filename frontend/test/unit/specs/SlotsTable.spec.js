import Vue from 'vue'
import SlotsTable from '@/components/SlotsTable'

describe('SlotsTable component', function () {
  it('should set correct default data', function () {
    expect(SlotsTable.data).to.be.a('function')
    const defaultData = SlotsTable.data()
    expect(defaultData.hours).to.have.lengthOf(25)
      .and.to.satisfy(arr => arr.every(el => typeof el === 'number'))
    expect(defaultData.refX).to.satisfy((n) => n % 1 === 0.5)
    expect(defaultData.refY).to.satisfy((n) => n % 1 === 0.5)
    expect(defaultData.gapX).to.be.above(0)
    expect(defaultData.gapY).to.be.above(0)
    expect(defaultData.slotHeight).to.be.above(0)
  })

  it('should have a `mounted` hook', function () {
    const Ctor = Vue.extend(SlotsTable)
    const randNum = Math.round(Math.random() * 10)
    const zoneRegExp = new RegExp(`\\?zone=${randNum}$`)
    const propsData = { zone: { num: randNum } }
    const vm = new Ctor({ propsData })
    sinon.stub(vm, 'fetch')
    vm.$mount()
    expect(vm.fetch).to.have.been.calledWithMatch(zoneRegExp)
  })

  it('should have a `baseSlot` computed property', function () {
    const vm = new Vue(SlotsTable)
    vm.zone = { url: 'test' }
    expect(vm.baseSlot).to.have.keys([
      'start_time', 'end_time', 'url', 'zone', ...vm.days
    ])
  })
})
