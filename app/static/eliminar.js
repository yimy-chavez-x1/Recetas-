const form = document.getElementById("formEliminarReceta");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("token");
  const id = document.getElementById("id").value;

  try {
    const response = await fetch(`/receta/${id}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await response.json();

    if (response.ok) {
      alert("Receta eliminada con éxito!");
      console.log("Backend respondió:", data);
      form.reset();
    } else {
      alert("Error: " + data.message);
    }
  } catch (error) {
    console.error("Error al eliminar receta:", error);
    alert("Error de conexión");
  }
});

const btnHome = document.getElementById("btnHome");
btnHome.addEventListener("click", () => {
  window.location.href = "/home";
})