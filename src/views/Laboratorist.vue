<template>
  <div id="laboratorist">
    <v-tabs color="blue" dark slider-color="yellow">
        <v-tab ripple>Reports</v-tab>
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
            <v-data-table :headers="headers" :items="reports" :search="search">
            <template v-slot:items="props">
                <td>{{ props.item.laboratorist }}</td>
                <td>{{ props.item.requester }}</td>
                <td>{{ props.item.patient }}</td>
                <td>{{ props.item.testType }}</td>
                <td>{{ props.item.testResult }}</td>
                <td>
                <v-btn round dark ripple v-bind:to="{name: 'Edit Report', params: {report_id: props.item.report_id}}">edit</v-btn>
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
    </v-tabs>
<!--    <v-card-text style="height: 100px; position: relative">-->
<!--        <v-fab-transition>-->
<!--            <v-btn to="/new_report"-->
<!--                color="pink"-->
<!--                dark-->
<!--                absolute-->
<!--                bottom-->
<!--                right-->
<!--                fab-->
<!--            >-->
<!--                <v-icon>add</v-icon>-->
<!--            </v-btn>-->
<!--        </v-fab-transition>-->
<!--    </v-card-text>-->
  </div>
</template>

<script>
import firebase from 'firebase'
var db = firebase.firestore()

export default {
  data() {
    return {
      search: "",
      headers: [
        {
            text: "Laboratorist",
            align: "left",
            sortable: true,
            value: "laboratorist"
        },
        {
            text: "Requester",
            value: "requester"
        },
        {
            text: "Patient",
            value: "patient"
        },
        { 
            text: "Test Type",
            value: "testType"
        },
        {
            text: "Test Result",
            value: "testResult"
        },
        { 
            text: "Edit Info", 
            value: "edit" 
        }
      ],
      reports: [],
    };
  },
    created () {
        db.collection('reports').limit(5).get().then(querySnapshot => {
            querySnapshot.forEach(doc => {
                let data = {
                    'report_id': doc.id,
                    'patient': '',
                    'testResult': doc.data().testResult,
                    'testType': doc.data().testType,
                    'laboratorist': '',
                    'requester': '',
                }
                doc.data().laboratorist.get()
                    .then(res => {
                        data["laboratorist"] = res.data().name
                        doc.data().patient.get()
                        .then(res => {
                            data["patient"] = res.data().name
                            doc.data().requester.get()
                                .then(res => {
                                    data['requester'] = res.data().name
                                    this.reports.push(data)
                                })
                        })
                    })                 
                
            })
        })
    }
};
</script>

<style>
</style>