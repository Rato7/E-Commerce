document.getElementById('cep').addEventListener('blur', function() {
    let cep = this.value.replace(/\D/g, '')

    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (!data.erro) {
                document.getElementById('street').value = data.logradouro;
                document.getElementById('neighborhood').value = data.bairro;
                document.getElementById('city').value = data.localidade;
                document.getElementById('state').value = data.uf;
            } else {
                alert('CEP não encontrado.')
            }
        })
        .catch(() => alert('Erro ao buscar CEP.'))
    }
})