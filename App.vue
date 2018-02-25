<template><div>
  <!-- start navbar -->
  <nav class="navbar is-transparent">
    <div class="navbar-brand">
      <router-link class="navbar-item" :to="{name: 'home'}">
        <b>CC ADMIN UI</b>
      </router-link>
      <div class="navbar-burger burger" data-target="navbar">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>

    <div id="navbar" class="navbar-menu">
      <div class="navbar-start">
        <router-link :to="{name: 'datacenters'}" class="navbar-item">Datacenters</router-link>
        <router-link :to="{name: 'nodes'}" class="navbar-item">Nodes</router-link>
        <router-link :to="{name: 'projects'}" class="navbar-item">Projects</router-link>
        <router-link :to="{name: 'users'}" class="navbar-item">Users</router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="field is-grouped">
            <p class="control">
              <a class="button is-primary" href="https://github.com/jgthms/bulma/archive/0.5.1.zip">
                <span class="icon">
                  <i class="fas fa-download"></i>
                </span>
                <span>Download</span>
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <!-- end navbar -->
  <router-view :key="$route.fullPath"/>
  <br><br><br><br><br>
</div></template>

<style lang="scss">
  @import url('https://fonts.googleapis.com/css?family=Cutive+Mono');
  
  body {
    font-family: 'Cutive Mono', monospace;
  }
</style>


<script>
export default {

}
</script>
