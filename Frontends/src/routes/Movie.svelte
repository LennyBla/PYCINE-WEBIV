<script>
  import '../globals.css';
  let promise = getFilmes();
  let searchTerm = "";
  
  async function getFilmes(searchTerm) {
    try {
      const url = searchTerm
      ? `http://localhost:8000/filmes?title=${encodeURIComponent(searchTerm)}`
      : `http://localhost:8000/filmes`;

      const res = await fetch(url);
      const text = await res.json();

      if (res.ok) {
        return text;
      } else {
        throw new Error(text);
      }
    } catch (error) {
      console.error('Erro ao buscar filmes:', error);
      throw error;
    }
  }

  function search() {
    promise = getFilmes(searchTerm); // Chama getFilmes com o termo de busca
  }

  async function favoritarFilme(tmdb_id, title) {
    try {
      const res = await fetch(`http://localhost:8000/favorites/1/${tmdb_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title })
      });

      if (res.ok) {
        document.getElementById('alert-title').textContent = title;
        const alertDiv = document.getElementById('alert');
        alertDiv.style.display = 'block';
        setTimeout(() => {
          alertDiv.style.display = 'none';
        }, 3000);
      } else {
      const errorText = await res.text(); 
      console.error('Erro ao adicionar filme aos favoritos:', errorText);
      alert('Erro ao adicionar filme aos favoritos.');
    }
    } catch (error) {
      console.error('Erro ao favoritar filme:', error);
    }
  }
</script>

{#await promise then data}
  <div class="title flexCenter">
    <form action="">
      <input bind:value={searchTerm} type="text" />
      <button on:click={search}> Procurar </button>
    </form>
  </div>
  <h1> Filmes</h1>

  {#await promise}
    <p>...waiting</p>
  {:then filmes}
    <div class="filmes">
      <h1>Estreias de Filmes 🎞️</h1>
      <div class="content flexCenter">
        {#if filmes.estreias && filmes.estreias.length > 0}
          {#each filmes.estreias as filme}
            <div class="movies boxBorder">
              <p>{filme.title}</p>
              <img src="{filme.image}" alt="capa">
              <button type="button" on:click={() => favoritarFilme(filme.tmdb_id, filme.title)}>Favoritar</button>
            </div>
          {/each}
        {:else}
          <p>Nenhum filme em estreia encontrado.</p>
        {/if}
      </div>

      <h1>Filmes Populares 🎞️</h1>
      <div class="content flexCenter">
        {#if filmes.populares && filmes.populares.length > 0}
          {#each filmes.populares as filme}
            <div class="movies boxBorder">
              <p>{filme.title}</p>
              <img src="{filme.image}" alt="capa">
              <button type="button" on:click={() => favoritarFilme(filme.tmdb_id, filme.title)}>Favoritar</button>
            </div>
          {/each}
        {:else}
          <p>Nenhum filme popular encontrado.</p>
        {/if}
      </div>

      <div id="alert">
        Favoritado ❤️‍🔥: <span id="alert-title"></span>
      </div>
    </div>

  {:catch error}
    <p style="color: red">{error.message}</p>
  {/await}
{/await}


<style>
  .content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    text-align: center;
  }

  .movies {
    text-align: center;
    background-color: #6b6a6af4;
  }
  .movies p {
    color: #ffffff;
    font-size: 20px;
  }
  h1 {
    text-align: center;
    color: #030303;
    margin-top: 1rem;
  }
 input {
    padding: 1rem;
    margin: 20px; 
  }

  button {
    margin: .3rem auto;
    display: block;
  }
  button {
    padding: 10px 20px;
    background-color: #052445;
    color: #fffffff1;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #4a2eaf; /* Cor de fundo do botão ao passar o mouse */
  }
  .boxBorder {
    gap: 0.5rem;
    padding: 1rem;
    margin: 0.5rem;
    border: 1px solid rgb(16, 15, 15);
    border-radius: 10px;
    box-shadow: 5px 5px 3px 0px rgba(0, 0, 0, 1);
  }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
  }
  #alert {
    display: none;
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: #000000;
    color: white;
    padding: 16px;
    z-index: 1000;
  }

</style>
