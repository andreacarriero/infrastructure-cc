<template>
  <section>
    <div class="container">
      <h1 class="title is-1 has-text-centered">[COMPANY NAME]</h1>
      <h2 class="title is-2 has-text-centered">NODES WITH ERRORS</h2>
      <nodestable :nodes="notOnlineNodes" :areNodesLoading="areNodesLoading" />
    </div>
  </section>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      notOnlineNodes: [],
      areNodesLoading: true
    }
  },

  created () {
    // get noy-online nodes
    this.areNodesLoading = true
    HTTP.get('/admin/nodes')
    .then(response => {
      let allNodes = response.data
      this.notOnlineNodes = allNodes.filter(function (node) {
        return node.status.current_status !== 'online'
      })
      this.areNodesLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  }
}
</script>
