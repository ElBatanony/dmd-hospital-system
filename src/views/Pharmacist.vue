<template>
  <v-container
    fluid
    grid-list-lg
  >
    <v-layout row wrap>
      <v-flex xs12>
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
            item-key="id"
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
              <td hidden key="id">{{ props.item.id }}</td>
              <td>{{ props.item.name }}</td>
              <td>{{ props.item.quantity }}</td>
              <td>{{ props.item.expDate }}</td>
            </template>

            <template v-slot:footer>
              <td :colspan="headers.length">
                <v-btn 
                  color="error" 
                  :disabled="drugsAreChosen" 
                  @click="deleteSelectedMedicines()"
                >Delete Selected</v-btn>
              </td>
            </template>
          </v-data-table>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-card>
          <v-card-title>
            <v-toolbar-title>Add medicine</v-toolbar-title>
          </v-card-title>

          <v-container>
            <v-form ref="drugInfo">
              <v-text-field
                name="drugName"
                v-model="drugName"
                label="Name"
                required
              ></v-text-field>

              <v-layout row wrap>
                <v-flex>
                  <v-text-field
                    name="drugQuantity"
                    v-model="drugQuantity"
                    label="Quantity"
                    type="number"
                    required
                  ></v-text-field>
                </v-flex>

                <v-flex>
                  <v-text-field
                    name="drugExpDate"
                    v-model="drugExpDate"
                    label="Expiration date"
                    mask="date"
                    placeholder="dd/mm/yyyy"
                    required
                  ></v-text-field>
                </v-flex>
              </v-layout>

              <v-btn 
                color="success" 
                :disabled="!formIsValid" 
                @click="addMedicine()"
              >submit</v-btn>
            </v-form>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
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
      },
      addMedicine() {
        var expDate = this.drugExpDate,
            expDateFormatted = expDate.substring(0, 2) + '/' + expDate.substring(2, 4) + '/' + expDate.substring(4, 8);
        
        const response = db.collection("medicines").add({
          name: this.drugName,
          quantity: this.drugQuantity,
          expDate: expDateFormatted
        });

        response.then(function(data) {
          db.collection("medicines").doc(data.id).update({
            id: data.id
          });
        });

        this.$refs.drugInfo.reset()
      },
    },
    computed: {
      drugsAreChosen: function() {
        return !(this.selected.length > 0);
      },
      formIsValid: function() {
        return this.drugName != "" 
            && this.drugQuantity != null 
            && this.drugExpDate.length == 8;
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
        ],
        drugName: "",
        drugQuantity: null,
        drugExpDate: ""
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