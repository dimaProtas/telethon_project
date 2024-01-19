const inputEl = document.querySelector('input')
const content = document.querySelector('#content')


const wildebisRequest = () => {
    requestText = inputEl.value
    const encodedText = encodeURIComponent(requestText);
    fetch(`http://127.0.0.1:8000/wildberis/${encodedText}`, {
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
        inputEl.value = ''

        data.result.forEach(el => {
            const divEl = document.createElement('div')
            divEl.setAttribute('class', 'divEl')
            const elP = document.createElement('a')
            elP.setAttribute('href', el.link)
            const spanEl = document.createElement('span')
            const imgEl = document.createElement('img')
            imgEl.setAttribute('src', el.link_img)
            const textP = document.createTextNode(el.title)
            const textSpan = document.createTextNode(el.price)

            elP.appendChild(textP)
            spanEl.appendChild(textSpan)

            divEl.appendChild(elP)
            divEl.appendChild(spanEl)
            divEl.appendChild(imgEl)

            content.appendChild(divEl)
        })

    })
    .catch(error => {
        console.log(`Error: ${error}`)
    })
}