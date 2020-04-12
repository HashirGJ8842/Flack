document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', () => {
    console.log("Hello")
    document.querySelector('#new').onclick = () => {
            const channel = document.querySelector('.new-channel-name').value
        document.querySelectorAll('.channell').forEach(button => {
            if(button.innerHTML == channel)
            {
                socket.emit('channel select', {'channel': channel})
            }
        })
        socket.emit('new channel', {'channel': channel})
    };
    document.querySelectorAll('.channell').forEach(button => {
        button.onclick = () => {
        const channel = button.innerHTML;
        socket.emit('channel select', {'channel': channel});
        };
        });
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
        socket.emit('store message', {'message': `${time_stamp} || ${document.querySelector('#name').innerHTML} -->> ${document.querySelector('#message').value}`, 'channel': document})
    };
    });
    socket.on('show channel', data => {
        const h1 = document.createElement('h1');
        h1.innerHTML = data.name;
        h1.classList.add('heading-channel');
        if(document.querySelector('.heading-channel'))
        {
            console.log('came inside if')
            document.querySelector('#messages-channel-name').replaceChild(h1, document.querySelector('.heading-channel'))
        }
        else
        {
            console.log('came inside else')
            document.querySelector('#messages-channel-name').append(h1);
        }
        console.log(data.message)
    });
    socket.on('display message', data => {

        console.log('TEST')
        const li = document.createElement('li')
        li.innerHTML = data.message
        document.querySelector('#message-channel-content').append(li)
    })
    socket.on('create channel', data => {
        if(data.new)
        {
            const li = document.createElement('li');
            const button = document.createElement('button')
            button.innerHTML = data.name
            button.classList.add('channell')
            li.append(button);
            document.querySelector('#total-channels').append(li);
        }
    })
});