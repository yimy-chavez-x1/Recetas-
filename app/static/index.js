// Capturar elementos del HTML
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const loginBtn = document.getElementById("loginBtn");

// Escuchar el click en el botón
loginBtn.addEventListener("click", login);

// Función principal de login
function login() {
  const email = emailInput.value;       // lo que el usuario escribió en el campo email
  const password = passwordInput.value; // lo que el usuario escribió en el campo password

  // Llamada al backend con fetch
  fetch("http://localhost:5000/login", {
    method: "POST", 
    headers: {
      "Content-Type": "application/json" // le decimos al backend que mandamos JSON
    },
    body: JSON.stringify({ email, password }) // convertimos el objeto JS en texto JSON
  })
  .then(res => res.json()) // convertimos la respuesta en JSON
  .then(data => {
    if (data.token) {
      // Si el backend devolvió un token, lo guardamos
      localStorage.setItem("token", data.token);
      alert("Login exitoso");
    } else {
      // Si no hay token, mostramos el mensaje de error
      alert("Error: " + data.mensaje);
    }
  })
  .catch(err => {
    // Si algo falla (servidor caído, error de red, etc.)
    console.error("Error:", err);
    alert("Hubo un problema con el servidor");
  });
}