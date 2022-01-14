<template>
    <div class="main-content">
        <main>
            <div class="page-header">
                <div class="header-input">
                    <h1>
                      Test Dashboard
                    </h1>
                    <small>
                      Monitor key metrics:
                    <input v-on:keyup.enter="execute" id="metrics" maxlength="12" :placeholder="id_" v-model="v">
                    </small>
                    <input type="checkbox" id="jack" value=false v-model="autocheck" @change="autoRun($event)">
                    <label for="jack">Auto-Run</label>
                    <span>{{ autocheck }}</span>
                </div>
                <div class="header-actions">
                    <button>
                        <span class="las la-file-export"></span>
                        Export
                    </button>
                    <button @click="toggleSetting">
                        <span class="las la-tools"></span>
                        Settings
                    </button>
                </div>
            </div>
            <div class="cards">
              <div v-for="(n, i) in c_nums" :key="i" class="card-single">
                <div class="card-flex">
                  <div class="multi-button">
                    <button class="las la-home" v-on:dblclick="togglehomeall(i)" @click="togglehome(i)"></button>
                    <button class="las la-file" v-on:dblclick="togglelogall(i)" @click="togglelog(i)"></button>
                  </div>
                  <div class="card-info" :class="{hactive: ishomeSelected(i)}">
                      <h4 class="scriptname">{{data.scriptname}}</h4>
                      <small>Next : </small>
                      <small :ref="'nf'+i" :id="'nf'+i">{{nstatus[i]}}</small>
                      <h2 :ref="'p'+i" :id="'p'+i">{{cstatus[i]}}</h2>
                      <!-- <small>PASS: 123, FAIL: 10</small> -->
                      <div class="card-head text3d">
                        <span :ref="'c'+i" :id="'c'+i">{{mac}}</span>
                        <span>,</span>
                        <span :ref="'n'+i" :id="'n'+i">{{sn}}</span>
                      </div>
                      <div class="one-third">
                        <transition name="slide" mode="out-in">
                          <h5 v-if="data.pass[i] % 2 === 0" class="stat" key="x">
                            {{data.pass[i]}}
                          </h5>
                          <h5 v-else class="stat" key="y">
                            {{data.pass[i]}}
                          </h5>
                        </transition>
                        <h5 class="stat-value" style="color:green">Pass</h5>
                      </div>
                      <div class="one-third">
                        <transition name="slide" mode="out-in">
                          <h5 v-if="data.fail[i] % 2 === 0" class="stat" key="x">
                            {{data.fail[i]}}
                          </h5>
                          <h5 v-else class="stat" key="y">
                            {{data.fail[i]}}
                          </h5>
                        </transition>
                        <h5 class="stat-value" style="color:red">Fail</h5>
                      </div>
                      <div class="one-third">
                        <transition name="slide" mode="out-in">
                          <h5 v-if="data.total[i] % 2 === 0" class="stat" key="x">
                            {{data.total[i]}}
                          </h5>
                          <h5 v-else class="stat" key="y">
                            {{data.total[i]}}
                          </h5>
                        </transition>
                        <h5 class="stat-value">Total</h5>
                      </div>
                  </div>
                  <div :ref="'q'+i" :id="'q'+i" class="card-chart success">
                    <span status="false" :ref="'run'+i" :id="'run'+i"></span>
                  </div>
              </div>
              <div class="textlog" :class="{active: islogSelected(i)}">
                  <textarea :ref="'t'+i" :id="'t'+i" placeholder="Log Message..." readonly></textarea>
              </div>
            </div>
          </div>
        </main>
    </div>
    <label for="sidebar-toggle" class="body-label"></label>
</template>

<script>
/* eslint no-eval: 0 */
import axios from 'axios'
import qs from 'qs'

export default {
  name: 'TestBoard',
  emits: ['btoggle', 'updateNum', 'mountscript'],
  props: ['data'],
  data () {
    return {
      // metrics parameter
      id_: 'ID',
      c_nums: 8,
      v: '',
      runid: '0',
      // mac, sn
      mac: '************',
      sn: '************',
      interval: null,
      autocheck: false,
      // Setting
      tlog: [false, false, false, false, false, false, false, false],
      thome: [true, true, true, true, true, true, true, true],
      cstatus: ['Waiting', 'Waiting', 'Waiting', 'Waiting', 'Waiting', 'Waiting', 'Waiting', 'Waiting'],
      nstatus: ['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None']
    }
  },
  mounted () {
    // this.interval = setInterval(() => {
    //   this.pass[0]++
    // }, 500)
    for (let i = 1; i <= this.c_nums; i++) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/data/',
        data: qs.stringify({
          card: 'c' + i.toString(),
          status: 'restore'
        }),
        headers: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
      })
        .then(response => {
          this.run('c' + i.toString(), 'restore')
          console.log(response)
        })
        .catch((error) => console.log(error))
    }
    this.gscriptname()
  },
  methods: {
    gscriptname () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/dload/',
        headers: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
      })
        .then(response => {
          console.log(response)
          this.$emit('mountscript', response.data.script)
        })
        .catch((error) => console.log(error))
    },
    autoRun (event) {
      // console.log(this.autocheck)
      if (this.autocheck) {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/api/arp/',
          data: qs.stringify({
            auto: this.autocheck
          }),
          headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
          }
        })
          .then(response => {
            const arp = response.data.arp
            // console.log(response.data.arp)
            for (let i = 0; i <= 7; i++) {
              console.log(this.$refs['run' + i].getAttribute('status') === 'false')
              if (this.$refs['run' + i].getAttribute('status') === 'false') {
                if (arp.length) {
                  const mac = arp.pop()
                  this.$refs['c' + i].textContent = mac
                  this.$refs['n' + i].textContent = mac
                  this.$refs['c' + i].style.color = '#0120cc'
                  this.$refs['n' + i].style.color = '#0120cc'
                  this.$refs['run' + i].setAttribute('status', 'true')
                  this.run('c' + (i + 1), 'start')
                }
              }
            }
            this.sleep(4000).then(() => {
              this.autoRun()
            })
          })
          .catch((error) => console.log(error))
      } else {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/api/arp/',
          data: qs.stringify({
            auto: this.autocheck
          }),
          headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
          }
        })
          .then(response => {
            console.log(response)
          })
          .catch((error) => console.log(error))
      }
    },
    toggleSetting () {
      // this.showSetting = !this.showSetting
      this.$emit('btoggle')
    },
    togglelog (id) {
      this.tlog[id] = true
      this.thome[id] = false
    },
    togglehomeall (id) {
      this.tlog = [false, false, false, false, false, false, false, false]
      this.thome = [true, true, true, true, true, true, true, true]
    },
    togglelogall (id) {
      this.tlog = [true, true, true, true, true, true, true, true]
      this.thome = [false, false, false, false, false, false, false, false]
    },
    togglehome (id) {
      this.tlog[id] = false
      this.thome[id] = true
    },
    islogSelected (id) {
      return this.tlog[id]
    },
    ishomeSelected (id) {
      return this.thome[id]
    },
    execute (event) {
      if (this.id_ === 'ID' && this.$refs['run' + (this.v - 1)].getAttribute('status') === 'false') {
        this.runid = this.v - 1
        this.id_ = 'MAC'
        this.v = ''
        this.$refs['c' + this.runid].textContent = this.mac
        this.$refs['n' + this.runid].textContent = this.sn
        this.$refs['c' + this.runid].style.color = '#0120cc'
        this.$refs['n' + this.runid].style.color = '#0120cc'
      } else if (this.id_ === 'MAC') {
        this.id_ = 'SN'
        this.$refs['c' + this.runid].textContent = this.v
        this.v = ''
      } else if (this.id_ === 'SN') {
        this.id_ = 'ID'
        this.$refs['n' + this.runid].textContent = this.v
        this.v = ''
        this.$refs['run' + this.runid].setAttribute('status', 'true')
        this.run('c' + (this.runid + 1), 'start')
        // this.runCard('run', this.runid)
      } else {
        alert('input error')
        this.v = ''
      }
    },
    run (c, s) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/data/',
        data: qs.stringify({
          card: c,
          status: s,
          mac: this.$refs['c' + (c[1] - 1)].textContent
        }),
        headers: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
      })
        .then(response => {
          const e = response.data
          var num = e.card[1] - 1
          const log = document.getElementById('t' + num)
          if (this.cstatus[num] !== e.flow) {
            this.cstatus[num] = e.flow
            this.nstatus[num] = e.nflow
          }
          if (e.log.length !== log.value.length) {
            log.value = e.log
            log.scrollTo(0, log.scrollHeight)
          }
          if (e.status === 'running') {
            // this.runCard('run', e.card)
            this.sleep(800).then(() => {
              this.run(e.card, e.status)
            })
          } else if (e.status === 'pass') {
            // this.runCard('stop', e.card)
            c = document.getElementById('c' + num)
            c.style.color = 'seagreen'
            c = document.getElementById('n' + num)
            c.style.color = 'seagreen'
            // this.pass[num] = e.pass
            // this.total[num] = (e.pass + e.fail)
            this.$emit('updateNum', num, e.pass, e.fail)
            this.$refs['run' + num].setAttribute('status', 'false')
          } else if (e.status === 'fail') {
            // this.runCard('stop', e.card)
            c = document.getElementById('c' + num)
            c.style.color = '#d96c4e'
            c = document.getElementById('n' + num)
            c.style.color = '#d96c4e'
            // this.fail[num] = e.fail
            // this.total[num] = (e.pass + e.fail)
            this.$emit('updateNum', num, e.pass, e.fail)
            this.$refs['run' + num].setAttribute('status', 'false')
          }
        })
        .catch((error) => console.log(error))
    },
    sleep (time) {
      return new Promise((resolve) => setTimeout(resolve, time))
    },
    rman (r) {
      var a
      const id = 'q' + r
      const chart = 'run' + r
      a = document.getElementById(id)
      setTimeout(function () {
        a.innerHTML = "<span class='las la-fire-alt' id='" + chart + "' style='font-size:5rem;color:seagreen'> </span>"
      }, 1000)
      setTimeout(function () {
        a.innerHTML = "<span class='las la-burn' id='" + chart + "' style='font-size:5rem;color:seagreen'> </span>"
      }, 2000)
      setTimeout(function () {
        a.innerHTML = "<span class='las la-fire' id='" + chart + "' style='font-size:5rem;color:seagreen'> </span>"
      }, 3000)
    },
    runCard (s, v) {
      if (s === 'run') {
        v === 'c1' && !(this.r1) ? this.r1 = setInterval(() => { this.rman('1') }, 3000)
          : v === 'c2' && !(this.r2) ? this.r2 = setInterval(() => { this.rman('2') }, 3000)
            : v === 'c3' && !(this.r3) ? this.r3 = setInterval(() => { this.rman('3') }, 3000)
              : v === 'c4' && !(this.r4) ? this.r4 = setInterval(() => { this.rman('4') }, 3000)
                : v === 'c5' && !(this.r5) ? this.r5 = setInterval(() => { this.rman('5') }, 3000)
                  : v === 'c6' && !(this.r6) ? this.r6 = setInterval(() => { this.rman('6') }, 3000)
                    : v === 'c7' && !(this.r7) ? this.r7 = setInterval(() => { this.rman('7') }, 3000)
                      : v === 'c8' && !(this.r8) ? this.r8 = setInterval(() => { this.rman('8') }, 3000)
                        : console.log('no card')
      } else {
        this.$refs['run' + v[1]].setAttribute('status', 'false')
        if (v === 'c1') {
          clearInterval(this.r1)
          this.r1 = 0
        } else if (v === 'c2') {
          clearInterval(this.r2)
          this.r2 = 0
        } else if (v === 'c3') {
          clearInterval(this.r3)
          this.r3 = 0
        } else if (v === 'c4') {
          clearInterval(this.r4)
          this.r4 = 0
        } else if (v === 'c5') {
          clearInterval(this.r5)
          this.r5 = 0
        } else if (v === 'c6') {
          clearInterval(this.r6)
          this.r6 = 0
        } else if (v === 'c7') {
          clearInterval(this.r7)
          this.r7 = 0
        } else if (v === 'c8') {
          clearInterval(this.r8)
          this.r8 = 0
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.scriptname {
  position: relative;
  bottom: 16px;
  color: #673ab7;
}

.text3d {
  /*color: #70869d;*/
  letter-spacing: .18em;
  text-shadow:
    2px 4px 5px rgba(0, 0, 0, 0.6),
    3px 4px 10px rgba(0, 0, 0, 0.3),
    5px 4px 15px rgba(0, 0, 0, 0.5),
    6px 4px 25px rgba(0, 0, 0, 0.6);
 }

.slide-enter {
  top: 10px;
  opacity: 0.5;
}

.slide-enter-active, .slide-leave-active {
  transition: all .15s;
}

.slide-enter-to {
  top: 0px;
  opacity: 1;
}

.slide-leave {
  top: 0px;
  opacity: 1;
}

.slide-leave-to {
  top: -20px;
  opacity: 0;
  transform: translateY(-18px);
}

.one-third {
  width: 33%;
  float: left;
  padding: 10px 10px;
  /*transition: opacity .5s;*/
}

.one-third.stat {
  position: flex;
  font-size: 24px;
  margin-bottom: 5px;
}

.one-third.stat-value {
  text-transform: uppercase;
  font-weight: 400;
  font-size: 12px;
}

.multi-button {
  z-index:0;
  position: absolute;
  top:1.25rem;
  left:1.25rem;
  border-radius:100%;
  width:0rem;
  height:0rem;
  transform: translate(-50%, -50%);
  transition: .5s cubic-bezier(0.25, 0, 0, 1);
}

.multi-button button {
  display: grid;
  place-items: center;
  position: absolute;
  font-size: 1.4rem;
  width:2.2rem;
  height:2.2rem;
  border:none;
  border-radius:100%;
  background: #ffffff00;
  color: transparent;
  transform: translate(-50%, -50%);
  cursor: pointer;
  box-shadow:0 0 0rem -.25rem #FFFFFF;
}

.textlog {
  /*display: none;*/
  position: absolute;
  width: 100%;
  height: 100%;
  top:0;
  left:0;
  padding: .3rem;
  transition: 0.5s;
  opacity: 0;
  visibility: hidden;
  /*margin-left: 10px;*/
}

.textlog.active {
  opacity: 1;
  visibility: visible;
  transition-delay: 0.01s;
}

#sidebar-toggle {
  display: none;
}

.body-label {
  position: fixed;
  height: 100%;
  width: calc(100% - 230px);
  z-index: 30;
  right: -100%;
  top: 0;
}

.main-content {
  margin-left: 230px;
  transition: margin-left 300ms;
}

main {
  padding: 1.5rem;
  /*background: #f1f5f9;*/
  min-height: calc(100vh - 70px);
  margin-top: 70px;
  height: 100%;
  /* max-height: 600px; */
  /*width: 1000px;*/
  background-color: hsl(209deg 100% 59% / 20%);
  background-image:
    url('../../static/image/tumblr_p7n8kqHMuD1uy4lhuo1_540.png'),
    url('../../static/image/tumblr_p7n908E1Jb1uy4lhuo1_1280.png'),
    url('../../static/image/tumblr_p7n8kqHMuD1uy4lhuo2_1280.png'),
    url('../../static/image/tumblr_p7n8on19cV1uy4lhuo1_1280.png'),
    url('../../static/image/tumblr_p7n8kqHMuD1uy4lhuo3_1280.png');
  background-repeat: repeat-x;
  background-position:
    0 30%,
    0 100%,
    0 50%,
    0 100%,
    0 0;
  background-size:
    2500px,
    800px,
    500px 200px,
    1000px,
    400px 260px;
  animation: 100s para infinite linear;
}

@keyframes para {
  100% {
    background-position:
    -5000px 20%,
    -800px 95%,
    500px 50%,
    1000px 100%,
    400px 0;
  }
}

.metrics {
  border-top: none;
  border-left: none;
  border-right: none;
  border-bottom-width: 3px;
  text-align:center;
  outline: none;
  background-color: transparent;
}

.header-input input {
  border: none;
  border-bottom: 3px solid #404040;
  font-size: 1.2rem;
  background-color: transparent;
  text-align:center;
  text-transform: uppercase;
}

.header-input input:focus {
  outline:none;
}

.page-header {
  display: flex;
  justify-content: space-between;
}

.header-actions button {
  outline: none;
  color: #fff;
  background: #4cad89;
  border: none;
  padding: .6rem 1rem;
  margin-left: 1rem;
  border-radius: 3px;
  font-weight: 600;
}

.header-actions button span {
  font-size: 1.2rem;
  margin-right: .6rem;
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 0.3fr);
  min-height: calc(40vh - 70px);
  /*width: 230px;*/
  grid-gap: 5.5rem;
  margin-top: 2rem;
/*  margin-left: 4rem;
  margin-right: 4rem;*/
  padding: 80px;
}

.cards textarea {
  padding: .1rem .4rem;
  background:#39395200;
  border-radius: 5px;
  width: 100%;
  height: 100%;
  /*height: calc(25vh - 70px);*/
  white-space: pre;
  overflow-wrap: normal;
  overflow-x: auto;
  font-size: 1rem;
  color: #0120cc;
  resize:none;
  outline: none;
  border: none;
}

.cards textarea::placeholder {
  position: relative;
  color: rgb(85 85 85 / 70%);
  /*color: #555555;*/
  font-size: 1rem;
  text-align: center;
  top:50%;
  transform:translateY(-50%);
}

.cards textarea::-webkit-scrollbar {
  cursor: auto;
  width: 7px;
  height: 7px;
  background-color: whitesmoke;
}

.cards textarea::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgb(0 0 0 / 30%);
  border-radius: 10px;
  background-color: whitesmoke;
}

.cards textarea::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgb(0 0 0 / 30%);
  background-color: #555555;
}

.card textarea:focus {
  outline: none;
  border:dotted 2px;
}

.card-single {
  /*min-height: calc(40vh - 120px);*/
  border-radius: 5px;
  background: #eeeeeef5;
  /*background: #fff;*/
  padding: .5rem;
  box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
  transform: scale(1,1);
  transition: all 0.2s ease-out;
}

/*.card-single:hover .card-flex {
  display: none;
}*/

.card-single:hover .multi-button button:nth-child(1) {
  background: #607d8b;
  color: black;
  left: 37%;
  top: 18%;
}

.card-single:hover .multi-button button:nth-child(2) {
  background: #e91e63;
  color: white;
  left: 18%;
  top: 37%;
}

.card-single:hover .multi-button, .multi-button:focus-within {
  width:10rem;
  height:10rem;
}

.card-flex {
  display: inline-block;
  text-align: center;
  padding: .1rem .4rem;
  padding-bottom: .3rem;
  z-index: 1;
}

.card-head {
  display: inline-block;
  border-bottom: 1.5px solid #888;
}

.card-head span {
  text-transform: uppercase;
  color: #555;
  width: 12px;
  font-size: 1px;
  font-family: 'Courier New';
  font-weight: bold;
  /*padding-right: 8px;*/
  visibility: none;
}

.card-head small {
  font-weight: 600;
  color: #555;
}

.card-info {
  visibility: hidden;
}

.hactive {
  visibility: visible;
}

.card-info h2 {
  font-size: 2.2rem;
  color: #333;
}

.card-chart span {
  font-size: 5rem;
}

.card-chart.success span {
  color: seagreen;
}

.card-chart.danger span {
  color: tomato;
}

.card-chart.yellow span {
  color: orangered;
}

.job-grid {
  margin-top: 3rem;
  display: grid;
  grid-template-columns: auto 66%;
  grid-gap: 3rem;
}

.analytics-card {
  background: #fff;
  padding: 1.5rem;
}

.analytics-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.analytics-head span {
  font-size: 1.5rem;
}

.analytics-chart small {
  font-weight: 600;
  color: #555;
  display: block;
  margin-bottom: 1rem;
}

.chart-circle {
  height: 150px;
  width: 150px;
  border-left: 10px solid transparent;
  border-right: 10px solid #5850ec;
  border-bottom: 10px solid #5850ec;
  border-top: 10px solid #5850ec;
  display: grid;
  place-items: center;
  margin: auto;
  border-radius: 50%;
  margin-bottom: 3rem;
}

.analytics-card button {
  display: block;
  padding: .6rem 1rem;
  width: 100%;
  height: 45px;
  background: #5850ec;
  color: #fff;
  border: 1px solid #5850ec;
  border-radius: 3px;
}

.jobs h2 small {
  color: #5850ec;
  font-weight: 600;
  display: inline-block;
  margin-left: 1rem;
  font-size: .9rem;
}

.jobs table {
  border-collapse: collapse;
  margin-top: 1rem;
}

span.indicator {
  background: #c9f7f5;
  height: 15px;
  width: 15px;
  border-radius: 50%;
}

span.indicator.even {
  background: #fff4de;
  height: 15px;
  width: 15px;
  border-radius: 50%;
}

.jobs table td div {
  background: #fff;
  margin-bottom: .8rem;
  height: 60px;
  display: flex;
  align-items: center;
  padding: .5rem;
  font-size: .85rem;
  color: #444;
}

table button {
  background: #8da2fb;
  color: midnightblue;
  border: 1px solid #8da2fb;
  padding: .5rem;
  border-radius: 3px;
}

.table-responsive {
  overflow: auto;
}

@media only screen and (max-width: 1385px) {
  .main-content {
      margin-left: 0;
  }
  .cards {
      grid-template-columns: repeat(3, 1fr);
  }
}

@media only screen and (max-width: 1178px) {
  .main-content {
      margin-left: 0;
  }
  .cards {
      grid-template-columns: repeat(2, 1fr);
  }
}

@media only screen and (max-width: 768px) {
  .cards {
      grid-template-columns: 100%;
  }
  .jobs-grid {
      grid-template-columns: 100%;
  }
}
</style>
