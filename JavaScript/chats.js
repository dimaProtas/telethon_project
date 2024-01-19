const chats = document.querySelector('#chats')
const messages = document.querySelector('#mesages')
let current_user = localStorage.getItem("user_id")
const divSendMessage = document.querySelector('#divSendMessage')


const chatsAdd = () => {
    fetch('http://127.0.0.1:8000/dialogs/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Origin': '*',
        }
    })
    .then(responce => {
        if (!responce.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return responce.json()
    })
    .then(data => {
        // console.log(data)
        data.forEach(el => {
            const linkChat = document.createElement('p')
            linkChat.setAttribute('class', 'chats')
            linkChat.setAttribute('id', el.hash_id)
            linkChat.onclick = getMessages
            const textChat = el.dialogs_name ? document.createTextNode(el.dialogs_name) : document.createTextNode(el.hash_id)
            linkChat.appendChild(textChat)

            chats.appendChild(linkChat)
        });
    })
    .catch(erorr => {
        console.log(`Erorr: ${erorr}`)
    })
}

const getMessages = (event) => {
    if (messages.firstChild) {
        while (messages.querySelector('p')) {
            messages.removeChild(messages.querySelector('p'));
        }
    }

    const inputMessage = document.querySelector("#inputMessage")
    inputMessage.setAttribute('hash', event.target.id)

    let absoluteValue = Math.abs(Number(event.target.id));

    fetch(`http://127.0.0.1:8000/get_messages/${absoluteValue}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Origin': '*',
        }
    })
    .then(responce => {
        if (!responce.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return responce.json()
    })
    .then(data => {
        console.log(data)

        data.reverse().forEach(el => {
            const elP = document.createElement('p')
            if (el.from_id) {
                elP.setAttribute('class', 'me')
            } else {
                elP.setAttribute('class', 'message')
            }
            const textEl = document.createTextNode(el.text)
    
            elP.appendChild(textEl)
    
            messages.insertBefore(elP, divSendMessage)
        })

    })
}

const sendMessage = () => {
    const inputMessage = document.querySelector('#inputMessage')
    const hash = inputMessage.getAttribute('hash')

    if (inputMessage.value.length !== 0 && hash) {
        fetch('http://127.0.0.1:8000/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                "hash": Number(hash),
                "message": inputMessage.value
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // console.log(data);
            if (data.status === "ok") {
                const elementP = document.createElement('p')
                const textP = document.createTextNode(inputMessage.value)
                elementP.setAttribute('class', 'me')
                elementP.appendChild(textP)
    
                messages.insertBefore(elementP, divSendMessage)

                inputMessage.value = ""
            }
        })
        .catch(error => {
            console.error(`Error: ${error}`);
        });
    } else {
        alert('Выберите чат, и заполните поле для отправки сообщения!')
    }


}

chatsAdd()
