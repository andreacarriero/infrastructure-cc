<template>
  <section>
    <b-loading :active.sync="isLoading"></b-loading>
    <div v-if="!isLoading" class="container">
      <h1 class="title is-1 has-text-centered">PROJECT: <copy :text="currentProject.project.name"/></h1>
      <p class="has-text-centered">
        <b>ID:</b> <code>{{currentProject.project.id}}</code>;
        <b>User:</b> <code><username :userID="currentProject.project.user_id"/></code>;
      </p>

      <div>
        <br><br>
        <h2 class="title is-2 has-text-centered">COMMAND JOBS</h2>
        <b-table :data="currentProject.project_command_jobs">
          <template slot-scope="props">
            <b-table-column field="id" label="ID">{{props.row.id}}</b-table-column>
            <b-table-column field="add_date" label="Added"><timesince :time="props.row.add_date" /></b-table-column>
            <b-table-column field="propagated" label="Propagated">
              <timesince v-if="props.row.propagated" :time="props.row.propagation_date" />
              <span v-if="!props.row.propagated">NO</span>
            </b-table-column>
            <b-table-column field="cmd" label="Command"><code>{{props.row.cmd}}</code></b-table-column>
            <b-table-column field="actions" label="Actions">
              <a @click="viewJob(props.row.id)" class="button is-small">View responses</a>
            </b-table-column>
          </template>
        </b-table>
        <div class="custom-modal" :active.sync="openJobModal">
          <b-loading :active.sync="isSelectedJobLoading"></b-loading>
          <div v-if="!isSelectedJobLoading" class="container">
            <br><br>
            <h3 class="title is-3 has-text-centered">JOB DETAILS</h3>
            <div class="has-text-centered"><a @click="openJobModal=false" class="button">Close</a></div>
            <p><b>ADDED:</b> <timesince :time="selectedJob.project_command_job.add_date" /></p>
            <p><b>PROPAGATED:</b> <timesince :time="selectedJob.project_command_job.propagation_date" /></p>
            <p><b>COMMAND:</b> <code>{{selectedJob.project_command_job.cmd}}</code></p>
            <div v-for="nodeCommand in selectedJob.node_commands" :key="nodeCommand.id">
              <h4 class="title is-4 has-text-centered"><nodename :nodeID="nodeCommand.id" /></h4>
              <p><b>ADDED:</b> <timesince :time="nodeCommand.add_date" /></p>
              <p><b>STATUS:</b> {{nodeCommand.status}}</p>
              <br>
              <pre v-html="nodeCommand.response" />
              <hr>
            </div>
          </div>
        </div>
      </div>

      <div>
        <br><br>
        <h2 class="title is-2 has-text-centered">HOSTED ON</h2>
        <nodestable :nodes="currentProject.nodes" :areNodesLoading="false" />
      </div>

    </div>
  </section>  
</template>

<style lang="scss" scoped>
.custom-modal {
  display: none;
}
.custom-modal[active]{
  display: unset;
  position: fixed;
  top: 0; left: 0; bottom: 0; right: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  background-color: white;
  overflow: scroll;
}
</style>

<script>
import {HTTP} from '../services/http'

export default {
  data () {
    return {
      currentProject: {},
      isProjectLoading: true,
      openJobModal: false,
      selectedJob: null,
      isSelectedJobLoading: true
    }
  },

  mounted () {
    // get project
    this.isProjectLoading = true
    HTTP.get('/admin/projects/' + this.$route.params.id)
    .then(response => {
      this.currentProject = response.data
      this.isProjectLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  },

  computed: {
    isLoading () {
      return this.isProjectLoading
    }
  },

  methods: {
    viewJob (jobID) {
      this.openJobModal = true
      this.isSelectedJobLoading = true
      HTTP.get('/admin/projects/' + this.$route.params.id + '/jobs/' + jobID)
      .then(response => {
        this.selectedJob = response.data
        this.isSelectedJobLoading = false
      })
      .catch(e => {
        console.log(e)
      })
    }
  }
  
}
</script>
