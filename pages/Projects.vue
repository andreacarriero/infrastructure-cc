<template>
  <div class="container">
    <h1 class="title is-1 has-text-centered">PROJECTS</h1>
    <projectstable :projects="projects" :areProjectsLoading="areProjectsLoading" />
  </div>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      projects: [],
      areProjectsLoading: true
    }
  },

  mounted () {
    // get projects
    this.areProjectsLoading = true
    HTTP.get('/admin/projects')
    .then(response => {
      this.projects = response.data
      this.areProjectsLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  }
}
</script>
