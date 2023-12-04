<script>
    // Variável reativa para armazenar a resposta da solicitação fetch
    let resposta = "";

    /**
     * Função para enviar o formulário via solicitação fetch.
     * @param {Event} event - Evento de submissão do formulário.
     */
    async function sendForm(event) {
        // Evitar o comportamento padrão de envio do formulário
        event.preventDefault();

        // Obter os dados do formulário
        let formData = new FormData(event.target);
        let userData = Object.fromEntries(formData.entries());

        // Enviar a solicitação fetch para adicionar um novo usuário
        const response = await fetch('http://localhost:8000/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:5173'
            },
            body: JSON.stringify(userData)
        });

        try {
            // Verificar se a resposta tem um código de status 400 (Bad Request)
            if (response.status === 400) {
                // Usuário já cadastrado, exibir alerta correspondente
                alert('Usuário já cadastrado');
            } else {
                // A resposta é bem-sucedida, obter e armazenar a resposta JSON
                const jsonResponse = await response.json();
                console.log(response);

                // Atualizar a variável de resposta com a mensagem de sucesso
                resposta = JSON.stringify('Adicionado com sucesso');

                // Exibir alerta com a resposta
                alert(resposta);
            }
        } catch (error) {
            console.error('Erro ao processar a resposta da solicitação:', error);
        }
    }
</script>

<h2>New user</h2>

<p>{resposta}</p>

<!-- Formulário para adicionar um novo usuário -->
<form class="crud" on:submit|preventDefault={sendForm}>
    <!-- Campos para inserir informações do novo usuário -->
    <input type="text" name="name" placeholder="User name" required autocomplete="off">
    <input type="email" name="email" placeholder="Email" required autocomplete="off">
    <input type="password" name="password" placeholder="Password" required autocomplete="off">
    
    <!-- Botão de envio do formulário -->
    <input type="submit" value="Adicionar">
</form>

<style>
    form.crud {
        display: grid;
        gap: 5px;
        row-gap: 10px;
    }
</style>
