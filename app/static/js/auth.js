// static/js/auth.js

import { auth } from "./firebase-config.js";
import { createUserWithEmailAndPassword, updateProfile, signInWithEmailAndPassword } 
  from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// Signup Function
window.signup = async function () {
  const firstName = document.getElementById("first_name").value;
  const lastName = document.getElementById("last_name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorMessage = document.getElementById("error-message");

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    await updateProfile(user, { displayName: `${firstName} ${lastName}` });

    const idToken = await user.getIdToken();
    console.log("Generated Firebase ID Token:", idToken); 
    
    const response = await fetch("/verify_login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idToken, first_name: firstName, last_name: lastName })
    });

    const data = await response.json();
    if (data.success) {
      window.location.href = "/dashboard";
    } else {
      throw new Error("Sign-up verification failed!");
    }
  } catch (error) {
    console.error("Sign-up error:", error);
    errorMessage.innerText = error.message;
  }
};

// Login Function
window.login = async function () {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  const errorMessage = document.getElementById("login-error-message");

  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const idToken = await userCredential.user.getIdToken();

    const response = await fetch("/verify_login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken })
      });
      
      const data = await response.json();
      console.log("Server Response:", data);  
    if (data.success) {
      window.location.href = "/dashboard";
    } else {
      errorMessage.innerText = "Login failed!";
    }
  } catch (error) {
    errorMessage.innerText = error.message;
  }
};

// Attach login function to form submit
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", (event) => {
      event.preventDefault();
      login();
    });
  }
});
