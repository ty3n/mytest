<template>
    <input type="checkbox" name="" id="sidebar-toggle" :checked="checked" @click="handleChange"/>
    <div class="sidebar">
        <div class="sidebar-brand">
            <div class="brand-flex">
                <img src="" width="40px" alt="">
                <div class="brand-icons">
                    <span class="las la-bell"></span>
                    <span class="las la-user-circle"></span>
                </div>
            </div>
            <div class="sidebar-menu">
                <div class="menu-head">
                    <span>Dashboard</span>
                </div>
                <ul>
                    <li>
                        <a href="">
                            <span class="las la-balance-scale"></span>
                            Finance
                        </a>
                    </li>
                    <li>
                        <a href="">
                            <span class="las la-chart-pie"></span>
                            Analytics
                        </a>
                    </li>
                </ul>
                <div class="menu-head">
                    <span>Applications</span>
                </div>
                <ul>
                    <li>
                        <a href="">
                            <span class="las la-calendar"></span>
                            Calendar
                        </a>
                    </li>
                    <li>
                        <a href="">
                            <span class="las la-users"></span>
                            Contacks
                        </a>
                    </li>
                    <li>
                        <a href="">
                            <span class="las la-shopping-cart"></span>
                            Ecommerce
                        </a>
                    </li>
                    <li>
                        <a href="">
                            <span class="las la-envelope"></span>
                            Mailbox
                        </a>
                    </li>
                    <li>
                        <a href="">
                            <span class="las la-check-circle"></span>
                            Tasks
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
// import Setting from '@/components/Setting.vue'

export default {
  props: ['checked'],
  emits: ['togglebar'],
  methods: {
    handleChange () {
      this.$emit('togglebar')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

#sidebar-toggle {
    display: none;
}

#sidebar-toggle:checked ~ .sidebar {
    left: -100%;
}

#sidebar-toggle:checked ~ .main-content header {
    left: 0;
    width: 100%;
    right: 0;
}

#sidebar-toggle:checked ~ .main-content {
    margin-left: 0;
}

.sidebar {
    width: 230px;
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    padding: 1rem 1.5rem;
    background: #0C4B33;
    color: #fff;
    z-index: 20;
    transition: left 300ms;
}

.sidebar-brand {
    height: 90px;
}

.brand-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand-icons span {
    font-size: 1.5rem;
    margin-left: .5rem;
}

.sidebar-user {
    margin: 1rem 0rem 1rem 0rem;
    text-align: center;
}

.sidebar-user img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border-left: 2px solid transparent;
    border-right: 2px solid #efefef;
    border-bottom: 2px solid #efefef;
    border-top: 2px solid transparent;
}

.sidebar-user h3 {
    font-size: 1rem;
}

.sidebar-user span {
    font-size: .8rem;
}

.sidebar-menu {
    margin-top: 2.5rem;
}

.menu-head {
    text-transform: uppercase;
    color: #8da2fb;
    font-size: .75rem;
    font-weight: 500;
    margin-bottom: .8rem;
}

.sidebar-menu ul {
    margin-bottom: 1.5rem;
}

.sidebar-menu li {
    margin-bottom: .9rem;
    display: flex;
    align-items: center;
}

.sidebar-menu li a {
    color: #efefef;
    font-size: .9rem;
    display: flex;
    align-items: center;
}

.sidebar-menu li a span {
    font-size: 1.5rem;
    display: inline-block;
    margin-right: .8rem;
}

@media only screen and (max-width: 1385px) {
    .sidebar {
        left: -100%;
        /*z-index: 30;*/
    }
    #sidebar-toggle:checked ~ .sidebar {
        left: 0;
    }
    #sidebar-toggle:checked ~ .body-label {
        right: 0;
    }
}

@media only screen and (max-width: 1178px) {
    .sidebar {
        left: -100%;
        /*z-index: 30;*/
    }
    header {
        left: 0;
        width: 100%;
    }
    #sidebar-toggle:checked ~ .sidebar {
        left: 0;
    }
    #sidebar-toggle:checked ~ .body-label {
        right: 0;
    }
}

@media only screen and (max-width: 768px) {
    .header-input {
        margin-bottom: 20px;
    }
    .page-header {
        display: block;
    }
    .header-actions button:first-child {
        margin-left: 0rem;
    }
}

</style>
