const crearBtn = document.getElementById("Crear")
const verBtn = document.getElementById("Ver")
const editarBtn = document.getElementById("Editar")
const eliminarBtn = document.getElementById("Eliminar")

crearBtn.addEventListener("click", () => { window.location.href = "/crear_receta.html"})
verBtn.addEventListener("click", () => { window.location.href = "/ver_receta.html"})
editarBtn.addEventListener("click", () =>{ window.location.href = "/editar_receta.html"})
eliminarBtn.addEventListener("click", () =>{ window.location.href = "/eliminar_receta.html"})