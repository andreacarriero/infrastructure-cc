<template>
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
        <a class="button is-small">Expand</a>
      </b-table-column>
    </template>
  </b-table>
</template>

<script>
export default {
  name: 'commandstable',
  props: ['commands', 'areCommandsLoading']
}
</script>
