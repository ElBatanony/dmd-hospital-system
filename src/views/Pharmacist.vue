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

              <td>
                <v-text-field
                  v-model="props.item.name"
                  :value="props.item.name"
                  required
                ></v-text-field>
              </td>

              <td>
                <v-layout row wrap justify-start align-center>
                  <v-flex xs2>
                    <v-btn
                      flat
                      icon
                      color="error"
                      @click="decrease(props.item.id, props.item.quantity)"
                    ><v-icon>remove</v-icon></v-btn>
                  </v-flex>

                  <v-flex xs3>
                    <v-text-field 
                      mask="######"
                      v-model="props.item.quantity"
                      :value="props.item.quantity"
                      required
                    ></v-text-field>
                  </v-flex>
                  
                  <v-flex xs2>
                    <v-btn
                      flat
                      icon
                      color="primary"
                      @click="increase(props.item.id, props.item.quantity)"
                    ><v-icon>add</v-icon></v-btn>
                  </v-flex>
                </v-layout>
              </td>

              <td>
                <v-text-field
                  mask="date"
                  v-model="props.item.expDate"
                  :value="props.item.expDate"
                  required
                  ></v-text-field>
              </td>
            </template>

            <template v-slot:footer>
              <td :colspan="headers.length">
                <v-btn 
                  color="error" 
                  :disabled="drugsAreChosen" 
                  @click="deleteSelected()"
                >Delete Selected</v-btn>

                <v-btn 
                  color="info"
                  :disabled="drugsAreChosen"
                  @click="updateSelected()"
                >Update Selected</v-btn>
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
                    mask="######"
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
      deleteSelected() {        
        for (let med of this.selected) {
          db.collection("medicines")
          .doc(med.id)
          .delete()
        }
      },
      updateSelected() { 
        for (let med of this.selected) {
          if (med.name != "" && med.expDate.length == 8) {
            db.collection("medicines").doc(med.id).update({
              name: med.name,
              quantity: med.quantity,
              expDate: med.expDate
            });
          }
        }

        this.selected = []
      },
      addMedicine() {
        const response = db.collection("medicines").add({
          name: this.drugName,
          quantity: Number(this.drugQuantity),
          expDate: this.drugExpDate
        });

        response.then(function(data) {
          db.collection("medicines").doc(data.id).update({
            id: data.id
          });
        });

        this.$refs.drugInfo.reset()
      },
      increase(docId, quantity) {
        db.collection("medicines").doc(docId).update({
          quantity: Number(quantity) + 1
        });
      },
      decrease(docId, quantity) {
        if (quantity > 0) {
          db.collection("medicines").doc(docId).update({
            quantity: Number(quantity) - 1
          });
        }
      }
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
