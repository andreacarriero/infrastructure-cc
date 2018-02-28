<template>
  <div class="container">
    <h1 class="title is-1 has-text-centered">NODES</h1>

    <!-- start datacenters table -->
      <nodestable :nodes="nodes" :areNodesLoading="areNodesLoading" />
    <!-- end datacenters table -->
  </div>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      nodes: [],
      areNodesLoading: true
    }
  },

  mounted () {
    // get nodes
    this.areNodesLoading = true
    HTTP.get('/admin/nodes/')
    .then(response => {
      this.nodes = response.data
      this.areNodesLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  }
}
</script>
