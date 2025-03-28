// Configuración básica para actualizaciones en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const socket = io();

    socket.on('biometric_update', function(data) {
        if (data.athlete_id === "{{ current_user.id }}") {
            document.getElementById('current-hr').textContent = data.heart_rate + ' BPM';
        }
    });
});