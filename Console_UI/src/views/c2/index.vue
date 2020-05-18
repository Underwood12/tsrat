<template>
  <div class="c2-container">
    <webconsole />
    <consolelog />
  </div>
</template>

<script>
import { Webconsole, Consolelog } from './components'
export default {
  name: 'C2',
  components: {
    Webconsole,
    Consolelog
  }
}
</script>
