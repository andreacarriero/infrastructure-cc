<template>
  <span>{{username}}</span>
</template>

<script>
import {HTTP} from '../services/http'
export default {
  name: 'username',
  props: ['userID'],
  data () {
    return {
      username: "[LOADING]"
    }
  },

  created () {
    // get user
    HTTP.get('/admin/users/' + this.userID)
    .then(response => {
      this.username = response.data.user.username
    })
    .catch(e => {
      this.username = "[ERROR]"
      console.log(e)
    })
  }
}
</script>
