<script>
    // Variáveis reativas para armazenar a resposta da API, a promessa da busca e a lista de favoritos
    let resposta = "";
    let promise = getFavoritos();
    let favoritos = [];

    // Função assíncrona para obter a lista de filmes favoritos
    async function getFavoritos() {
        try {
            const res = await fetch(`http://localhost:8000/favoritesArtist/1`);
            console.log(res);
            const text = await res.json();
            if (res.ok) {
                artistasFavoritos = text;
                console.log(artistasFavoritos);
                return text;
            } else {
                throw new Error("Erro ao obter artistas favoritos");
            }
        } catch (error) {
            console.error("Erro ao obter artistas favoritos:", error);
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
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'}
            });

            if (res.ok) {
                resposta = `Artista desfavoritado`;
                promise = getFavoritos();
            } else {
                throw new Error("Erro ao desfavoritar artista");
            }
        } catch (error) {
            console.error("Erro ao desfavoritar artista:", error);
            throw error;
        }
    }
</script>

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