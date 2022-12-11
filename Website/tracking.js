/*
-----------------------------------TO DO-----------------------------------
| 1) Mobile Support |
-----------------------------------TO DO-----------------------------------
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
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars;
}
const auth = getAuth();
var displayLevel = "student";
var uuid = "";
var teacherStudents = [];
signInWithEmailAndPassword(auth, getUrlVars()["email"], getUrlVars()["pass"])
    .then((userCredential) => {
        // Signed in 
        const user = userCredential.user;
        uuid = user.uid;
        console.log(uuid);
        console.log("Authenticed");
        if (getUrlVars()["email"].includes("student")) {
            console.log("student");
            displayLevel = "student";
        } else if (getUrlVars()["email"].includes("teacher")) {
            console.log("teacher");
            displayLevel = "teacher";
        } else if (getUrlVars()["email"].includes("admin")) {
            console.log("admin");
            displayLevel = "admin";
            $("#settingsBtn").hide();
        }
        if(displayLevel == "teacher"){
            $("#lockout").hide();
            $("#lockdown").hide();
        }
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorMessage);
    });

window.onload = function () {
    //GLOBAL
    var canvas = document.querySelector("#game_canvas");
    var context = canvas.getContext("2d");
    var markers = [];
    //CONSTANT
    var FRAME_RATE = 1000 / 60; //60 fps
    var offset = [0, 0];
    var zoom = 1.0;
    var mousePos = [0, 0];
    var background = new Image();
    var selectedID = 0;
    var scrollWheel = 0;
    var danger = 0;
    var emergencyStatus = 0;
    var averageAccuracy = 0;
    var online = 0;
    var offline = 0;
    var period = 0;
    var oldStudentData;
    // Make sure the image is loaded first otherwise nothing will draw.
    background.onload = function () {
        
        drawZoomedImage()
    }
    canvas.addEventListener('wheel', function (event) {
        scrollWheel += event.deltaY;
        zoom = 1.0 + scrollWheel / 1000;
        if (zoom > 3) {
            zoom = 3;
        } else if (zoom < 1.0) {
            zoom = 1.0;
            scrollWheel = 0;
        }
        updateDrag();
        drawZoomedImage();
        for (var i = 0; i < markers.length; i++) {
            drawCircle(context, markers[i][0], markers[i][1], markers[i][2] * zoom, '', markers[i][4], 3);
            drawCircle(context, markers[i][0], markers[i][1], 1, '', markers[i][4], 2);
        }
        return false;
    }, false);

    var setup = (function () {
        const db = getDatabase();
        const studentRef = ref(db, 'students');
        const settingsRef = ref(db, 'settings');
        const teachersRef = ref(db, 'teachers');
        console.log();
        $(".card-title").css("font-size", (window.innerWidth / 1920 * 80).toString() + "px");
        $(".card-body").css("font-size", (window.innerWidth / 1920 * 30).toString() + "px");
        $("#game_canvas").width(window.innerWidth * 0.5052).height(window.innerHeight * 0.73);
        /*
        SETTINGS:
        0 - EMERGENCY STATE
        1 - STUDENTS IN DANGER
        2 - PERIOD
        */
        onValue(studentRef, (snapshot) => {
            const data = snapshot.val();
            updateStudents(data);
        });
        onValue(teachersRef, (snapshot) => {
            get(child(studentRef,uuid)).then((snapshot) => {
                if (snapshot.exists()) {
                    updateStudents(snapshot.val());
                } else {
                  console.log("No data available");
                }
              }).catch((error) => {
                console.error(error);
              });
            
        });
        onValue(settingsRef, (snapshot) => {
            if (snapshot.exists()) {
                oldStudentData = snapshot.val();
                //$("#settings").hide();
                emergencyStatus = snapshot.val()[0];
                if(period == 0){
                    period = snapshot.val()[2];
                }
                if(snapshot.val()[2] != period){
                    location.reload();
                }
                
                
                //danger = snapshot.val()[1];
                //$("#danger").text(danger);
                if(emergencyStatus == 0){
                    background.src = "gchs.png";
                }else if(emergencyStatus == 1){
                    background.src = "lockout.png";
                }else{
                    background.src = "lockin.png";
                        }
                console.log(emergencyStatus);
                if (emergencyStatus != 0) {
                    $("body").css("background-color", "red");
                    if (emergencyStatus == 1) {
                        $("#lockout").text("END LOCKOUT")
                    } else {
                        $("#lockdown").text("END LOCKDOWN")
                    }
                }
            } else {
                console.log("No data available");
            }
        });
        $("#settings").hide();
    })();

    function draw(e) {
        // getStudentData();
        if(danger == 0){
            $("#danger").css("color","green");
        }else{
            $("#danger").css("color","red");
            
        }
        $("#danger").text(danger);
        $("#online").text(online);
        if(online == 0){
            $("#online").css("color","red");
        }else{
            $("#online").css("color","green");
        }
        $("#offline").text(offline);
        if(offline == 0){
            $("#offline").css("color","green");
        }else{
            $("#offline").css("color","red");
        }
        if(selectedID == 0){
            $("#selected").text("Select A Name");
        }else{
            $("#selected").text(selectedID);
        }
    }
    function declareEmergency(situation) {
        //0 - no situation
        //1 - lock out
        //2 - lock down
        const db = getDatabase();
        update(ref(db, 'settings/'), {
            "0": situation
        });
        emergencyStatus = situation;
    }
    function movedMouse(e) {

        drawZoomedImage()
        var pos = getMousePos(canvas, e);
        if (mouseIsDown) {
            offset = [offset[0] + (pos.x - mousePos[0]), offset[1] + (pos.y - mousePos[1])];
        }
        mousePos = [pos.x, pos.y];
        averageAccuracy = 0.0;
        var isSelected = false;
        for (var i = 0; i < markers.length; i++) {
            drawCircle(context, markers[i][0], markers[i][1], markers[i][2] * zoom, '', markers[i][4], 3);
            drawCircle(context, markers[i][0], markers[i][1], 1, '', markers[i][4], 2);
            averageAccuracy += markers[i][2] / 4.658;
            
            let cirX = markers[i][0] * zoom + offset[0] - (canvas.width / 2 * (zoom - 1));
            let cirY = markers[i][1] * zoom + offset[1] - (canvas.height / 2 * (zoom - 1));
            if (dist(pos.x, pos.y, cirX, cirY) < 5) {
                context.font = (20 * zoom).toString() + 'px arial';
                context.fillStyle = "#0000ff"
                selectedID = markers[i][6];
                isSelected = true;
                context.strokeText(markers[i][3], cirX - context.measureText(markers[i][2]).width / 2 - 10, cirY - 10 * zoom);
                context.fillStyle = "#ffffff"
                context.fillText(markers[i][3], cirX - context.measureText(markers[i][2]).width / 2 - 10, cirY - 10 * zoom);
            }
        }
        if(!isSelected){
            selectedID = 0;
        }
        averageAccuracy /= markers.length;
        $("#accuracy").text(Math.round(averageAccuracy * 100) / 100);
        $("#accuracy").text( $("#accuracy").text() + "m");
    }
    window.addEventListener('mousemove', movedMouse, false);
    function dist(x1, y1, x2, y2) {
        var deltaX = x1 - x2;
        var deltaY = y1 - y2;
        var dist = Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));
        return (dist);
    };

    function getMousePos(canvas, evt) {
        var rect = canvas.getBoundingClientRect();
        return {
            x: (evt.clientX - rect.left) / (rect.right - rect.left) * canvas.width,
            y: (evt.clientY - rect.top) / (rect.bottom - rect.top) * canvas.height
        };
    }
    var mouseIsDown = false;

    function updateDrag() {

    }
    canvas.onmousedown = function (e) {
        mouseIsDown = true;
    }
    canvas.onmouseup = function (e) {
        mouseIsDown = false;
    }
    function updateStudents(data) {
        const db = getDatabase();
        const teacherRef = ref(db, 'teachers');
        oldStudentData = data;
        markers = [];
        drawZoomedImage();
        offline = 0;
        online = 0;
        danger = 0;
        if(displayLevel != "teacher"){
            jQuery.each(data, function (i, val) {
                var color = 'blue';
                var currTime = Date.now() / 1000;
                var diff = currTime - val["position"][3];
                if(diff / 60 > 20){
                    offline += 1;
                    color = 'gray';
                }else{
                    online += 1;
                } 
                if(val["details"][0]){
                    danger += 1;
                    if(color != 'gray'){
                        color = 'red';
                    }
                }
                console.log(color);
                markers.push([val["position"][0], val["position"][1], val["position"][2], i, color, val["details"][0], val["details"][1]]);
            });
        }else{
            get(child(teacherRef,uuid)).then((snapshot) => {
                if (snapshot.exists()) {
                  teacherStudents = snapshot.val()["students"][period - 1];
                  console.log(period);
                  updateSettings(data, teacherStudents);
                    jQuery.each(data, function (i, val) {
                        if(teacherStudents.includes(parseInt(i))){
                            var color = 'blue';
                            var currTime = Date.now() / 1000;
                            var diff = currTime - val["position"][3];
                            if(diff / 60 > 20){
                                offline += 1;
                                color = 'gray';
                            }else{
                                online += 1;
                            } 
                            if(val["details"][0]){
                                danger += 1;
                            }
                            markers.push([val["position"][0], val["position"][1], val["position"][2], i, color, val["details"][0], val["details"][1]]);
                        }
                    });
                } else {
                  console.log("No data available");
                }
              }).catch((error) => {
                console.error(error);
              });
        }
        
    }
    //auth.uid === 'FVzufH0WzsRcoLsbGvNB1Z9OmwG2'
    function updateSettings(data, exclusions){
        var table = document.getElementById("settingsTable");
        var count = 0;
        var items = document.getElementsByClassName("item");
        console.log(data);
        while(items[0]) {
            items[0].parentNode.removeChild(items[0]);
        }
        jQuery.each(data, function (i, val) {
            if(exclusions.includes(parseInt(i))){
                var row = document.createElement("tr");
                row.className = "item";
                var name = document.createElement("td");
                name.innerHTML = val["details"][1];
                var id = document.createElement("td");
                id.innerHTML = i;
                var remove = document.createElement("button");
                remove.className = "btn btn-danger";
                remove.innerHTML = "Remove";
                remove.id = count;
                remove.onclick = function() { removeFunc(); };
                row.appendChild(name);
                row.appendChild(id);
                row.appendChild(remove);
                table.appendChild(row);
                count += 1;
            }
        });
        
    }
    function addFunc(){
        //
        if($("#addID").val() != ""){
            const teachersRef = ref(db, 'teachers');
        get(child(teachersRef,uuid)).then((snapshot) => {
            if (snapshot.exists()) {
                let students = snapshot.val()["students"];
                let num = event.target.id;
                let students2 = teacherStudents;
                students2.push(parseInt($("#addID").val()));;
                students[period - 1] = students2;
                set(ref(db, 'teachers/' + uuid), {
                    students
                });
                location.reload();
            } else {
                console.log("No data available");
            }
            }).catch((error) => {
            console.error(error);
            });
            
        }
    }
    function removeFunc(){
        const teachersRef = ref(db, 'teachers');
        get(child(teachersRef,uuid)).then((snapshot) => {
            if (snapshot.exists()) {
                let students = snapshot.val()["students"];
                let num = event.target.id;
                let students2 = teacherStudents;
                students2.pop(num);
                students[period - 1] = students2;
                set(ref(db, 'teachers/' + uuid), {
                    students
                });
                location.reload();
            } else {
                console.log("No data available");
            }
            }).catch((error) => {
            console.error(error);
            });
        
    }
    function drawZoomedImage() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(background, offset[0] - (canvas.width / 2 * (zoom - 1)), offset[1] - (canvas.height / 2 * (zoom - 1)), (canvas.width * zoom), (canvas.height * zoom));
        
    }
    function drawCircle(ctx, x, y, radius, fill, stroke, strokeWidth) {
        ctx.beginPath()
        ctx.arc(x * zoom + offset[0] - (canvas.width / 2 * (zoom - 1)), y * zoom + offset[1] - (canvas.height / 2 * (zoom - 1)), radius, 0, 2 * Math.PI, false)
        if (fill) {
            ctx.fillStyle = fill
            ctx.fill()
        }
        if (stroke) {
            ctx.lineWidth = strokeWidth
            ctx.strokeStyle = stroke
            ctx.stroke()
        }
    }
    var draw_interval = setInterval(draw, FRAME_RATE);
    $("#lockout").click(function () {
        if(emergencyStatus != 0){
            declareEmergency(0);
        }else{
            declareEmergency(1);
        }
        location.reload()
    });
    $("#lockdown").click(function () {
        if(emergencyStatus != 0){
            declareEmergency(0);
        }else{
            declareEmergency(2);
        }
        location.reload()
    });
    $("#logout").click(function () {
        
        location = "/index.html"
    });
    $("#settingsBtn").click(function () {
        $("#dashboard").toggle();
        $("#settings").toggle();
    });
    $("#homeBtn").click(function () {
        $("#dashboard").show();
        $("#settings").hide();
    });
    $("#addNewStudent").click(function () {
        addFunc();
    });
};

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