<template>
  <span>{{nodename}}</span>
</template>

<script>
import {HTTP} from '../services/http'
export default {
  name: 'nodename',
  props: ['nodeID'],
  data () {
    return {
      nodename: "[LOADING]"
    }
  },

  created () {
    // get user
    HTTP.get('/admin/nodes/' + this.nodeID)
    .then(response => {
      this.nodename = response.data.node.name
    })
    .catch(e => {
      this.nodename = "[ERROR]"
      console.log(e)
    })
  }
}
</script>
