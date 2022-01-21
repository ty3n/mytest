<template>
  <div id="backdrop" class="backdrop" v-bind:class="{ dropa: checked }">
<!--     <div id="wrapper">
      <div class="loading-bar">
        <div class="progress-bar"></div>
      </div>
      <div class="status">
        <span class="state">Loading</span>
        <div class="percentage">5%</div>
      </div>
    </div> -->
    <div v-on:keyup.enter="search" class="modal list" :class="{ sale: theme === 'sale' }">
      <!-- <div class="modal list" :class="{ sale: theme === 'sale' }" @click="closeSetting"> -->
      <i class="las la-times close df ac jc" @click="closeSetting"></i>
      <h2>{{ header }}</h2>
      <!-- <p>modal content</p> -->
      <h4 class="ui df ac header">
        <div>
          Repository
          <span class="ui grey label ml-3"> {{repolen}} </span>
        </div>
        <div v-if="showper" class="status">
          <div class="state">Loading</div>
          <div class="percentage">{{percent}}%</div>
        </div>
      </h4>
      <div class="loading-bar">
        <div class="progress-bar" :style="'width:' + percent + '%'"></div>
      </div>
      <div class="ui segment">
        <div class="ui fluid input icon">
          <input placeholder="Search Repository..." v-model="v">
          <i class="las la-search icon df ac jc"></i>
        </div>
        <div>
          <ul>
            <div v-if="loading" class="loader"></div>
            <li v-else v-for="repo in repos" :key="repo.id" class="df ac lk">
              <span class="las la-book"></span>
              <a :class="{pointernon: pointer}" href="#" @click="pointer=true, download(repo.full_name,'post')">{{repo.full_name}}</a>
            </li>
            <li>
              <div class="center">
                <div class="ui pagination menu">
                  <a class="df ac jc" title="上一頁">
                    <i class="las la-angle-left" :class="disabled" @click="lastpage"></i>
                  </a>
                  <a class="page">{{page}}</a>
                  <a class="df ac jc" title="下一頁">
                    <i class="las la-angle-right" @click="nextpage"></i>
                  </a>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'Setting',
  emits: ['updateNum', 'mountscript', 'close'],
  props: ['header', 'theme', 'checked', 'data'],
  data () {
    return {
      repos: [],
      repolen: 0,
      v: '',
      page: 1,
      loading: false,
      percent: 0,
      showper: false,
      pointer: false
    }
  },
  mounted () {
    const d = this.query('')
    const showd = async () => {
      const a = await d
      this.repos = []
      for (let i = 0; i < a.length; i++) {
        this.repos.push({
          id: a[i].id,
          full_name: a[i].full_name
        })
      }
      this.sleep(150).then(() => {
        this.loading = false
        this.repolen = this.repos.length
      })
    }
    showd()
  },
  computed: {
    disabled: function () {
      return {
        disabled: this.page < 2
      }
    }
  },
  methods: {
    emptyCnt () {
      // this.interval = setInterval(() => {
      //   this.pass[0]++
      // }, 500)
      for (let i = 1; i <= 8; i++) {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/api/data/',
          data: qs.stringify({
            card: 'c' + i.toString(),
            status: 'clean'
          }),
          headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
          }
        })
          .then(response => {
            console.log(response)
            const e = response.data
            var num = e.card[1] - 1
            // this.pass[num] = e.pass
            // this.fail[num] = e.fail
            // this.total[num] = (e.pass + e.fail)
            console.log(e.pass, e.fail)
            this.$emit('updateNum', num, e.pass, e.fail)
          })
          .catch((error) => console.log(error))
      }
    },
    closeSetting () {
      this.percent = 0
      this.$emit('close')
      // console.log(this.checked)
    },
    toggleper () {
      this.showper = !this.showper
    },
    download (r, m) {
      if (m === 'post') this.toggleper()
      axios({
        method: m,
        url: 'http://127.0.0.1:8000/api/dload/',
        data: qs.stringify({
          repo: r
        }),
        headers: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
      })
        .then(response => {
          if (response.data.percent !== 100) {
            if (response.data.percent !== this.percent) {
              this.percent = response.data.percent
              console.log(response.data.percent === this.percent)
              console.log(this.percent)
            }
            this.sleep(1000).then(() => {
              this.download(r, 'get')
            })
          } else if (response.data.percent === 100) {
            this.percent = 100
            this.sleep(2000).then(() => {
              this.emptyCnt()
              this.closeSetting()
              this.toggleper()
              this.pointer = false
              this.$emit('mountscript', r)
            })
          }
        })
        .catch((error) => console.log(error))
      // this.closeSetting()
    },
    getrepo (r) {
      console.log(r)
      const q = axios.get('http://172.25.70.190:8000/api/v1/repos/' + r + '/contents/', {}, {
        auth: {
          username: 'hitron',
          passwords: 'hitron'
        },
        headers: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
      })
      const qdata = q.then(response => response.data)
        .catch((error) => console.log(error))
      const showd = async () => {
        const s = await qdata
        console.log(s)
      }
      showd()
      // this.closeSetting()
    },
    nextpage () {
      this.page += 1
      const d = this.query(this.page)
      const showd = async () => {
        const a = await d
        this.repos = []
        for (let i = 0; i < a.length; i++) {
          this.repos.push({
            id: a[i].id,
            full_name: a[i].full_name
          })
        }
        this.sleep(150).then(() => {
          this.loading = false
          this.repolen = this.repos.length
        })
      }
      showd()
    },
    lastpage () {
      this.page > 1 ? this.page -= 1 : this.page = 1
      const d = this.query(this.page)
      const showd = async () => {
        const a = await d
        this.repos = []
        for (let i = 0; i < a.length; i++) {
          this.repos.push({
            id: a[i].id,
            full_name: a[i].full_name
          })
        }
        this.sleep(150).then(() => {
          this.loading = false
          this.repolen = this.repos.length
        })
      }
      showd()
    },
    query (page) {
      const q = axios.get('http://172.25.70.190:8000/api/v1/repos/search?page=' + page + '&limit=10&uid=0&exclusive=True&q=' + this.v, {}, {
        auth: {
          username: 'hitron',
          passwords: 'hitron'
        },
        headers: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
      })
      this.loading = true
      const qdata = q.then(response => response.data.data)
        .catch((error) => console.log(error))
      return qdata
    },
    search (event) {
      const d = this.query(this.page)
      const showd = async () => {
        const a = await d
        this.repos = []
        for (let i = 0; i < a.length; i++) {
          this.repos.push({
            id: a[i].id,
            full_name: a[i].full_name
          })
        }
        this.sleep(150).then(() => {
          this.loading = false
          this.repolen = this.repos.length
        })
      }
      showd()
    },
    sleep (time) {
      return new Promise((resolve) => setTimeout(resolve, time))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .pointernon {
    pointer-events:none;
  }
  #wrapper{
    left: 43%;
    top: 5%;
    position:relative;
    opacity:1;
    justify-content: center;
    z-index: 1;
  }
  .loading-bar{
    /*width:15%;*/
    height:2.3px;
    background:#dfe6e9;
    border-radius:5px;
    border:0px solid #0abde3;
  }
  .progress-bar{
    /*width:0%;*/
    height:100%;
    background:#7b63ff;
    border-radius:5px;
    border:0px solid #0abde3;
  }

  .status{
    display: flex;
    /*justify-content: space-between!important;*/
  }
  .state{
    font-size:0.9em;
    letter-spacing:1pt;
    text-transform:uppercase;
    color: rgba(136,136,136,1);
    transition: color .10s cubic-bezier(0.4, 0, 1, 1);
  }
  .state:hover {
    color: rgba(136,136,136,0);
  }
  .percentage{
    font-size:0.9em;
    color: rgba(136,136,136,1);
    margin-left: 15px;
  }
  .loader {
    position: relative;
    margin-top: 10px;
    margin-bottom: 2px;
    left: calc(50% - 1em);
    border: 2px solid #f3f3f3;
    -webkit-animation: spin 1s linear infinite;
    animation: spin 1s linear infinite;
    border-top: 2px solid #555;
    border-radius: 50%;
    width: 30px;
    height: 30px;
  }
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .close {
    position: absolute;
    right: 0px;
    top: 0px;
    width: 40px;
    height: 40px;
    opacity: 0.3;
    font-size: 1.4rem;
    color: #000000;
  }
  .close:hover {
    opacity: 1;
  }
  .las.disabled,
  .las[disabled],
  .disabled > .las,
  [disabled] > .las {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }
  .center {
    text-align: center;
  }
  .center .page {
    font-size: 1.2rem;
  }
  .center i {
    font-size: 1.2rem;
    margin-left: 2px;
    margin-right: 2px;
    opacity: 0.3;
  }
  .center i:hover {
    opacity: 1;
  }
  .ui.pagination.menu {
    margin: 0;
    display: inline-flex;
    al-align: middle;
  }
  .modal {
    width: 25%;
    top: 90px;
    padding: 10px;
    margin: auto;
    background: white;
    border-radius: 10px;
    position: relative;
  }
  .modal.list {
    list-style-type: none;
  }
  .backdrop {
    top: 30px;
    position: fixed;
    background: rgba(0,0,0,0.5);
    width: 100%;
    height: 100%;
    margin-left: 125px;
    transition: margin-left 300ms;
  }
  .dropa {
    margin-left: 0;
  }
  .backdrop h2 {
    color: #03cfb4;
    border: none;
    padding: 0;
    text-align: center;
  }
  .df {
    display: flex!important;
  }
  .ac {
    align-items: center!important;
  }
  .jc {
    justify-content: center!important;
  }
  .sb {
    justify-content: space-between!important;
  }
  .lk {
    padding: 2px 0em;
    border-bottom: 1.2px solid #dedede;
  }
  .ml-3 {
    margin-left: .5rem!important;
  }
  .label {
    background-color: #767676;
    border-color: #767676;
    color: #fff;
  }
  .ui.label {
    font-size: .85714286rem;
    display: inline-block;
    line-height: 1;
    vertical-align: baseline;
    margin: 0 .14285714em;
    background-color: #e8e8e8;
    background-image: none;
    padding: .5833em .833em;
    color: rgba(0,0,0,.6);
    text-transform: none;
    font-weight: 500;
    border: 0 solid transparent;
    border-radius: .28571429rem;
    transition: background .1s ease;
    padding: .3em .5em;
    background: #767676;
    color: white;
  }
  .ui.header {
    background: #fff;
    padding: .78571429rem 1rem;
    margin: 0 -1px;
    box-shadow: none;
    border: 1px solid #d4d4d5;
    border-radius: 0.28571429rem 0.28571429rem 0 0;
    position: relative;
    background: #f7f7f7;
    border-color: #dedede;
    justify-content: space-between!important;
  }
  .ui.fluid.input {
    display: flex;
  }
  .ui.input {
    position: relative;
    font-weight: 400;
    font-style: normal;
    display: inline-flex;
    color: rgba(0,0,0,.87);
  }
  .ui.input>input {
    margin: 0;
    max-width: 100%;
    flex: 1 0 auto;
    outline: none;
    -webkit-tap-highlight-color: rgba(255,255,255,0);
    text-align: left;
    line-height: 1.21428571em;
    padding: .67857143em 1em;
    background: #fff;
    border: 1px solid rgba(34,36,38,.15);
    color: rgba(0,0,0,.87);
    border-radius: .28571429rem;
    transition: box-shadow .1s ease,border-color .1s ease;
    box-shadow: none;
    padding-left: 2.67142857em;
    padding-right: 1em;
  }
  .ui.input>input:hover, .ui.input>input:focus {
    border: 1px solid #4183c4;
  }
  .ui.input i {
    -webkit-text-stroke: 1px;
  }
  .ui.segment {
    position: relative;
    background: #fff;
    box-shadow: 0 1px 2px 0 rgb(34 36 38 / 15%);
    margin: 0 0;
    padding: .5em .5em 0em;
    /*border-radius: .28571429rem;*/
    border: 1px solid rgba(34,36,38,.15);
  }
  .ui.input>i.icon {
    cursor: default;
    position: absolute;
    line-height: 1;
    text-align: center;
    top: 0;
    right: 0;
    margin: 0;
    height: 100%;
    width: 2.67142857em;
    opacity: .5;
    border-radius: 0 .28571429rem .28571429rem 0;
    transition: opacity .3s ease;
    left: 1px;
  }
  .ui span {
    font-size: 1.4rem;
  }
  @media only screen and (max-width: 1385px) {
    .backdrop {
      margin-left: 0;
    }
  }

</style>
