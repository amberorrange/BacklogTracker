"use strict";


// Toggles password visibility(elements identified by the class "password")
function togglePasswordVisibilty() {
    const x = document.querySelectorAll(".password");
    for (const element of x) {
        if (element.type === "password") {
            element.type = "text";
        } else {
            element.type = "password";
        }
    }
}


//Reminds user of password requirements
function passwordRequirements() {
    const pw = document.getElementById('pw')
    const pwconfirm = document.getElementById('pwconfirm')
    const length = document.getElementById('charLength')
    const match = document.getElementById('pwMatch')

    console.log(pw.value, pwconfirm.value)
    

    if (pw.value.length >= 8 && pw.value.length <= 20 && pwconfirm.value.length >= 8 && pwconfirm.value.length <= 20) {
        length.style.color = 'green';
    } else {
        length.style.color = 'red';
    }

    if (pw.value != pwconfirm.value) {
        match.style.color = 'red'
    } else{
        match.style.color = 'green'
    }  
}

