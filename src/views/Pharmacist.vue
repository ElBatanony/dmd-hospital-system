<template>
    <v-card>
        <v-card-title>
          <v-toolbar-title> Medicine list </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>

        <v-data-table
          v-model="selected"
          :headers="headers"
          :items="medicines"
          :search="search"
          item-key="name"
          select-all
          class="elevation-1"
        >
          <template v-slot:items="props">
              <td>
                  <v-checkbox
                    v-model="props.selected"
                    primary
                    hide-details
                  ></v-checkbox>
              </td>
              <td hidden>{{ props.item.id }}</td>
              <td>{{ props.item.name }}</td>
              <td>{{ props.item.quantity }}</td>
              <td>{{ props.item.expDate }}</td>
          </template>

          <template v-slot:footer>
            <td :colspan="headers.length">
              <v-btn :disabled="disabled" color="error" v-on:click="deleteSelectedMedicines()">Delete Selected</v-btn>
            </td>
          </template>
        </v-data-table>
    </v-card>
</template>

<script>
  import firebase from 'firebase'

  var app, db

  export default {
    name: "Pharmacist",
    methods: {
      deleteSelectedMedicines() {        
        for (let med of this.selected) {
          db.collection("medicines")
          .doc(med.id.trim())
          .delete()
        }
      }
    },
    computed: {
      disabled: function() {
        return !(this.selected.length > 0);
      }
    },
    data() {
      return {
        search: "",
        selected: [],
        headers: [
          {text: "Name", value: "name"},
          {text: "Quantity", value: "quantity"},
          {text: "Expiration date", value: "expDate"}
        ],
        medicines: [
          { 
            id: "Loading...",
            name: "Loading...",
            quantity: "Loading...",
            expDate: "Loading..."
          }
        ]
      }
    },
    created() {
      db = firebase.firestore();

      app = this;

      db.collection("medicines").onSnapshot(function(querySnapshot) {
        app.medicines = [];

        querySnapshot.forEach(function(doc) {
          app.medicines.push(
            {
              id: doc.id,
              name: doc.name,
              quantity: doc.quantity,
              expDate: doc.expDate,
              ...doc.data()
            }
          );
        });
      });
    }
  }
</script>