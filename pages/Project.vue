<template>
  <section>
    <b-loading :active.sync="isLoading"></b-loading>
    <div v-if="!isLoading" class="container">
      <h1 class="title is-1 has-text-centered">PROJECT: <copy :text="currentProject.project.name"/></h1>
      <p class="has-text-centered">
        <b>ID:</b> <code>{{currentProject.project.id}}</code>;
        <b>User:</b> <code><username :userID="currentProject.project.user_id"/></code>;
      </p>

      <div>
        <br><br>
        <h2 class="title is-2 has-text-centered">HOSTED ON</h2>
        <nodestable :nodes="currentProject.nodes" :areNodesLoading="false" />
      </div>

    </div>
  </section>  
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      currentProject: {},
      isProjectLoading: true
    }
  },

  mounted () {
    // get project
    this.isProjectLoading = true
    HTTP.get('/admin/projects/' + this.$route.params.id)
    .then(response => {
      this.currentProject = response.data
      this.isProjectLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  },

  computed: {
    isLoading () {
      return this.isProjectLoading
    }
  }
  
}
</script>
