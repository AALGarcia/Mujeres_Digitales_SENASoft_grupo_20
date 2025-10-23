
    const form = document.getElementById('usuarioForm');
    const alerta = document.getElementById('alerta');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());

      try {
        // Enviar a un endpoint (ajustar ruta cuando exista backend)
        // const res = await fetch('/api/usuarios', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        // const json = await res.json();

        console.log('Datos del usuario:', data);
        alerta.className = 'alert alert-success';
        alerta.textContent = 'Usuario preparado para guardar (pendiente integración backend).';
        alerta.classList.remove('d-none');
      } catch (err) {
        alerta.className = 'alert alert-danger';
        alerta.textContent = 'Error al procesar el usuario.';
        alerta.classList.remove('d-none');
      }
    });
