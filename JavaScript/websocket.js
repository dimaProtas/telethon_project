const errorDiv = document.querySelector('#errorDiv')

const ws = new WebSocket("ws://127.0.0.1:8000/ws");

        ws.onopen = () => {
            console.log("WebSocket connected");
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);

            if (data.status === "success") {
                // Обработка успешной авторизации
                console.log("Authorization success");
                console.log(data.user);
                localStorage.setItem("user_id", data.user.id)
                // register_user(data.user.id, data.user.username)
                window.location.href = "file:///home/dima_protasevich/Documents/FastAPI/telethon_project/templates/index.html";
            } else if (data.status === "error") {
                const errorMes = document.createElement('p')
                errorMes.style.color = 'red'
                const errorText = document.createTextNode('QR-code устарел, обновите страницу!')

                errorMes.appendChild(errorText)
                errorDiv.appendChild(errorMes)
                // Обработка ошибки авторизации
                console.error("Authorization error:", data.error);
            } else {
                // Обработка данных QR-кода (в данном случае выводим QR-код на страницу)
                const qrCodeImg = document.createElement('img');
                qrCodeImg.setAttribute('src', data.qr_code_url);
                document.getElementById('qrCode').appendChild(qrCodeImg);
            }
        };

        ws.onclose = (event) => {
            console.log("WebSocket closed:", event);
        };

        ws.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };



// const register_user = (user_id, username) => {
//     fetch('http://127.0.0.1:8000/auth/register', {
//         method: "POST",
//         headers: {
//             'Content-Type': 'application/json',
//             'Accept': 'application/json',
//         },
//         body: JSON.stringify({
//             "email": `${user_id}@email.ru`,
//             "password": "1234",
//             "is_active": true,
//             "is_superuser": false,
//             "is_verified": false,
//             "username": username
//           })
//     })
//     .then(responce => {
//         if(!responce.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         return responce.json()
//     })
//     .then(data => {
//         console.log(data)
//     })
//     .catch(error => {
//         console.error(`Error: ${error}`);
//     });
// }

