const form = document.getElementById("formCrearReceta");

form.addEventListener("submit", async (e) => {
  e.preventDefault(); // evita que recargue la página

  const token = localStorage.getItem("token");


  const nombre = document.getElementById("nombre").value;
  const ingredientes = document.getElementById("ingredientes").value;
  const preparacion = document.getElementById("preparacion").value;

  try {
    const response = await fetch("/receta", {
      method: "POST",
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
      alert("Receta creada con éxito!");
      console.log("Backend respondió:", data);
      form.reset(); 
    } else {
      alert("Error: " + data.message);
    }
  } catch (error) {
    console.error("Error al crear receta:", error);
  }
});

const btnHome = document.getElementById("btnHome");

btnHome.addEventListener("click", () => {
  window.location.href = "/home"; 
});