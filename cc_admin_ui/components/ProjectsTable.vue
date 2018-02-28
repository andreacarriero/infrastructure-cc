<template>
  <b-table
    :data="projects"
    :loading="areProjectsLoading">

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

    <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p><b>No projects to display.</b></p>
          </div>
        </section>
      </template>
  </b-table>
</template>

<script>
export default {
  name: 'projectstable',
  props: ['projects', 'areProjectsLoading']
}
</script>
