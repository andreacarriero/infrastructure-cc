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
              <td><timesince :time="currentNode.node.status.last_update" /></td>
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
              <username :userID="props.row.user_id" />
            </b-table-column>

            <b-table-column field="name" label="Name">
              {{props.row.name}}
            </b-table-column>

            <b-table-column field="nodes" label="Nodes">
              <b-collapse :open="false">
                <a slot="trigger">
                  {{props.row.nodes_ids.length}}
                  <span v-if="props.row.nodes_ids.length == 1">node</span>
                  <span v-if="props.row.nodes_ids.length != 1">nodes</span>
                </a>
                <div v-for="node_id in props.row.nodes_ids" :key="node_id">
                  <nodename :nodeID="node_id" />
                  <router-link :to="{name: 'node', params: {id: node_id}}">
                    <i class="fa fa-external-link"></i>
                    Open
                  </router-link>
                </div>
              </b-collapse>
            </b-table-column>

            <b-table-column field="actions" label="Actions">
              <router-link :to="{name: 'project', params: {id: props.row.id}}" class="button is-small">Open</router-link>
            </b-table-column>
          </template>
        </b-table>
      </div>

      <div>
        <br><br>
        <h2 class="title is-2 has-text-centered">NODE COMMANDS</h2>
        <commandstable :commands="currentNodeCommands" :areCommandsLoading="areCurrentNodeCommandsLoading" />
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
        isDatacenterLoading: true,
        currentNodeCommands: [],
        areCurrentNodeCommandsLoading: true
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

    // get node commands
    this.areCurrentNodeCommandsLoading = true
    HTTP.get('/admin/nodes/' + this.currentNodeID + '/commands')
    .then(response => {
      this.currentNodeCommands = response.data
      this.areCurrentNodeCommandsLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  },

  computed: {
    isLoading () {
      return this.isCurrentNodeLoading
    }
  }
}
</script>
