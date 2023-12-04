<script>
    // Inicializa uma promise para obter os artistas favoritos
    let promise = getFavoritos();
    let favoritos = [];

    // Função assíncrona para obter artistas favoritos
    async function getFavoritos() {
        try {
            // Faz uma requisição assíncrona para obter os artistas favoritos do servidor
            const res = await fetch(`http://localhost:8000/favoritesArtist/1`);
            if (res.ok) {
                // Se a resposta for bem-sucedida, obtém os dados em formato JSON
                const data = await res.json();
                favoritos = data; // Atualiza a lista de favoritos
                return data; // Retorna os dados obtidos
            } else {
                throw new Error("Erro ao obter artistas favoritos");
            }
        } catch (error) {
            console.error("Erro ao obter artistas favoritos:", error);
        }
    }

    // Função assíncrona para excluir um artista favorito
    async function deleteFavorito(e, id) {
        e.preventDefault();
        try {
            // Faz uma requisição assíncrona para excluir um artista favorito pelo ID
            const res = await fetch(`http://localhost:8000/deleteFavoritesArtista/1/${id}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            if (res.ok) {
                // Se a exclusão for bem-sucedida, atualiza a lista de favoritos chamando getFavoritos()
                await getFavoritos();
            } else {
                throw new Error("Erro ao desfavoritar artista");
            }
        } catch (error) {
            console.error("Erro ao desfavoritar artista:", error);
        }
    }
</script>

<!-- Botão para carregar artistas favoritos quando clicado -->
<button on:click={getFavoritos}> Carregar artistas favoritos... </button>

<!-- Bloco de código para lidar com a promise de carregamento -->
{#await promise}
    <p>Carregando...</p>
{:then favoritos}
    <!-- Exibe a lista de artistas favoritos -->
    <h1>Meus Artistas Favoritos</h1>
    {#each favoritos as favorito}
        <p>Nome: {favorito.name} - Id: {favorito.id} </p>
        <!-- Botão para desfavoritar um artista específico -->
        <button on:click={(e) => deleteFavorito(e, favorito.id)}>Desfavoritar</button>
    {/each}
{:catch error}
    <!-- Exibe uma mensagem de erro em caso de falha -->
    <p style="color: red">Erro ao carregar: {error.message}</p>
{/await}
