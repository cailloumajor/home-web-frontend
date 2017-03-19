import Vue from 'vue'
import LoadingLayout from '@/components/LoadingLayout'

describe('LoadingLayout component', function () {
  it('should set correct default data', function () {
    expect(LoadingLayout.data).to.be.a('function')
    const defaultData = LoadingLayout.data()
    expect(defaultData.progressSize).to.be.above(0)
  })

  it('should render error text', function () {
    const Ctor = Vue.extend(LoadingLayout)
    const errorText = 'Testing error text'
    const propsData = {
      errorText: errorText,
      status: 'error'
    }
    const vm = new Ctor({ propsData }).$mount()
    expect(vm.$el.textContent).to.contain(errorText)
  })
})
