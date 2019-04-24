<template>
    <v-form
    ref="form"
    v-model="valid"
    lazy-validation
    >
        <v-select
        v-model="laboratorist"
        :items="laboratorists"
        :rules="[v => !!v || 'Laboratorist is required']"
        label="Laboratorist"
        required
        ></v-select>

        <v-select
        v-model="patient"
        label="Patient"
        readonly
        ></v-select>

        <v-select
        v-model="testType"
        label="Test Type"
        readonly
        ></v-select>

        <v-textarea
            v-model="testResult"
            auto-grow
            label="Test Result"
            rows="2"
        ></v-textarea>

        <v-btn @click="update" color="success">edit</v-btn>
        <v-btn @click="remove" color="error">delete</v-btn>
        <v-btn @click="back">back</v-btn>
    </v-form>  
</template>

<script>
import firebase from 'firebase'
var db = firebase.firestore()
export default {
  name: 'edit-employee',
  data () { 
        return {
            valid: true,
            report_id: '',
            laboratorist: '',
            patient: '',
            requester: '',
            laboratorists: [],
            testResult: '',
            testType: '',
        };
    },
  beforeRouteEnter (to, from, next) {
    db.collection('reports').doc(to.params.report_id).get().then(doc => {
        next(function(vm) {
            vm.report_id = doc.id
            doc.data().laboratorist.get().then(res => {
              vm.laboratorist = res.id
            })
            vm.laboratorists = []
            db.collection('employees').limit(20).where("role", "==", "Laboratorist")
            .get().then(querySnapshot => {
                querySnapshot.forEach(doc => {
                    let data = doc.id;
                    vm.laboratorists.push(data);
                })
            })
            vm.testResult = doc.data().testResult
            vm.testType = doc.data().testType
            vm.patient = doc.data().patient.id
            vm.requester = doc.data().requester.id
      })
      })
  },
  methods: {
    update () {
      db.collection('reports').doc(this.report_id).update({
            testResult: this.testResult,
            // date:
          })
          .then(() => {
            this.$router.push('/laboratorist')
          });
    },
    remove() {
      if (confirm("Are you sure?")) {
        db.collection('reports').doc(this.report_id).delete();
        this.$router.push('/laboratorist');
      }
    },
    back () {
      this.$router.push('/laboratorist');
    }
  }
}
</script>