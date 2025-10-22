// Controlador para la gestión de eventos
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar validación de formularios de Bootstrap
    initFormValidation();
    
    // Cargar eventos al iniciar la página
    cargarEventos();
    
    // Configurar listeners para los formularios
    document.getElementById('crearEventoForm').addEventListener('submit', crearEvento);
    document.getElementById('guardarEdicionBtn').addEventListener('click', guardarEdicionEvento);
    document.getElementById('confirmarEliminarBtn').addEventListener('click', eliminarEvento);
});

// URL base para las peticiones a la API
const API_URL = '/api/eventos';

// Inicializar validación de formularios
function initFormValidation() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Función para crear un nuevo evento
function crearEvento(event) {
    event.preventDefault();
    
    const form = document.getElementById('crearEventoForm');
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    // Obtener datos del formulario
    const formData = new FormData(form);
    const eventoData = {
        nombre: formData.get('nombre'),
        descripcion: formData.get('descripcion'),
        fecha_evento: formData.get('fechaEvento'),
        hora_inicio: formData.get('hora_inicio'),
        hora_fin: formData.get('hora_fin')
    };
    
    // Enviar datos al servidor
    fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(eventoData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        // Mostrar mensaje de éxito
        alert('Evento creado exitosamente');
        
        // Limpiar formulario
        form.reset();
        form.classList.remove('was-validated');
        
        // Recargar lista de eventos
        cargarEventos();
        
        // Cambiar a la pestaña de listar
        const listTab = new bootstrap.Tab(document.getElementById('listar-tab'));
        listTab.show();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al crear el evento: ' + error.message);
    });
}

// Función para cargar la lista de eventos
function cargarEventos() {
    fetch(API_URL)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        const tablaBody = document.getElementById('cuerpoTablaEventos');
        tablaBody.innerHTML = '';
        
        // Si no hay eventos, mostrar mensaje
        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="7" class="text-center">No hay eventos registrados</td>';
            tablaBody.appendChild(row);
            return;
        }
        
        // Mostrar eventos en la tabla
        data.forEach(evento => {
            const row = document.createElement('tr');
            
            // Formatear fecha y hora para mostrar
            const fecha = new Date(evento.fecha_evento).toLocaleDateString();
            
            row.innerHTML = `
                <td>${evento.codigo}</td>
                <td>${evento.nombre}</td>
                <td>${evento.descripcion.substring(0, 50)}${evento.descripcion.length > 50 ? '...' : ''}</td>
                <td>${fecha}</td>
                <td>${evento.hora_inicio}</td>
                <td>${evento.hora_fin}</td>
                <td>
                    <button class="btn btn-sm btn-primary editar-btn" data-id="${evento.id}">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-danger eliminar-btn" data-id="${evento.id}" data-nombre="${evento.nombre}">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            
            tablaBody.appendChild(row);
        });
        
        // Agregar event listeners a los botones de editar y eliminar
        document.querySelectorAll('.editar-btn').forEach(btn => {
            btn.addEventListener('click', () => abrirModalEditar(btn.getAttribute('data-id')));
        });
        
        document.querySelectorAll('.eliminar-btn').forEach(btn => {
            btn.addEventListener('click', () => abrirModalEliminar(
                btn.getAttribute('data-id'),
                btn.getAttribute('data-nombre')
            ));
        });
    })
    .catch(error => {
        console.error('Error:', error);
        const tablaBody = document.getElementById('cuerpoTablaEventos');
        tablaBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar eventos: ${error.message}</td></tr>`;
    });
}

// Función para abrir el modal de edición
function abrirModalEditar(id) {
    // Obtener datos del evento
    fetch(`${API_URL}?id=${id}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(evento => {
        // Llenar el formulario con los datos del evento
        document.getElementById('edit_id').value = evento.id;
        document.getElementById('edit_codigo').value = evento.codigo;
        document.getElementById('edit_nombre').value = evento.nombre;
        document.getElementById('edit_descripcion').value = evento.descripcion;
        document.getElementById('edit_fechaEvento').value = evento.fecha_evento;
        document.getElementById('edit_hora_inicio').value = evento.hora_inicio;
        document.getElementById('edit_hora_fin').value = evento.hora_fin;
        
        // Mostrar el modal
        const modal = new bootstrap.Modal(document.getElementById('editarEventoModal'));
        modal.show();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al cargar los datos del evento: ' + error.message);
    });
}

// Función para guardar los cambios de edición
function guardarEdicionEvento() {
    const form = document.getElementById('editarEventoForm');
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    // Obtener datos del formulario
    const id = document.getElementById('edit_id').value;
    const eventoData = {
        id: id,
        nombre: document.getElementById('edit_nombre').value,
        descripcion: document.getElementById('edit_descripcion').value,
        fecha_evento: document.getElementById('edit_fechaEvento').value,
        hora_inicio: document.getElementById('edit_hora_inicio').value,
        hora_fin: document.getElementById('edit_hora_fin').value
    };
    
    // Enviar datos al servidor
    fetch(API_URL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(eventoData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editarEventoModal'));
        modal.hide();
        
        // Mostrar mensaje de éxito
        alert('Evento actualizado exitosamente');
        
        // Recargar lista de eventos
        cargarEventos();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el evento: ' + error.message);
    });
}

// Función para abrir el modal de eliminación
function abrirModalEliminar(id, nombre) {
    document.getElementById('idEventoEliminar').value = id;
    document.getElementById('nombreEventoEliminar').textContent = nombre;
    
    const modal = new bootstrap.Modal(document.getElementById('eliminarEventoModal'));
    modal.show();
}

// Función para eliminar un evento
function eliminarEvento() {
    const id = document.getElementById('idEventoEliminar').value;
    
    fetch(`${API_URL}?id=${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        // Cerrar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('eliminarEventoModal'));
        modal.hide();
        
        // Mostrar mensaje de éxito
        alert('Evento eliminado exitosamente');
        
        // Recargar lista de eventos
        cargarEventos();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar el evento: ' + error.message);
    });
}