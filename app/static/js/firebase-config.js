// static/js/firebase-config.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDQKY7VKYFLAAG8ECgihmunVnjDMXwzm4k",
  authDomain: "dublin-bikes-bc821.firebaseapp.com",
  projectId: "dublin-bikes-bc821",
  storageBucket: "dublin-bikes-bc821.appspot.com",
  messagingSenderId: "1048274875760",
  appId: "1:1048274875760:web:440f4852fbc3467d240bb5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
