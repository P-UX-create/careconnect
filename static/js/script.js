console.log("CareConnect Loaded");

function searchPatients(){

let input=document.getElementById("searchPatient");

let filter=input.value.toUpperCase();

let table=document.getElementById("patientTable");

let tr=table.getElementsByTagName("tr");

for(let i=1;i<tr.length;i++){

let td=tr[i].getElementsByTagName("td")[1];

if(td){

let txt=td.textContent||td.innerText;

tr[i].style.display=txt.toUpperCase().indexOf(filter)>-1?"":"none";

}

}

}


function searchDoctors(){

let input=document.getElementById("searchDoctor");

let filter=input.value.toUpperCase();

let table=document.getElementById("doctorTable");

let tr=table.getElementsByTagName("tr");

for(let i=1;i<tr.length;i++){

let td=tr[i].getElementsByTagName("td")[1];

if(td){

let txt=td.textContent||td.innerText;

tr[i].style.display=
txt.toUpperCase().indexOf(filter)>-1?"":"none";

}

}

}


function searchAppointments(){

let input=document.getElementById("searchAppointment");

let filter=input.value.toUpperCase();

let table=document.getElementById("appointmentTable");

let tr=table.getElementsByTagName("tr");

for(let i=1;i<tr.length;i++){

let patient=tr[i].getElementsByTagName("td")[1];

let doctor=tr[i].getElementsByTagName("td")[2];

if(patient&&doctor){

let text=(patient.textContent+" "+doctor.textContent).toUpperCase();

tr[i].style.display=text.indexOf(filter)>-1?"":"none";

}

}

}