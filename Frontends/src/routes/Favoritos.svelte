<script>
    let resposta = "";
    let promise = getFavoritos();
    let favoritos = [];
// Adicionar Listar e favoritar e desfavoritar artisata aqui tambem
    async function getFavoritos() {
        try {
            var res = await fetch(`http://localhost:8000/favorites/1`);
            console.log(res);
            const text = await res.json();
            if (res.ok) {
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

    function handleClick() {
        promise = getFavoritos();
    }

    async function deleteFavorito(e) {
        e.preventDefault();
        const tmdb_id = e.target.elements.tmdb_id.value;

        try {
            const res = await fetch(`http://localhost:8000/deleteFavoritos/1/${tmdb_id}`, {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'}
            });

            if (res.ok) {
                resposta = `Filme desfavoritado`;
                // Somente fazer um novo getFavoritos se a exclusão for bem-sucedida (retorno 200)
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

<button on:click={handleClick}> Carregar filmes favoritos... </button>

{#await promise}
    <p>...loading</p>
{:then favoritos}
    <h1>Meus Filmes Favoritos</h1>
    {#each favoritos as favorito}
        <p>Nome: {favorito.title} - Id: {favorito.tmdb_id} </p>
        <form on:submit|preventDefault={deleteFavorito}>
            <input type="hidden" name="tmdb_id" value="{favorito.tmdb_id}">
            <button type="submit">Desfavoritar</button>
        </form>
    {/each}
{/await}