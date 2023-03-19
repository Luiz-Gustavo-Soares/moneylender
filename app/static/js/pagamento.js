// Area de pagamento

let AreaPagamento = document.querySelector('.area-pagamento')

function closeAreaPagamento() {
    AreaPagamento.style.display = 'none'
    AreaPagamento.querySelector('.qrs').style.display = 'none'
}


AreaPagamento.querySelector('#mostar-qr-pix').addEventListener('click', () => {
    AreaPagamento.querySelector('.qrs').style.display = 'block'
    AreaPagamento.querySelector('.pix').style.display = 'block'
    AreaPagamento.querySelector('.pix-total').style.display = 'none'
})

AreaPagamento.querySelector('#mostar-qr-pix-total').addEventListener('click', () => {
    AreaPagamento.querySelector('.qrs').style.display = 'block'
    AreaPagamento.querySelector('.pix').style.display = 'none'
    AreaPagamento.querySelector('.pix-total').style.display = 'block'
})

function getAreaPagamento(idDivida) {
    let id = Number(idDivida)
    if (!id) {
        console.error('Parametro id especificado incorretamento')
        return
    }


    fetch(`/api/pagamento/${id}`)
    .then(response => response.json())
    .then(data => {
        const {meses_devendo, valor, pix, pix_total} = data

        AreaPagamento.querySelector('#parcela').textContent = 'R$ ' + Number(valor * meses_devendo).toFixed(2)
        AreaPagamento.querySelector('#total').textContent = 'R$ ' + Number(valor).toFixed(2)

        AreaPagamento.querySelector('.pix').src = pix
        AreaPagamento.querySelector('.pix-total').src = pix_total

        AreaPagamento.style.display = 'flex'
    })
    .catch(error => console.error(error))
}
