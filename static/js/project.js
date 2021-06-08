"use strict";



// Toggles password visibility(identified by the class "password")
function myFunction() {
    const x = document.querySelectorAll(".password");
    for (const element of x) {
        if (element.type === "password") {
            element.type = "text";
        } else {
            element.type = "password";
        }
    }
}


// $('#delete_account').on('click', (evt) => {
//     evt.preventDefault();
//     alert('Are you sure you you want to delete your account? This change is permanent.');

// })



const delete_account = document.querySelector('delete_account');

delete_account.addEventListener('click', (evt) => {
    alert('Warning.');
    evt.preventDefault();
