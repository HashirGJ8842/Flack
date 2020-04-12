document.addEventListener('DOMContentLoaded', () => {
// Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
// When connected, configure buttons
    socket.on('connect', () => {
    console.log("Hello")
// Each button should emit a "submit vote" event
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
        const channel = button.dataset.channel;
        console.log('HI')
        socket.emit('channel select', {'channel': channel});
        };
    });
});
// When a new vote is announced, add to the unordered list
    socket.on('show channel', data => {
        console.log("Returned")
        const p = document.createElement('p');
        p.innerHTML = `Vote recorded: ${data.name}`;
        document.querySelector('#messages-section').append(p);
    });
});