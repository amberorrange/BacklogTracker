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


