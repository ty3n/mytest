<template>
  <SideBar :checked="checked" @togglebar="toggledrop"/>
  <Header :checked="checked"/>
  <router-view @btoggle="toggleSetting" @mountscript="mountscript" :data="data" @updateNum="updateNum"/>
  <div v-if="showSetting">
    <Setting :header="header" @updateNum="updateNum" @mountscript="mountscript" :checked="checked" @close="toggleSetting" />
  </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'
import Header from '@/components/Header.vue'
import Setting from '@/components/Setting.vue'

export default {
  name: 'App',
  components: {
    SideBar,
    Header,
    Setting
  },
  data () {
    return {
      checked: true,
      header: 'Import Repository',
      showSetting: false,
      data: {
        scriptname: '___',
        pass: [0, 0, 0, 0, 0, 0, 0, 0],
        fail: [0, 0, 0, 0, 0, 0, 0, 0],
        total: [0, 0, 0, 0, 0, 0, 0, 0]
      }
    }
  },
  methods: {
    toggledrop () {
      this.checked = !this.checked
      // console.log(this.checked)
    },
    toggleSetting () {
      this.showSetting = !this.showSetting
    },
    mountscript (r) {
      this.data.scriptname = r
    },
    updateNum (i, p, f) {
      // console.log(i, p, f)
      this.data.pass[i] = p
      this.data.fail[i] = f
      this.data.total[i] = (p + f)
    }
  }
}
</script>

<style scoped>
@import '../static/css/1.3.0/css/line-awesome.css';
@import '../static/css/font.css';

</style>
