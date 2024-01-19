const profile = document.querySelector('#profile')


const add_profile = (event) => {
    fetch('http://127.0.0.1:8000/profile/', {
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
        profile.innerHTML = `<p>id: ${data.id}</p>\n<p>Username: ${data.username}</p>\n<p>First Name: ${data.first_name}</p>\n<p>Phone: ${data.phone}</p>`
        localStorage.setItem("user_id", data.id)
        console.log(data)
    })
    .catch(error => {
        console.log(`Erorr ${error}`)
    })
}

add_profile()