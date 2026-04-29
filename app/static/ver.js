document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("token");
  const lista = document.getElementById("listaRecetas");

  try {
    const response = await fetch("/receta", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await response.json();

    if (response.ok) {
      lista.innerHTML = "";

      data.receta.forEach(r => {
  const li = document.createElement("li");


  li.innerHTML = `
    <strong>ID: ${r.id}</strong><br>
    <strong>${r.nombre}</strong><br>
    <em>Ingredientes:</em> ${r.ingredientes}<br>
    <em>Preparación:</em> ${r.preparacion}`;

  lista.appendChild(li);
});
    } else {
      lista.innerHTML = `<li>Error: ${data.message}</li>`;
    }
  } catch (error) {
    console.error("Error al obtener recetas:", error);
    lista.innerHTML = "<li>Error de conexión</li>";
  }
});

const btnHome = document.getElementById("btnHome");

btnHome.addEventListener("click", () => {
  window.location.href = "/home"; // ajusta la ruta según tu Flask
});