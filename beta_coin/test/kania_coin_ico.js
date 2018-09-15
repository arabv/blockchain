import assertRevert from 'openzeppelin-solidity/test/helpers/assertRevert'
import latestTime from 'openzeppelin-solidity/test/helpers/latestTime'
import { duration } from 'openzeppelin-solidity/test/helpers/increaseTime'
 
const CharityToken = artifacts.require('KaniaToken')
const CharityTokenICO = artifacts.require('KaniaTokenICO')
 
contract('KaniaTokenICO', (accounts) => {
  const wallet = accounts[9]
  const rate = 100
 
  beforeEach(async function () {
    this.startTime = latestTime() + duration.days(1)
    this.endTime = this.startTime + duration.days(3)
    this.token = await CharityToken.new()
  })
 
  describe('ICO initialization', async () => {
    it('should initialize ICO', async function () {
      const ico = await CharityTokenICO.new(this.startTime, this.endTime, rate, wallet, this.token.address)
 
      assert.equal(this.startTime, await ico.openingTime())
      assert.equal(this.endTime, await ico.closingTime())
      assert.equal(rate, await ico.rate())
      assert.equal(wallet, await ico.wallet())
      assert.equal(this.token.address, await ico.token())
    })
 
    it('should reject if a start time is in the past', async function () {
      const startTime = latestTime() - duration.days(1)
      await assertRevert(CharityTokenICO.new(startTime, this.endTime, rate, wallet, this.token.address))
    })
 
    it('should reject if an end time is before a start time', async function () {
      const endTime = this.startTime - duration.days(1)
      await assertRevert(CharityTokenICO.new(this.startTime, endTime, rate, wallet, this.token.address))
    })
 
    it('should reject if given rate is 0', async function () {
      await assertRevert(CharityTokenICO.new(this.startTime, this.endTime, 0, wallet, this.token.address))
    })
  })
})
