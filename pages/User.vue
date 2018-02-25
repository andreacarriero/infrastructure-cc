<template>
  <section>
      <b-loading :active.sync="isCurrentUserLoading"></b-loading>
      <div v-if="currentUser" class="container">
          <h1 class="title is-1 has-text-centered">USER: <copy :text="currentUser.user.username"/></h1>
          <p class="has-text-centered"><b>ID:</b> <code>{{currentUser.user.id}}</code>;</p>

          <div>
              <br><br>
              <projectstable :projects="currentUser.projects" :areProjectsLoading="false" />
          </div>
      </div>
  </section>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
      return {
          currentUser: null,
          isCurrentUserLoading: true
      }
  },

  created () {
      // get user
      this.isCurrentUserLoading = true
      HTTP.get('/admin/users/' + this.$route.params.id)
      .then(response => {
          this.currentUser = response.data
          this.isCurrentUserLoading = false
      })
      .catch(e => {
          console.log(e)
      })
  }
}
</script>
