google.charts.load("current", { packages: ["scatter"] });

let readLimit = 1000;

var chartOptions = {
  width: 1200,
  height: 600,
  chart: {
    title: "Geospatial Search",
    subtitle: "based on doctors' salaries vs. number of patients per doctor"
  },
  hAxis: {
    title: "Salary of doctor"
  },
  vAxis: {
    title: "Number of patients"
  }
};

var config = {
  apiKey: "AIzaSyDNBtZl3FDTc-SaYhoGJxKInT2VfwyR4jc",
  authDomain: "sampledata-89242.firebaseapp.com",
  databaseURL: "https://sampledata-89242.firebaseio.com",
  projectId: "sampledata-89242",
  storageBucket: "sampledata-89242.appspot.com",
  messagingSenderId: "795547228220"
};
firebase.initializeApp(config);

var db = firebase.firestore();

let mydata = [];
var doctors = {};

let testing = false;

function fetchData() {
  let start = new Date().getTime();
  if (testing) {
    for (let i = 0; i < 400; i++) {
      let salary = getRandomInt(1200, 3600) * 10;
      let patients = getRandomInt(0, 10);
      doctors[i] = {
        name: i,
        salary,
        patients
      };
      mydata.push([salary, patients]);
    }
    google.charts.setOnLoadCallback(drawChart);
  }

  if (!testing) {
    db.collection("employees").where("role", "==", "doctor").limit(readLimit).get().then(function(querySnapshot) {
        querySnapshot.forEach(function(doc) {
          doctors[doc.id] = {
            salary: doc.data().salary,
            patients: 0,
            name: doc.data().name
          };
        });

        db.collection("records").where("status", "==", "approved").limit(readLimit).get().then(function(querySnapshot) {
          querySnapshot.forEach(function(doc) {
            let doctorId = doc.data().doctor.path.split("/")[1];
            if (!doctors[doctorId]) {
              doctors[doctorId] = { salary: 12000, patients: 0, name: doctorId };
              console.log("missing doctor");
            }
            doctors[doctorId].patients += 1;
          });
          for (let doctor in doctors) {
            mydata.push([doctors[doctor].salary, doctors[doctor].patients]);
          }
          app.readTime = new Date().getTime() - start;
          drawChart();
        })
        .catch(function(error) {
          console.log("Error getting documents: ", error);
        });
      })
      .catch(function(error) {
        console.log("Error getting documents: ", error);
      });
  }
  
}

function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "Salary of doctor");
  data.addColumn("number", "Number of patients");

  data.addRows(mydata);

  var chart = new google.charts.Scatter(
    document.getElementById("scatterchart_material")
  );

  chart.draw(data, google.charts.Scatter.convertOptions(chartOptions));
}

function calculateDistance(s1, p1, s2, p2) {
  s1 /= 1000; s2 /= 1000;
  return Math.sqrt((s1 - s2) * (s1 - s2) + (p1 - p2) * (p1 - p2));
}

function runGeospatial() {
  let ret = [];
  for (let doctorId in doctors) {
    if ( calculateDistance(app.salary, app.patients, doctors[doctorId].salary, doctors[doctorId].patients) < app.searchDist ) {
      ret.push( {
        name : doctors[doctorId].name,
        salary : doctors[doctorId].salary,
        patients: doctors[doctorId].patients,
        id : doctorId
      } )
    }
  }
  app.searchResults = ret;
  app.resultsDialog = true;
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}
