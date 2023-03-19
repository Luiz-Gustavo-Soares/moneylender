// button disable
cardDividas = document.querySelectorAll('.card-divida')

for (let i=0; i<cardDividas.length;  i++ ) {
    let valorDivida = Number(cardDividas[i].querySelector('.mes').textContent)
    if (valorDivida == 0) cardDividas[i].querySelector('button').disabled = true
    else cardDividas[i].querySelector('button').disabled = false
}
