import Vue from 'vue'
import SlotsTable from '@/components/SlotsTable'

describe('SlotsTable component', function () {
  it('should set correct default data', function () {
    expect(SlotsTable.data).to.be.a('function')
    const defaultData = SlotsTable.data()
    expect(defaultData.days).to.have.length(7)
      .and.to.all.satisfy((el) => typeof el === 'string')
    expect(defaultData.hours).to.have.length(25)
      .and.to.all.satisfy((el) => typeof el === 'number')
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
    const propsData = { zoneNum: randNum }
    const vm = new Ctor({ propsData })
    sinon.stub(vm, 'fetch')
    vm.$mount()
    expect(vm.fetch).to.have.been.calledWithMatch(zoneRegExp)
  })

  it('should have a `slotSpecs` computed property', function () {
    const vm = new Vue(SlotsTable)
    expect(vm.slotSpecs).to.have.lengthOf(1)
    vm.fetchData = [{ a: 1, b: 2, c: 3, d: 4 }]
    expect(vm.slotSpecs).to.have.lengthOf(2)
  })
})
