<script>
    // Variável reativa para armazenar a resposta da solicitação fetch
    let resposta = "";

    /**
     * Função para enviar o formulário via solicitação fetch.
     * @param {Event} e - Evento de submissão do formulário.
     * @param {string} method - Método HTTP (e.g., 'PUT', 'POST').
     * @param {string} url - URL para a qual a solicitação será enviada.
     */
    async function sendForm(e, method, url) {
        e.preventDefault();

        // Obter os dados do formulário
        let formData = new FormData(e.target || undefined);
        let data = Object.fromEntries(formData.entries());

        // Enviar a solicitação fetch
        const res = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        // Obter e armazenar a resposta JSON
        const json = await res.json();
        resposta = JSON.stringify(json);
    }

    /**
     * Função específica para atualizar usuário.
     * @param {Event} e - Evento de submissão do formulário.
     */
    async function updateUser(e) {
        // Obter o ID do usuário do formulário
        const userId = e.target.querySelector('input[name="id"]').value;

        // Chamar a função geral de envio de formulário com o método PUT
        sendForm(e, 'PUT', `http://localhost:8000/users/${userId}`);
    }
</script>

<!-- Conteúdo do formulário -->
<h2>Update user</h2>

<!-- Formulário para atualizar usuário -->
<form class="crud" on:submit|preventDefault={updateUser}>
    <!-- Campos para inserir novas informações do usuário -->
    <input type="text" name="name" placeholder="New name" autocomplete="off">
    <input type="text" name="email" placeholder="New email" autocomplete="off">
    <input type="text" name="password" placeholder="New password" autocomplete="off">
    
    <!-- Campo oculto para armazenar o ID do usuário -->
    <!-- svelte-ignore missing-declaration -->
    <input type="hidden" name="id" value={user.id}>
    
    <!-- Botão de envio do formulário -->
    <input type="submit" value="Update">
</form>
