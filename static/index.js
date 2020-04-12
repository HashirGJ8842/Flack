document.addEventListener('DOMContentLoaded', () => {
// Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
    console.log("Hello")
    document.querySelector('#new').onclick = () => {
    console.log('Hiiii')
        const new_channel = document.querySelector('.new-channel-name').value;
        socket.emit('new channel', {'channel': new_channel})
    };
    document.querySelectorAll('.channell').forEach(button => {
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