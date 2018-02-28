<template>
  <section>
    <b-loading :active.sync="isLoading"></b-loading>

    <div v-if="currentDatacenter" class="container">
        <h1 class="title is-1 has-text-centered">DATACENTER: {{currentDatacenter.datacenter.name}}</h1>
        <p class="has-text-centered">
          <b>ID:</b> <code>{{currentDatacenter.datacenter.id}}</code>;
          <b>Location:</b> <code>{{currentDatacenter.datacenter.location}}</code>;
        </p>
        <p v-if="currentDatacenter.datacenter.latitude && currentDatacenter.datacenter.longitude" class="has-text-centered">
          <b>Coordinates:</b> <code>{{currentDatacenter.datacenter.latitude}}, {{currentDatacenter.datacenter.longitude}}</code>;
        </p>

        <br><br>

        <h2 class="title is-2 has-text-centered">NODES</h2> 
        <nodestable :nodes="currentDatacenter.nodes" :areNodesLoading="false" />
    </div>  
  </section>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      currentDatacenterID: this.$route.params.id,
      currentDatacenter: null,
      isCurrentDatacenterLoading: true
    }
  },

  mounted () {
    // get current datacenter
    this.isCurrentDatacenterLoading = true
    HTTP.get('/admin/datacenters/' + this.currentDatacenterID)
    .then(response => {
      this.currentDatacenter = response.data
      this.isCurrentDatacenterLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  },

  computed: {
    isLoading () {
      return this.isCurrentDatacenterLoading
    }
  },

  methods: {
    colorStatus (status) {
      if (status == 'online') {
        return '<span class="tag is-success">ONLINE</span>'
      } else if (status == 'offline') {
        return '<span class="tag is-danger">OFFLINE</span>'
      } else {
        return '<span class="tag is-warning">' + status + '</span>'
      }
    }
  },

  filters: {
    timeSince (date) {
      var seconds = Math.floor((new Date() - new Date(date)) / 1000);
      var interval = Math.floor(seconds / 31536000);
      if (interval > 1) {
        return interval + " years";
      }
      interval = Math.floor(seconds / 2592000);
      if (interval > 1) {
        return interval + " months";
      }
      interval = Math.floor(seconds / 86400);
      if (interval > 1) {
        return interval + " days";
      }
      interval = Math.floor(seconds / 3600);
      if (interval > 1) {
        return interval + " hours";
      }
      interval = Math.floor(seconds / 60);
      if (interval > 1) {
        return interval + " minutes";
      }
      return Math.floor(seconds) + " seconds";
    }
  }
}
</script>
