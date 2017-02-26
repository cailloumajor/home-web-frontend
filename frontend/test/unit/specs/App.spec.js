import App from '../../../src/App'

describe('App.vue entrypoint', function () {
  it('should set the correct default data', function () {
    expect(App.data).to.be.a('function')
    const defaultData = App.data()
    expect(defaultData.links).to.not.be.empty
      .and.to.have.keys('text', 'href')
  })
})
