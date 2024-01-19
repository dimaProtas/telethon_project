const head = document.getElementById('header')
const user_id = localStorage.getItem("user_id")

const linkDiv = document.createElement('div')
// if (user_id) {
    
const linkChats = document.createElement('a')
const linkProfile = document.createElement('a')
const linkWildberis = document.createElement('a')


linkChats.setAttribute('href', 'chats.html')
linkProfile.setAttribute('href', 'profile.html')
linkWildberis.setAttribute('href', 'waildberis.html')


const textChats = document.createTextNode('Чаты')
const textProfile = document.createTextNode('Профиль')
const textWildberis = document.createTextNode('Wildberis')

linkChats.appendChild(textChats)
linkProfile.appendChild(textProfile)
linkWildberis.appendChild(textWildberis)



linkDiv.appendChild(linkProfile)
linkDiv.appendChild(linkChats)
linkDiv.appendChild(linkWildberis)


// } 



const linkIndex = document.createElement('a')
linkIndex.setAttribute('href', 'index.html')
const textIndex = document.createTextNode('Главная')
linkIndex.appendChild(textIndex)
linkDiv.appendChild(linkIndex)

const divLogin = document.createElement('div')
const linklogin = document.createElement('a')
linklogin.setAttribute('href', 'login.html')
const textlogin = document.createTextNode('login')
linklogin.appendChild(textlogin)
divLogin.appendChild(linklogin)


head.appendChild(linkDiv)
head.appendChild(divLogin)

head.setAttribute('class', 'head')


const elA = linkDiv.querySelectorAll('a')
elA.forEach(el => {
    el.style.marginLeft = '10px'
})
