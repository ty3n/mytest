<template>
    <header>
        <div class="menu-toggle">
            <label for="sidebar-toggle">
                <span class="las la-bars"></span>
            </label>
        </div>
        <div class="header-icons">
            <span class="las la-search"></span>
            <span class="las la-bookmark"></span>
            <span class="las la-sms"></span>
        </div>
    </header>
</template>

<style scoped>

header {
    height: var(--header-height);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    position: fixed;
    left: 230px;
    width: calc(100% - 230px);
    top: 0;
    z-index: 20;
    background: #fff;
    box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
    transition: left 300ms;
}

.header-icons span {
    display: inline-block;
    margin-left: .7rem;
    font-size: 1.4rem;
}

.menu-toggle label {
    height: 60px;
    width: 60px;
    display: grid;
    place-items: center;
    font-size: 1.5rem;
    border-radius: 50%
}

.menu-toggle label:hover {
    background: #efefef;
}

.main-content {
    margin-left: 250px;
    transition: margin-left 300ms;
}

#sidebar-toggle:checked ~ .sidebar {
    left: -100%;
}

#sidebar-toggle:checked ~ header {
    left: 0;
    width: 100%;
    right: 0;
}

#sidebar-toggle:checked ~ .main-content {
    margin-left: 0;
}

@media only screen and (max-width: 1385px) {
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

@media only screen and (max-width: 1178px) {
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
