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
            <td>{{ props.item.roomType }}</td>
            <td>{{ props.item.patientId }}</td>
            <!-- <td>{{ props.item.pName }}</td> -->
            <td>
              <v-btn v-on:click="remove(props.item.roomId)" round dark ripple>free</v-btn>
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
        <v-card-title>
          Reports
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers2" :items="reports" :search="search2">
          <template v-slot:items="props">
            <td>{{ props.item.testT }}</td>
            <td>{{ props.item.testR }}</td>
            <td>{{ props.item.laboratorist }}</td>
            <td>{{ props.item.patient }}</td>
          </template>
          <v-alert
            v-slot:no-results
            :value="true"
            color="error"
            icon="warning"
          >Your search for "{{ search2 }}" found no results.</v-alert>
        </v-data-table>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import firebase from 'firebase'

var db = firebase.firestore()

export default {
  data() {
    return {
      remove: function(id) {
        var deleteID = 0;
        // console.log(db.collection('patients').doc('p1'))
        db.collection('rooms').get().then(querySnapshot => {
          querySnapshot.forEach(doc => {
              if(doc.data().roomID === id){
                deleteID = doc.id
                db.collection('rooms').doc(deleteID).delete()
              }
          })
        })
        
        
      },
      search: "",
      headers: [
        {
          text: "Room ID",
          align: "left",
          sortable: true,
          value: "roomId"
        },
        { text: "Type of room", value: "roomType" },
        {
          text: "Patient ID",
          value: "patientId"
        },
        // { text: "Patient Name", value: "pName" },
        { text: "Edit Info", value: "edit" }
      ],
    
      rooms: [],
    
      search2: "",
      headers2: [
        { text: "Test Type", value: "testT" },
        { text: "Test Type", value: "testR" },
        { text: "Laboratorist", value: "laboratorist" },
        { text: "Patient", value: "patient" }
      ],
      reports: [],
    };
  },
  created () {
      console.log(this.$route.name)
      console.log(db.collection('rooms').doc('1'))
      db.collection('rooms').get().then(querySnapshot => {
          querySnapshot.forEach(doc => {
              var pID = doc.data().patient.id
              const data = {
                'roomId': doc.data().roomID,
                'roomType': doc.data().roomType,
                'patientId': doc.data().patient.id,
                // 'pName': "John Doe" //doc.data().patient.get().data().name,
              }
              this.rooms.push(data)
          })
      })
      db.collection('reports').get().then(querySnapshot =>{
        querySnapshot.forEach(doc => {
          const data = {
            'laboratorist': doc.data().laboratorist.id,
            'patient': doc.data().patient.id,
            'testT': doc.data().testT,
            'testR': doc.data().testR
          
          }
          this.reports.push(data)
        })
      }) 
  }
};
</script>

<style>
</style>