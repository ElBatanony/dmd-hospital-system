<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Hospital management system</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn flat v-on:click="switchComponent('HelloWorld')"> Hello world </v-btn>
        <v-btn flat v-on:click="switchComponent('Pharmacist')"> Pharmacist </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-content>
      <keep-alive>
        <component :is="current"></component>
      </keep-alive>
    </v-content>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld'
import Pharmacist from './components/Pharmacist'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Pharmacist
  },
  methods: {
    switchComponent(component) {
      this.current = component
    }
  },
  computed: {
    
  },
  data() {
    return {
      current: "HelloWorld"
    }
  }
}
</script>
