<template>
  <div class="container">
    <h1 class="title is-1 has-text-centered">USERS</h1>
    <b-table :data="users" :loading="areUsersLoading">
      <template slot-scope="props">
        <b-table-column field="id" label="ID">{{props.row.id}}</b-table-column>
        <b-table-column field="username" label="Username">{{props.row.username}}</b-table-column>
        <b-table-column label="Actions">
          <router-link :to="{name: 'user', params: {id: props.row.id}}" class="button is-small">Open</router-link>
        </b-table-column>
      </template>
    </b-table>   
  </div>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      users: [],
      areUsersLoading: true
    }
  },

  created () {
    // get users
    this.areUsersLoading = true
    HTTP.get('/admin/users')
    .then(response => {
        this.users = response.data
        this.areUsersLoading = false
    })
    .catch(e => {
        console.log(e)
    })
  }
}
</script>
