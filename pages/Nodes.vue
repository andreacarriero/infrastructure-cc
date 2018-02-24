<template>
  <div class="container">
    <h1 class="title is-1 has-text-centered">NODES</h1>

    <!-- start datacenters table -->
      <b-table
        :data="nodes"
        :loading="areNodesLoading">

        <template slot-scope="props">
            <b-table-column field="id" label="ID">{{props.row.id}}</b-table-column>
            <b-table-column field="name" label="Name">
              <copy :text="props.row.name"/>
            </b-table-column>
            <b-table-column field="type" label="Type">{{props.row.type}}</b-table-column>
            <b-table-column field="ips" label="IPs">
              <div v-for="ip in props.row.ips" :key="ip.id" attached>
                IPv{{ip.ipv}} <code><copy :text="ip.ip"/>/{{ip.netmask}}</code>
              </div>
            </b-table-column>
            <b-table-column field="status" label="Status">
              <div v-if="props.row.status">
                <span v-if="props.row.status.imposed_status == props.row.status.current_status">
                  <span v-html="colorStatus(props.row.status.current_status)"/>
                </span>
                <span v-if="props.row.status.imposed_status != props.row.status.current_status">
                  {{props.row.status.imposed_status}} --> {{props.row.status.current_status}}
                </span>
              </div>
            </b-table-column>
            <b-table-column field="lastUpdate" label="Last Update">
              <b-tooltip v-if="props.row.status" :label="props.row.status.last_update" dashed>
                {{props.row.status.last_update | timeSince}} ago
              </b-tooltip>
            </b-table-column>

            <b-table-column field="actions" label="Actions">
              <router-link :to="{name: 'node', params: {id: props.row.id}}" class="button is-small">Open</router-link>
            </b-table-column>
          </template>
      </b-table>
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
    HTTP.get('/nodes/')
    .then(response => {
      this.nodes = response.data
      this.areNodesLoading = false
    })
    .catch(e => {
      console.log(e)
    })
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
