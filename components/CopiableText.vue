<template>
  <b-tooltip label="Click to copy">
    <span v-clipboard:copy="text">{{text}}</span>
  </b-tooltip>
</template>

<script>
export default {
  name: 'copy',
  props: ['text']
}
</script>

