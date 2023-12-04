<script>
    let resposta = "";
    let promise = getUsers();

    // Função para obter a lista de usuários
    async function getUsers() {
        // Faz uma solicitação GET para o endpoint /users
        const res = await fetch(`http://localhost:8000/getUsers/`);
        const text = await res.json();
        if (res.ok) {
            // Retorna os dados se a resposta for bem-sucedida
            return text;
        } else {
            // Lança um erro se a resposta não for bem-sucedida
            throw new Error(text);
        }
    }

    // Função chamada ao clicar no botão para recarregar usuários
    function handleClick() {
        promise = getUsers();
    }

    // Função para excluir um usuário
    async function deleteUser(e) {
        // Evita o comportamento padrão do envio do formulário
        e.preventDefault();
        const userId = e.target.elements.id.value;
        const userName = e.target.elements.name.value;

        // Faz uma solicitação DELETE para excluir o usuário pelo ID
        const res = await fetch(`http://localhost:8000/users/${userId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (res.ok) {
            // Atualiza a mensagem de resposta
            resposta = `Usuário ${userName} excluído`;

            // Faz uma solicitação GET para atualizar a lista de usuários após a exclusão bem-sucedida
            promise = getUsers();
        }
    }
</script>

<!-- Botão para recarregar usuários -->
<button on:click={handleClick}> Carregar Usuários... </button>

{#await promise}
  <!-- Exibido enquanto a promessa está pendente (carregando) -->
  <p>...loading</p>
{:then users}
  <!-- Exibido quando a promessa é resolvida com sucesso -->
  <h1>Lista de Usuários</h1>
  {#each users as user}
      <!-- Exibe informações sobre cada usuário e fornece um botão para excluí-lo -->
      <p>ID: {user.id} - Nome: {user.name} - Email: {user.email}</p>
      
      <form on:submit|preventDefault={deleteUser}>
          <!-- Campos ocultos para enviar informações sobre o usuário a ser excluído -->
          <input type="hidden" name="name" value="{user.name}">
          <input type="hidden" name="id" value="{user.id}">
          <button type="submit">Excluir Usuário</button>
      </form>
  {/each}

{:catch error}
    <!-- Exibido em caso de erro -->
    <p style="color: red">{error.message}</p>
{/await}
