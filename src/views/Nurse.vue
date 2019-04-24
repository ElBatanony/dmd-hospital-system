<template>
  <div>
  <v-tabs color="blue" dark slider-color="yellow">
    <v-tab ripple>Rooms</v-tab>
    <v-tab ripple>Free Rooms</v-tab>
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
            <td>{{ props.item.roomNumber }}</td>
            <td>{{ props.item.roomType }}</td>
            <td>{{ props.item.patientId }}</td>
            <td>{{ props.item.patientName }}</td>
            <td>
              <v-btn v-on:click="remove(props.item.roomNumber)" round dark ripple>free</v-btn>
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
          Room allocation
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers3" :items="rooms2" :search="search3">
          <template v-slot:items="props">
            <td>{{ props.item.roomNumber }}</td>
            <td>{{ props.item.roomType }}</td>
            <!-- <td>{{ props.item.patientId }}</td> -->
            <!-- <td>{{ props.item.patientName }}</td> -->
            <td>
              <v-btn v-on:click="openRoomDialog(props.item.roomNumber)" round dark ripple>Allocate</v-btn>
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
            Diagnostic Reports
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
                <td>{{ props.item.laboratorist }}</td>
                <td>{{ props.item.patient }}</td>
                <td>{{ props.item.testType }}</td>
                <td>{{ props.item.testResult }}</td>
                <!-- <td>
                <v-btn round dark ripple v-bind:to="{name: 'Edit Report', params: {report_id: props.item.report_id}}">edit</v-btn>
                </td> -->
            </template>
            <v-alert
                v-slot:no-results
                :value="true"
                color="error"
                icon="warning"
            >Your search for "{{ search }}" found no results.</v-alert>
            </v-data-table>
            
        </v-card>
        <v-card-text style="height: 100px; position: relative">
        <v-fab-transition>
            <v-btn to="/new_report"
                color="pink"
                dark
                absolute
                bottom
                right
                fab
            >
                <v-icon>add</v-icon>
            </v-btn>
          </v-fab-transition>
          </v-card-text>
        </v-tab-item>
    

    <v-dialog
      v-model="roomDialog"
      persistent
      max-width="600px"
      v-if="freeRoom"
    >
      <v-card>
        <v-card-title>
          <span class="headline">RoomAllocation ID: {{freeRoom.roomNumber}}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              
              <v-flex xs12 sm6>
                <v-autocomplete
                  v-model="freeRoom.patient"
                  :items="freeRoomsList"
                  label="Patient ID*"
                ></v-autocomplete>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="roomDialog = false"
            >Close</v-btn
          >
          <v-btn color="blue darken-1" flat v-on:click="allocate">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


  </v-tabs>
  
  </div>
</template>

<script>
import firebase from 'firebase'

var db = firebase.firestore()
var nurse = this
var newT = this
var pName = ''
var names = []

var adjust = function(){
  nurse.rooms2 = []
  nurse.rooms = []
  db.collection('rooms').where("nurse", "==", firebase.auth().currentUser.uid).where("free", "==", false).limit(10)
      .get().then(querySnapshot => {
        querySnapshot.forEach(doc2 => {
          
          var data = {
                'roomNumber': doc2.data().roomNumber,
                'roomType': doc2.data().roomType,
                'patientId': '',
                'patientName': ''
          }

          var pQuery = db.collection('room_assignment').get().then(querySnapshot => {
            querySnapshot.forEach(doc => {
              if(doc.data()){
                if(doc.data().room){
                  if(doc.data().room.id == doc2.id){
                    data.patientId = doc.data().patient.id;
                    db.collection('patients').doc(doc.data().patient.id).onSnapshot(doc2 =>{
                    
                      if(doc2.data()){
                        data.patientName = doc2.data().name
                      }else{
                        data.patientName = 'undefined'
                      }

                    })
                  }
                }else{
                  data.patientId = 'undefined';
                  data.patientName = 'undefined';
                }
              }else{
                data.patientId = 'undefined';
                data.patientName = 'undefined';
              }
            })
          })
          
          nurse.rooms.push(data)
        })
        
      });
      db.collection('rooms')
        .where("free", "==", true)
          .where("nurse", "==", db.collection('employees').doc(firebase.auth().currentUser.uid))
            .limit(10)
            .get()
              .then(querySnapshot => {
                  querySnapshot.forEach(doc2 => {
                    var data = {
                      'roomNumber': doc2.data().roomNumber,
                      'roomType': doc2.data().roomType,
                    }
                    nurse.rooms2.push(data)
                  })
        
              });
      
}

export default {
  data() {
    return {
      remove: function(id) {
        var deleteID = 0;
        db.collection('rooms').get().then(querySnapshot => {
          querySnapshot.forEach(doc => {
              if(doc.data().roomNumber === id){
                deleteID = doc.id
                db.collection('rooms').doc(deleteID).update({
                  free: true,
                  patient: null
                })
                adjust();                
                
              }
          })
        })
        
      },
      allocate: function() {
        
        nurse.roomDialog = false;
        nurse.freeRoom.free = false;
          
        
        

      },
      openRoomDialog: function(roomNumber) {
        db.collection('patients').get().then(snapshot =>{
          snapshot.forEach(doc =>{
            nurse.freeRoomsList.push(doc.id)
          })
        })
        nurse.freeRoom = nurse.rooms2.filter(x => x.roomNumber == roomNumber)[0];
        nurse.roomDialog = true;
      },
      roomDialog: false,
      search: "",
      freeRoomsList: [],
      headers: [
        {
          text: "Room Number",
          align: "left",
          sortable: true,
          value: "roomNumber"
        },
        { text: "Type of room", value: "roomType" },
        {
          text: "Patient ID",
          value: "patientId"
        },
        {text: "Patient Name", value: "patientName"},
        { text: "Edit Info", value: "edit" }
      ],
      freeRoom: null,
      temp: null,
      rooms: [],
      search2: "",
      headers2: [
        {
            text: "Laboratorist",
            align: "left",
            sortable: true,
            value: "laboratorist"
        },
        {
            text: "Patient",
            value: "patient"
        },
        { 
            text: "Test Type",
            value: "testT" 
        },
        {
            text: "Test Result",
            value: "testR"
        },
       
      ],
      headers3: [
        {
          text: "Room Number",
          align: "left",
          sortable: true,
          value: "roomNumber"
        },
        { text: "Type of room", value: "roomType" },
        { 
            text: "Edit Info", 
            value: "edit" 
        }
      ],
      rooms2: [],
      search3: "",
      reports: [],
    };
  },
  created () {
    nurse = this
    firebase.auth().onAuthStateChanged(function(user) {
      if(user){
      console.log(nurse.$route.name)
      adjust();

      db.collection('reports').limit(10).get().then(querySnapshot => {
            querySnapshot.forEach(doc => {
                let data = {
                    'report_id': doc.id,
                    'patient': '',
                    'testResult': doc.data().testResult,
                    'testType': doc.data().testType,     
                    'laboratorist': '',
                    // 'requester': db.collection('employees').doc(firebase.auth().currentUser.uid)
                }
                if(doc.data().laboratorist){
                doc.data().laboratorist.get()
                    .then(res => {
                        console.log(res.data())
                        data["laboratorist"] = res.data().name
                        doc.data().patient.get()
                        .then(res => {
                            data["patient"] = res.data().name
                            nurse.reports.push(data)
                        })
                    })                 
                }else{
                  data.laboratorist = 'undefined'
                  if(doc.data().patient){
                    doc.data().patient.get().then(snapshot => {
                      data.patient = snapshot.data().name;
                    })
                    nurse.reports.push(data)
                  }else{
                    data.patient = 'undefined'
                    nurse.reports.push(data)
                  }
                }
            })
        })
      
        }
    });
  },

  
};
</script>

<style>
</style>