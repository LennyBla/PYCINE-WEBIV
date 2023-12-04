<script>
    let promise = getFavoritos();
    let favoritos = [];
  
    async function getFavoritos() {
      try {
        const res = await fetch(`http://localhost:8000/favoritesArtist/1`);
        if (res.ok) {
          const data = await res.json();
          favoritos = data;
          return data;
        } else {
          throw new Error("Erro ao obter artistas favoritos");
        }
      } catch (error) {
        console.error("Erro ao obter artistas favoritos:", error);
      }
    }
  
    async function deleteFavorito(e, id) {
      e.preventDefault();
      try {
        const res = await fetch(`http://localhost:8000/deleteFavoritesArtista/1/${id}`, {
          method: 'DELETE',
          headers: {'Content-Type': 'application/json'}
        });
  
        if (res.ok) {
          // Atualizar a lista de favoritos após a exclusão
          await getFavoritos();
        } else {
          throw new Error("Erro ao desfavoritar artista");
        }
      } catch (error) {
        console.error("Erro ao desfavoritar artista:", error);
      }
    }
  </script>
  
  <button on:click={getFavoritos}> Carregar artistas favoritos... </button>
  
  {#await promise}
    <p>Carregando...</p>
  {:then favoritos}
    <h1>Meus Artistas Favoritos</h1>
    {#each favoritos as favorito}
      <p>Nome: {favorito.name} - Id: {favorito.id} </p>
      <button on:click={(e) => deleteFavorito(e, favorito.id)}>Desfavoritar</button>
    {/each}
  {:catch error}
    <p style="color: red">Erro ao carregar: {error.message}</p>
  {/await}
  