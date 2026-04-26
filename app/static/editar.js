const form = document.getElementById("formEditarReceta");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("token");
  const id = document.getElementById("id").value;
  const nombre = document.getElementById("nombre").value;
  const ingredientes = document.getElementById("ingredientes").value;
  const preparacion = document.getElementById("preparacion").value;

  try {
    const response = await fetch(`/receta/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        nombre: nombre,
        ingredientes: ingredientes,
        preparacion: preparacion
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert("Receta actualizada con éxito!");
      console.log("Backend respondió:", data);
      form.reset();
    } else {
      alert("Error: " + data.message);
    }
  } catch (error) {
    console.error("Error al actualizar receta:", error);
    alert("Error de conexión");
  }
});

const btnHome = document.getElementById("btnHome");
btnHome.addEventListener("click", () => {
  window.location.href = "/home";
});
