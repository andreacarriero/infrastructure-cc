<template>
  <div>
    <div class="custom-modal" :active.sync="showCommandModal">
      <b-loading :active.sync="isSelectedCommandLoading"></b-loading>
      <div v-if="selectedCommand" class="container" style="background-color: white;">
        <br><br>
        <h3 class="title is-3 has-text-centered">COMMAND DETAILS</h3>
        <div class="has-text-centered"><a class="button" @click="showCommandModal = false">Close</a></div>
        <p><b>ADDED:</b> <timesince :time="selectedCommand.project_command_job.add_date" /></p>
        <p><b>PROPAGATED: </b><timesince :time="selectedCommand.project_command_job.propagation_date" /></p>
        <br><br>
        <table class="table is-bordered is-fullwidth">
          <tbody>
            <tr>
              <th>COMMAND</th>
              <td><code>{{selectedCommand.project_command_job.cmd}}</code></td>
            </tr>
            <tr>
              <th>STATUS</th>
              <td>{{selectedCommand.command.status}}</td>
            </tr>
            <tr>
              <th>RESPONSE</th>
              <td><pre v-html="selectedCommand.command.response" /></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-table :data="commands" :loading="areCommandsLoading">
      <template slot-scope="props">
        <b-table-column field="id" label="ID">
          {{props.row.id}}
        </b-table-column>

        <b-table-column field="add_date" label="Added">
          <timesince :time="props.row.add_date" />
        </b-table-column>

        <b-table-column field="status" label="Status">
          {{props.row.status}}
        </b-table-column>

        <b-table-column field="actions" label="Actions">
          <a @click="expand(props.row.id)" class="button is-small">Expand</a>
        </b-table-column>
      </template>
    </b-table>
  </div>
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
  name: 'commandstable',
  props: ['commands', 'areCommandsLoading'],

  data () {
    return {
      selectedCommandID: null,
      selectedCommand: null,
      isSelectedCommandLoading: true,
      showCommandModal: false
    }
  },

  methods: {
    expand (commandID) {
      this.isSelectedCommandLoading = true
      this.showCommandModal = true
      HTTP.get('/admin/nodes/0/commands/' + commandID)
      .then(response => {
        this.selectedCommand = response.data
        this.isSelectedCommandLoading = false
      })
      .catch(e => {
        console.log(e)
      })
    }
  }
}
</script>
