<script>
<<<<<<< HEAD
    // Variáveis reativas para armazenar a resposta da API, a promessa da busca e a lista de favoritos
    let resposta = "";
=======
    // Inicializa uma promise para obter os artistas favoritos
>>>>>>> 2eefe52247eb6082aabcf9f95b1dcb902c96cae5
    let promise = getFavoritos();
    let favoritos = [];

    // Função assíncrona para obter artistas favoritos
    async function getFavoritos() {
        try {
<<<<<<< HEAD
            const res = await fetch(`http://localhost:8000/favoritesArtist/1`);
            console.log(res);
            const text = await res.json();
            if (res.ok) {
                artistasFavoritos = text;
                console.log(artistasFavoritos);
                return text;
=======
            // Faz uma requisição assíncrona para obter os artistas favoritos do servidor
            const res = await fetch(`http://localhost:8000/favoritesArtist/1`);
            if (res.ok) {
                // Se a resposta for bem-sucedida, obtém os dados em formato JSON
                const data = await res.json();
                favoritos = data; // Atualiza a lista de favoritos
                return data; // Retorna os dados obtidos
>>>>>>> 2eefe52247eb6082aabcf9f95b1dcb902c96cae5
            } else {
                throw new Error("Erro ao obter artistas favoritos");
            }
        } catch (error) {
            console.error("Erro ao obter artistas favoritos:", error);
<<<<<<< HEAD
            throw error;
        }
    }
    function handleClick() {
        promise = getFavoritos();
    }

    async function deleteFavorito(e) {
        e.preventDefault();
        const tmdb_id = e.target.elements.tmdb_id.value;

        try {
            const res = await fetch(`http://localhost:8000/deleteFavoritesArtista/1/${tmdb_id}`, {
=======
        }
    }

    // Função assíncrona para excluir um artista favorito
    async function deleteFavorito(e, id) {
        e.preventDefault();
        try {
            // Faz uma requisição assíncrona para excluir um artista favorito pelo ID
            const res = await fetch(`http://localhost:8000/deleteFavoritesArtista/1/${id}`, {
>>>>>>> 2eefe52247eb6082aabcf9f95b1dcb902c96cae5
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            if (res.ok) {
<<<<<<< HEAD
                resposta = `Artista desfavoritado`;
                promise = getFavoritos();
=======
                // Se a exclusão for bem-sucedida, atualiza a lista de favoritos chamando getFavoritos()
                await getFavoritos();
>>>>>>> 2eefe52247eb6082aabcf9f95b1dcb902c96cae5
            } else {
                throw new Error("Erro ao desfavoritar artista");
            }
        } catch (error) {
            console.error("Erro ao desfavoritar artista:", error);
<<<<<<< HEAD
            throw error;
=======
>>>>>>> 2eefe52247eb6082aabcf9f95b1dcb902c96cae5
        }
    }
</script>

<<<<<<< HEAD
<!-- Botão para carregar filmes favoritos -->
<button on:click={handleClick}> Carregar artistas favoritos... </button>
{#await promise}
    <p>...loading</p>
{:then artistasFavoritos}
    <h1>Meus Artistas Favoritos</h1>
    <div class="favoritos-container">
        {#each artistasFavoritos as artista}
            <div class="favorito">
                <p>{artista.name}</p> 
                <img src={`https://image.tmdb.org/t/p/w185/${artista.profile_path}`} alt="foto do artista" class="favorito-image"> 
                <p>ID: {artista.id}</p> 
                <form on:submit|preventDefault={deleteFavorito}>
                    <input type="hidden" name="tmdb_id" value={artista.id}>
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
=======
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
>>>>>>> 2eefe52247eb6082aabcf9f95b1dcb902c96cae5
