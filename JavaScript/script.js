const content = document.querySelector('#content')


const additem = (event) => {
    fetch('http://127.0.0.1:8000/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Origin': '*',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        content.innerHTML = `<p>${data.Hello}</p>`
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

additem()