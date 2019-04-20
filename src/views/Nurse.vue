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
            <!-- <td>{{ props.item.patientName }}</td> -->
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
var nurse = this
var newT = this
var pName = ''
var names = []

export default {
  data() {
    return {
      remove: function(id) {
        var deleteID = 0;
        db.collection('rooms').get().then(querySnapshot => {
          querySnapshot.forEach(doc => {
              if(doc.data().roomID === id){
                deleteID = doc.id
                db.collection('rooms').doc(deleteID).update({
                  free: true
                })
                nurse.rooms = nurse.rooms.filter(value => value.roomID == id)
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
        // {text: "Patient Name", value: "patientName"},
        { text: "Edit Info", value: "edit" }
      ],
    
      rooms: [],
      search2: "",
      headers2: [
        { text: "Test Type", value: "testT" },
        { text: "Test Result", value: "testR" },
        { text: "Laboratorist", value: "laboratorist" },
        { text: "Patient", value: "patient" }
      ],
      reports: [],
    };
  },
  created () {
    nurse = this
    firebase.auth().onAuthStateChanged(function(user) {
      if(user){
      console.log(nurse.$route.name)
      db.collection('rooms').where("nurse", "==", firebase.auth().currentUser.uid).where("free", "==", false)
      .get().then(querySnapshot => {
        querySnapshot.forEach(doc2 => {
          
          var names = []
          console.log(doc2.data().patient)
          var pName = db.collection('patients').where("PID", "==", doc2.data().patient).get().then(querySnapshot2 =>{
            querySnapshot2.forEach(doc3 =>{
              
              names.name = doc3.data().name;
              console.log("doc3.name=", doc3.data().name)
              
              
            })
            
          })
          
          console.log(pName)
          const data = {
                'roomId': doc2.data().roomID,
                'roomType': doc2.data().roomType,
                'patientId': doc2.data().patient,
             
          }
          nurse.rooms.push(data)
        })
      });

      names = []
      names.push(1)
      console.log(names)
      console.log(names[0])
      
      
      db.collection('reports').get().then(querySnapshot =>{
        querySnapshot.forEach(doc => {
          
          const data = {
            'laboratorist': doc.data().laboratorist.id,
            'patient': doc.data().patient,
            'testT': doc.data().testT,
            'testR': doc.data().testR
          
          }
          nurse.reports.push(data)
        })
      }) 
      }
    });
  },

  
};
</script>

<style>
</style>