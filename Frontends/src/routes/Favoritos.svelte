<script>
    // Variáveis reativas para armazenar a resposta da API, a promessa da busca e a lista de favoritos
    let resposta = "";
    let promise = getFavoritos();
    let favoritos = [];

    // Função assíncrona para obter a lista de filmes favoritos
    async function getFavoritos() {
    try {
        var res = await fetch(`http://localhost:8000/favorites/1`);
        console.log(res);
        const text = await res.json();
        if (res.ok) {
            favoritos = text;
            console.log(favoritos);  // Imprima a variável favoritos no console
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
<!-- Botão para carregar filmes favoritos -->
<button on:click={handleClick}> Carregar filmes favoritos... </button>

{#await promise}
    <p>...loading</p>
{:then favoritos}
    <h1>Meus Filmes Favoritos</h1>
    <div class="favoritos-container">
        {#each favoritos as favorito}
            <div class="favorito">
                <p>{favorito.title}</p> 
                <img src={favorito.image} alt="capa" class="favorito-image"> 
                <p>ID: {favorito.tmdb_id}</p> 
                <form on:submit|preventDefault={deleteFavorito}>
                    <input type="hidden" name="tmdb_id" value={favorito.tmdb_id}>
                    <button type="submit" class="btn-desfavoritar">Desfavoritar</button>
                </form>
            </div>
        {/each}
    </div>
{:catch error}
    <p style="color: red;">{error.message}</p>
{/await}

<style>
    .favoritos-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }

    .favorito {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 10px;
        margin: 10px;
        text-align: center;
        width: 200px;
    }

    .favorito-image {
        max-width: 100%;
        height: auto;
        border-radius: 5px;
    }
    .btn-desfavoritar {
        margin-top: 10px;
        padding: 5px 10px;
        background-color: #ff4444;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }

    .btn-desfavoritar:hover {
        background-color: #ff0000;
    }
</style>