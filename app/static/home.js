const crearBtn = document.getElementById("Crear")
const verBtn = document.getElementById("Ver")
const editarBtn = document.getElementById("Editar")
const eliminarBtn = document.getElementById("Eliminar")

crearBtn.addEventListener("click", () => { window.location.href = "/crear"})
verBtn.addEventListener("click", () => { window.location.href = "/ver"})
editarBtn.addEventListener("click", () =>{ window.location.href = "/editar"})
eliminarBtn.addEventListener("click", () =>{ window.location.href = "/eliminar"})


const token = localStorage.getItem("token");
if (token) {
  try {
    // Decodificar el payload del JWT (sin librerías externas)
    const payloadBase64 = token.split('.')[1];
    const payload = JSON.parse(atob(payloadBase64));

   
    const titulo = document.getElementById("titulo_Home");
    titulo.textContent = `Welcome ${payload.user_id}`;

  } catch (error) {
    console.error("Error leyendo el token:", error);
  }
}