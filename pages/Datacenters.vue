<template>
  <div class="container">
    <h1 class="title is-1 has-text-centered">DATACENTERS</h1>

    <!-- start datacenters table -->
      <b-table
        :data="datacenters"
        :loading="areDatacentersLoading">

        <template slot-scope="props">
          <b-table-column field="id" label="ID">
            {{props.row.id}}
          </b-table-column>

          <b-table-column field="name" label="Name">
            {{props.row.name}}
          </b-table-column>

          <b-table-column field="location" label="Location">
            {{props.row.location}}
          </b-table-column>

          <b-table-column field="coordinates" label="Coordinates">
            <span v-if="props.row.latitude && props.row.longitude">
              {{props.row.latitude}}; {{props.row.longitude}}
            </span>
          </b-table-column>

          <b-table-column field="actions" label="Actions">
            <router-link :to="{name: 'datacenter', params: {id: props.row.id}}" class="button is-small">Open</router-link>
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
      datacenters: [],
      areDatacentersLoading: true
    }
  },

  mounted () {
    // get datacenters
    this.areDatacentersLoading = true
    HTTP.get('/datacenters/')
    .then(response => {
      this.datacenters = response.data
      this.areDatacentersLoading = false
    })
    .catch(e => {
      console.log(e)
    })
  }
}
</script>
