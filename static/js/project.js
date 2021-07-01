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
    const pw = getElementById('pw')
    const pwconfirm = getElementById('pwconfirm')

    if (pw.value.length >= 8 && pwconfirm.value.length >= 8) {
        $('#passwordHelpBack').css('color', 'green');
        // document.getElementById('passwordHelpBlock').style.color = 'green';   
    } else {
        document.getElementById('passwordHelpBlock').style.color = 'red';  
    }
}
