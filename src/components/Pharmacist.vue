<template>
  <v-container>
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
          :items="drugs"
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
              <td>{{ props.item.name }}</td>
              <td>{{ props.item.quantity }}</td>
              <td>{{ props.item.expDate }}</td>
          </template>

          <template v-slot:footer>
            <td :colspan="headers.length">
              <!-- <v-btn color="error">Delete</v-btn> -->
            </td>
          </template>
        </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Pharmacist",
  methods: {
    
  },
  computed: {
    
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
      drugs: [
        {
          name: "Maxicold",
          quantity: 10,
          expDate: "11/09/19"
        },
        {
          name: "Antigrippin",
          quantity: 3,
          expDate: "12/09/18"
        }
      ]
    }
  }
}
</script>