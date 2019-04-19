<template>
  <v-tabs color="blue" dark slider-color="yellow">
    <v-tab ripple>Rooms</v-tab>
    <v-tab ripple>Reports</v-tab>
    <v-tab-item>
      <v-card flat>
        <v-card-title>
          Rooms allocation
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="rooms" :search="search">
          <template v-slot:items="props">
            <td>{{ props.item.roomId }}</td>
            <!-- <td class="text-xs-right">{{ props.item.roomId }}</td> -->
            <td>{{ props.item.bedId }}</td>
            <td>{{ props.item.patientId }}</td>
            <td>{{ props.item.pName }}</td>
            <!-- <td>{{ props.item.protein }}</td> -->
            <td>
              <v-btn round dark ripple>delete</v-btn>
            </td>
          </template>
          <v-alert
            v-slot:no-results
            :value="true"
            color="error"
            icon="warning"
          >Your search for "{{ search }}" found no results.</v-alert>
        </v-data-table>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat>
        <v-card-text>Contents for Item 2 go here</v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import firebase from 'firebase'
//import firebaseConfig from './firebaseConfig'

//const firebaseApp = firebase.initializeApp(firebaseConfig)

//export default firebaseApp.firestore() 
//import db from "./firebaseinit";

var db = firebase.firestore()

export default {
  data() {
    return {
      // callback: function(){
      // },
      search: "",
      headers: [
        {
          text: "Room ID",
          align: "left",
          sortable: true,
          value: "roomId"
        },
        { text: "Bed ID", value: "bedId" },
        {
          text: "Patient ID",
          value: "patientId"
        },
        { text: "Patient Name", value: "pName" },
        { text: "Edit Info", value: "edit" }
      ],
      rooms: [
        // {
        //   roomId: 1,
        //   bedId: 1,
        //   patientId: 1,
        //   pName: "John Doe",
        //   protein: 4.0
        // },
        // {
        //   roomId: 1,
        //   bedId: 1,
        //   patientId: 1,
        //   pName: "John Doe",
        //   protein: 4.0
        // },
        // {
        //   roomId: 1,
        //   bedId: 1,
        //   patientId: 1,
        //   pName: "John Doe",
        //   protein: 4.0
        // },
        // {
        //   roomId: 1,
        //   bedId: 1,
        //   patientId: 1,
        //   pName: "John Doe",
        //   protein: 4.0
        // }
      ],
    };
  },
  created () {
      console.log(this.$route.name)
      db.collection('rooms').get().then(querySnapshot => {
          querySnapshot.forEach(doc => {
              console.log(doc.data())
              const data = {
                //   'roomId': doc.data().roomId,
                'roomId': doc.data().roomID,
                'bedId': doc.data().roomID,
                'patientId': "1",
                'pName': "John Doe",
                // 'protein': doc.data().patient
                
              }
              this.rooms.push(data)
          })
      })
  }
};
</script>

<style>
</style>