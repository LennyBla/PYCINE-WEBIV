<script>
  import '../globals.css';
  import { onMount } from 'svelte';

  let filmesPopulares = [];
  let filmesEmEstreia = [];
  let filmesPesquisados = [];
  let searchTerm = "";

  onMount(async () => {
    await loadPopularAndNowPlaying();
  });

  async function loadPopularAndNowPlaying() {
    filmesPopulares = await fetchApi('/filmes-populares');
    filmesEmEstreia = await fetchApi('/filmes-em-estreia');
  }
  async function fetchApi(endpoint) {
    try {
      const response = await fetch(`http://localhost:8000${endpoint}`);
      const data = await response.json();
      return response.ok ? (data.populares || data.estreias || data.search || []) : [];
    } catch (error) {
      console.error('Erro ao buscar filmes:', error);
      return [];
    }
  }

  async function search() {
    if (searchTerm) {
      filmesPesquisados = await fetchApi(`/pesquisar-filmes?search=${encodeURIComponent(searchTerm)}`);
    }
  }
  // Função assíncrona para favoritar um filme
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
        // Atualiza o alerta com o título do filme favoritado
        document.getElementById('alert-title').textContent = title;
        // Exibe o alerta
        const alertDiv = document.getElementById('alert');
        alertDiv.style.display = 'block';
        // Esconde o alerta após 2 segundos
        setTimeout(() => {
          alertDiv.style.display = 'none';
        }, 2000);
      } else {
        // Em caso de falha, exibe detalhes do erro no console e alerta o usuário
        const errorText = await res.text();
        console.error('Erro ao adicionar filme aos favoritos:', errorText);
        alert('Erro ao adicionar filme aos favoritos.');
      }
    } catch (error) {
      // Exibe detalhes do erro no console para fins de depuração
      console.error('Erro ao favoritar filme:', error);
    }
  }
</script>

<div class="title flexCenter">
  <form on:submit|preventDefault={search}>
    <input bind:value={searchTerm} type="text" />
    <button type="submit"> Procurar </button>
  </form>
</div>

<h1>Filmes</h1>

<!-- Seção de filmes pesquisados -->
{#if filmesPesquisados.length > 0}
  <h2>Resultados da Pesquisa</h2>
  <div class="content flexCenter">
    {#each filmesPesquisados as filme}
      <div class="movies boxBorder">
        <p>{filme.title}</p>
        <img src={filme.image} alt="capa">
        <button type="button" on:click={() => favoritarFilme(filme.tmdb_id, filme.title)}>Favoritar</button>
      </div>
    {/each}
  </div>
{/if}

<!-- Seção de estreias de filmes -->
<h2>Estreias de Filmes 🎞️</h2>
<div class="content flexCenter">
  {#each filmesEmEstreia as filme}
    <div class="movies boxBorder">
      <p>{filme.title}</p>
      <img src={filme.image} alt="capa">
      <button type="button" on:click={() => favoritarFilme(filme.tmdb_id, filme.title)}>Favoritar</button>
    </div>
  {/each}
</div>

<!-- Seção de filmes populares -->
<h2>Filmes Populares 🎞️</h2>
<div class="content flexCenter">
  {#each filmesPopulares as filme}
    <div class="movies boxBorder">
      <p>{filme.title}</p>
      <img src={filme.image} alt="capa">
      <button type="button" on:click={() => favoritarFilme(filme.tmdb_id, filme.title)}>Favoritar</button>
    </div>
  {/each}
</div>

<div id="alert">
  Favoritado ❤️‍🔥: <span id="alert-title"></span>
</div>

<style>
  /* Estilos CSS para a marcação Svelte */

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
