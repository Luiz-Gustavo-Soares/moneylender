// // dashboard

// // configs


function enviarEmail(id) {
    fetch(`api/enviaremail/${id}`)
    .then(response => response.json())
    .then(data => {})
    .catch(error => console.error(error))
}
