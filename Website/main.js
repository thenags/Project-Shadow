/*
POTENTIAL BUGS: If 2 people order at the EXACT SAME SECOND the "complete" button will
complete BOTH buttons.
*/

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
import { getDatabase, ref, onValue, child, get, push, update, set } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-auth.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCW-xXgbVvsRSNgPPlCsBv19g-tltwhdAE",
    authDomain: "schooltracking-40411.firebaseapp.com",
    databaseURL: "https://schooltracking-40411-default-rtdb.firebaseio.com",
    projectId: "schooltracking-40411",
    storageBucket: "schooltracking-40411.appspot.com",
    messagingSenderId: "857799116203",
    appId: "1:857799116203:web:afa76806c021dc2a73beee",
    measurementId: "G-QTSMFZLYEQ"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
// Initialize Realtime Database and get a reference to the service
const db = getDatabase(app);

$("#signin").click(function() {
    const auth = getAuth();
    signInWithEmailAndPassword(auth,$("#floatingInput").val(), $("#floatingPassword").val())
    .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;
        console.log("Success");
        location.href = 'tracking.html?email=' + $("#floatingInput").val() + '&pass=' + $("#floatingPassword").val();
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorMessage);
        $("#signinheader").text("Permission Denied");
    });
});

/*var id = 224289;
const dbRef = ref(getDatabase());
get(child(dbRef, `students/224289`)).then((snapshot) => {
    if (snapshot.exists()) {
      console.log(snapshot.val());
    } else {
      console.log("No data available");
    }
  }).catch((error) => {
    console.error(error);
  });*/