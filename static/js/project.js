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