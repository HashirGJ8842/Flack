document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', () => {
    if(document.querySelector('#message-button'))
    {
    document.querySelector('#message-button').onclick = () => {

        console.log('TEST')
        var x = new Date();
        const hours = x.getHours();
        const minutes = x.getMinutes();
        const seconds = x.getSeconds();
        const time = `${hours}: ${minutes}: ${seconds}`
        const month = x.getMonth()+1;
        const year = x.getFullYear();
        const date = x.getDate();
        const time_stamp = `${date}/${month}/${year}, ${time}`
        socket.emit('store message', {'message': `${time_stamp} || ${document.querySelector('#name').innerHTML} -->> ${document.querySelector('#message').value}`, 'channel': document.querySelector('#heading').innerHTML})
    };
    }
    });
    socket.on('display message', data => {
        const li = document.createElement('li')
        li.innerHTML = data.message
        document.querySelector('#message-channel-content').append(li)
    })
});