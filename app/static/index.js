//datos del register
const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

//datos del login
const email_l = document.getElementById("email_l")
const password_l = document.getElementById("password_l")


const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
loginBtn.addEventListener("click", login);
registerBtn.addEventListener("click", register);


async function login() {
  const email = email_l.value;       
  const password = password_l.value; 

  try {
    const response = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (data.token) {
      // Guardamos el token en localStorage
      localStorage.setItem("token", data.token);
      alert("Login exitoso");

      email_l.value = "";
      password_l.value = "";

      window.location.href = "/home";
    } 
    
    else {
      alert("Error: " + data.mensaje);
    }
  } 
  
  catch (err) {
    console.error("Error en login:", err);
    alert("Hubo un problema con el servidor");
  }
}


async function register() {
  const username = usernameInput.value;
  const email = emailInput.value;
  const password = passwordInput.value;

  try {
    const response = await fetch("http://localhost:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (data.mensaje === "Usuario creado") {
      alert("Registro exitoso, ahora puedes iniciar sesión");
      usernameInput.value = ""
      emailInput.value = ""
      passwordInput.value = ""
      

    } 
    else {
      alert("Error: " + data.mensaje);
    }
  } 
  catch (err) {
    console.error("Error en registro:", err);
    alert("Hubo un problema con el servidor");
  }
}
