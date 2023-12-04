<script>
    // Variáveis reativas para armazenar a resposta da API, a promessa da busca e a lista de favoritos
    let resposta = "";
    let promise = getFavoritos();
    let favoritos = [];

    // Função assíncrona para obter a lista de filmes favoritos
    async function getFavoritos() {
        try {
            // Requisição à API para obter a lista de favoritos
            var res = await fetch(`http://localhost:8000/favorites/1`);
            
            // Imprimir a resposta no console para fins de depuração
            console.log(res);

            const text = await res.json();

            if (res.ok) {
                // Atualizar a lista de favoritos com os dados recebidos
                favoritos = text;
                return text;
            } else {
                throw new Error("Erro ao obter favoritos");
            }
        } catch (error) {
            console.error("Erro ao obter favoritos:", error);
            throw error;
        }
    }

    // Função chamada ao clicar no botão para carregar filmes favoritos
    function handleClick() {
        promise = getFavoritos();
    }

    // Função assíncrona para excluir um filme dos favoritos
    async function deleteFavorito(e) {
        e.preventDefault();
        // Obter o ID do filme a ser desfavoritado do formulário
        const tmdb_id = e.target.elements.tmdb_id.value;

        try {
            // Requisição à API para excluir o filme dos favoritos
            const res = await fetch(`http://localhost:8000/deleteFavoritos/1/${tmdb_id}`, {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'}
            });

            if (res.ok) {
                // Atualizar a resposta e a lista de favoritos após a exclusão bem-sucedida
                resposta = `Filme desfavoritado`;
                promise = getFavoritos();
            } else {
                throw new Error("Erro ao desfavoritar filme");
            }
        } catch (error) {
            console.error("Erro ao desfavoritar filme:", error);
            throw error;
        }
    }
</script>

<!-- Botão para carregar filmes favoritos -->
<button on:click={handleClick}> Carregar filmes favoritos... </button>

<!-- Renderização condicional da lista de favoritos -->
{#await promise}
    <p>...loading</p>
{:then favoritos}
    <!-- Título e iteração sobre a lista de favoritos -->
    <h1>Meus Filmes Favoritos</h1>
    {#each favoritos as favorito}
        <!-- Exibir informações sobre cada filme favorito -->
        <p>Nome: {favorito.title} - Id: {favorito.tmdb_id} </p>
        <!-- Formulário para desfavoritar um filme -->
        <form on:submit|preventDefault={deleteFavorito}>
            <input type="hidden" name="tmdb_id" value="{favorito.tmdb_id}">
            <button type="submit">Desfavoritar</button>
        </form>
    {/each}
{/await}
