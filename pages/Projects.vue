<template>
  <div class="container">
      <h1 class="title is-1 has-text-centered">PROJECTS</h1>

      <!-- start projects table -->
        <b-table
          :data="projects"
          :loading="areProjectsLoading">

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
              <b-collapse :open="false">
                <a slot="trigger">
                  {{props.row.nodes_ids.length}}
                  <span v-if="props.row.nodes_ids.length == 1">node</span>
                  <span v-if="props.row.nodes_ids.length != 1">nodes</span>
                </a>
                <div v-for="node_id in props.row.nodes_ids" :key="node_id">
                  <span v-bind:id="'node-name-' + node_id" />
                  <router-link :to="{name: 'node', params: {id: node_id}}">
                    <i class="fa fa-external-link"></i>
                    Open
                  </router-link>
                  {{getNodeName(node_id)}}
                </div>
              </b-collapse>
            </b-table-column>

            <b-table-column field="actions" label="Actions">
              <router-link :to="{name: 'project', params: {id: props.row.id}}" class="button is-small">Open</router-link>
            </b-table-column>

          </template>
        </b-table>
      <!-- end projects table -->
  </div>
</template>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      projects: [],
      areProjectsLoading: true
    }
  },

  mounted () {
    // get projects
    this.areProjectsLoading = true
    HTTP.get('/admin/projects')
    .then(response => {
      this.projects = response.data
      this.areProjectsLoading = false
    })
    .catch(e => {
      console.log(e)
    })
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
  }
  
}
</script>
