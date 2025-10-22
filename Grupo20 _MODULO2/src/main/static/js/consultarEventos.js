// Controlador para consultar eventos
document.addEventListener('DOMContentLoaded', function() {
    // Cargar eventos al iniciar la página
    cargarEventos();
    
    // Configurar el botón de búsqueda
    document.getElementById('searchBtn').addEventListener('click', filtrarEventos);
    
    // Configurar búsqueda en tiempo real
    document.getElementById('searchTerm').addEventListener('input', filtrarEventos);
    document.getElementById('searchDate').addEventListener('change', filtrarEventos);
});

// URL base para las peticiones a la API
const API_URL = '/api/eventos';

// Almacenamiento de eventos para filtrado local
let todosLosEventos = [];

// Función para cargar todos los eventos
function cargarEventos() {
    // Mostrar indicador de carga
    document.getElementById('loadingEvents').classList.remove('d-none');
    document.getElementById('noEventsMessage').classList.add('d-none');
    
    fetch(API_URL)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        // Guardar todos los eventos para filtrado local
        todosLosEventos = data;
        
        // Ocultar indicador de carga
        document.getElementById('loadingEvents').classList.add('d-none');
        
        // Mostrar eventos
        mostrarEventos(data);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loadingEvents').classList.add('d-none');
        document.getElementById('eventosContainer').innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    Error al cargar eventos: ${error.message}
                </div>
            </div>
        `;
    });
}

// Función para mostrar eventos en tarjetas
function mostrarEventos(eventos) {
    const container = document.getElementById('eventosContainer');
    container.innerHTML = '';
    
    // Si no hay eventos, mostrar mensaje
    if (eventos.length === 0) {
        document.getElementById('noEventsMessage').classList.remove('d-none');
        return;
    } else {
        document.getElementById('noEventsMessage').classList.add('d-none');
    }
    
    // Crear tarjetas para cada evento
    eventos.forEach(evento => {
        // Formatear fecha para mostrar
        const fecha = new Date(evento.fecha_evento).toLocaleDateString();
        
        // Crear elemento de tarjeta
        const card = document.createElement('div');
        card.className = 'col-md-4';
        card.innerHTML = `
            <div class="card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span class="event-date">
                        <i class="bi bi-calendar-event"></i> ${fecha}
                    </span>
                    <span class="badge bg-primary">
                        ${evento.hora_inicio} - ${evento.hora_fin}
                    </span>
                </div>
                <div class="card-body">
                    <h5 class="card-title">${evento.nombre}</h5>
                    <p class="card-text">${evento.descripcion.substring(0, 100)}${evento.descripcion.length > 100 ? '...' : ''}</p>
                </div>
                <div class="card-footer text-end">
                    <button class="btn btn-sm btn-outline-primary ver-detalle" data-id="${evento.id}">
                        <i class="bi bi-eye"></i> Ver detalles
                    </button>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
    
    // Agregar event listeners a los botones de ver detalle
    document.querySelectorAll('.ver-detalle').forEach(btn => {
        btn.addEventListener('click', () => verDetalleEvento(btn.getAttribute('data-id')));
    });
}

// Función para filtrar eventos
function filtrarEventos() {
    const searchTerm = document.getElementById('searchTerm').value.toLowerCase();
    const searchDate = document.getElementById('searchDate').value;
    
    // Filtrar eventos según los criterios
    const eventosFiltrados = todosLosEventos.filter(evento => {
        // Filtrar por término de búsqueda
        const coincideTermino = searchTerm === '' || 
            evento.nombre.toLowerCase().includes(searchTerm) || 
            evento.descripcion.toLowerCase().includes(searchTerm);
        
        // Filtrar por fecha
        const coincideFecha = searchDate === '' || evento.fecha_evento === searchDate;
        
        // Devolver true si coincide con ambos criterios
        return coincideTermino && coincideFecha;
    });
    
    // Mostrar eventos filtrados
    mostrarEventos(eventosFiltrados);
}

// Función para ver detalle de un evento
function verDetalleEvento(id) {
    // Buscar el evento en el array local
    const evento = todosLosEventos.find(e => e.id == id);
    
    if (evento) {
        // Formatear fecha para mostrar
        const fecha = new Date(evento.fecha_evento).toLocaleDateString();
        
        // Llenar el modal con los datos del evento
        document.getElementById('detalleCodigo').textContent = evento.codigo;
        document.getElementById('detalleNombre').textContent = evento.nombre;
        document.getElementById('detalleFecha').textContent = fecha;
        document.getElementById('detalleHoraInicio').textContent = evento.hora_inicio;
        document.getElementById('detalleHoraFin').textContent = evento.hora_fin;
        document.getElementById('detalleDescripcion').textContent = evento.descripcion;
        
        // Mostrar el modal
        const modal = new bootstrap.Modal(document.getElementById('eventoDetalleModal'));
        modal.show();
    } else {
        console.error('Evento no encontrado');
    }
}