<template>
  <section>
    <b-loading :active.sync="isLoading"></b-loading>
    <div v-if="currentNode" class="container">
      <h1 class="title is-1 has-text-centered">NODE: <copy :text="currentNode.node.name"/></h1>
      <p class="has-text-centered">
        <b>ID:</b> <code>{{currentNode.node.id}}</code>;
        <b>TYPE:</b> <code>{{currentNode.node.type}}</code>;
      </p>
      <p class="has-text-centered">
        <b>Datacenter Name:</b> <span v-if="datacenter">{{datacenter.datacenter.name}}</span> <span v-if="isDatacenterLoading" class="button is-loading"/>
      </p>
      <p class="has-text-centered">
        <b>Datacenter Location:</b> <code>{{currentNode.datacenter.location}}</code>
      </p>

      <div v-if="currentNode.node.status">
        <br><br>
        <h2 class="title is-2 has-text-centered">NODE STATUS</h2>
        <table class="table is-bordered is-fullwidth">
          <tbody>
            <tr>
              <th>Imposed Status</th>
              <td>{{currentNode.node.status.imposed_status}}</td>
            </tr>

            <tr>
              <th>Current Status</th>
              <td>{{currentNode.node.status.current_status}}</td>
            </tr>

            <tr>
              <th>Last Update</th>
              <td>{{currentNode.node.status.last_update | timeSince}} ago<br>{{currentNode.node.status.last_update}}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div>
        <br><br>
        <h2 class="title is-2 has-text-centered">NODE IPs</h2>
        <table class="table is-bordered is-fullwidth">
          <thead>
            <tr>
              <th>IP Type</th>
              <th>IP</th>
              <th>Netmask</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ip in currentNode.node.ips" :key="ip.id">
              <td>IPv{{ip.ipv}}</td>
              <td><copy :text="ip.ip"/></td>
              <td>{{ip.netmask}}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div>
        <br><br>
        <h2 class="title is-2 has-text-centered">HOSTED PROJECTS</h2>
        <b-table :data="currentNode.hosted_projects">
          <template slot-scope="props">
            <b-table-column field="id" label="ID">
              {{props.row.id}}
            </b-table-column>

            <b-table-column field="user" label="User">
              <span v-bind:id="'project-' + props.row.id" />
              {{getUserName(props.row.user_id, props.row.id)}}
            </b-table-column>

            <b-table-column field="name" label="Name">
              {{props.row.name}}
            </b-table-column>

            <b-table-column field="nodes" label="Nodes">
              <div v-for="node_id in props.row.nodes_ids" :key="node_id">
                <span v-bind:id="'node-name-' + node_id" />
                <router-link :to="{name: 'node', params: {id: node_id}}">
                  <i class="fa fa-external-link"></i>
                  Open
                </router-link>
                {{getNodeName(node_id)}}
              </div>
            </b-table-column>
          </template>
        </b-table>
      </div>

    </div>
  </section>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
        currentNodeID: this.$route.params.id,
        currentNode: null,
        isCurrentNodeLoading: true,
        datacenter: null,
        isDatacenterLoading: true
    }
  },

  mounted () {
    // get node
    this.isCurrentNodeLoading = true
    HTTP.get('/admin/nodes/' + this.currentNodeID)
    .then(response => {
      this.currentNode = response.data
      this.isCurrentNodeLoading = false

      // get datacenter
      this.isDatacenterLoading = true
      HTTP.get('/admin/datacenters/' + response.data.node.datacenter_id)
      .then(response => {
        this.datacenter = response.data
        this.isDatacenterLoading = false
      })
    })
    .catch(e => {
      console.log(e)
    })
  },

  computed: {
    isLoading () {
      return this.isCurrentNodeLoading
    }
  },

  methods: {
    getUserName (user_id, project_id) {
      var element = document.querySelector('#project-' + project_id)
      if (element) {
        HTTP.get('/admin/users/' + user_id)
        .then(response => {
          let user = response.data.user
          let userName = user.username
          element.innerHTML = userName
        })
        .catch(e => {
          console.log(e)
          element.innerHTML = "[ERROR]"
        })
      }
    },

    getNodeName (node_id) {
      var element = document.querySelector('#node-name-' + node_id)
      if (element) {
        HTTP.get('/nodes/' + node_id)
        .then(response => {
          let node = response.data.node
          let nodeName = node.name
          element.innerHTML = nodeName
        })
        .catch(e => {
          console.log(e)
          element.innerHTML = "[ERROR]"
        })
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
