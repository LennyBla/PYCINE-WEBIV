<script>
  // Importando os estilos globais
  import '../globals.css';

  // Variáveis reativas para armazenar a promessa da busca e o nome do artista
  let promise = "";
  let nameArtist = "";

  // Função assíncrona para obter informações sobre um artista
  async function getArtista(name) {
      try {  
          const res = await fetch(`http://localhost:8000/artistas/${name}`);
          const text = await res.json();

          if (res.ok) {
              return text;
          } else {
              throw new Error(text);
          }
      } catch (error) {
          console.error('Erro ao Buscar:', error);
          throw error;
      }
  }

  // Função chamada ao clicar no botão de busca
  function handleClick() {
      promise = getArtista(nameArtist);
  }

  // Função assíncrona para favoritar um artista
  async function favoritarArtista(tmdb_id, name) {
      try {
          const res = await fetch(`http://localhost:8000/favorites/artist/1/${tmdb_id}`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ tmdb_id: name })
          });

          if (res.ok) {
              document.getElementById('alert-name').textContent = name;
              const alertDiv = document.getElementById('alert')
              alertDiv.style.display = 'block';
              setTimeout(() => { alertDiv.style.display = 'none';}, 3000); 
          } else {
              const errorText = await res.text();
              console.error('Erro ao favoritar artista:', errorText);
              alert('Erro ao favoritar artista.');
          }
      } catch (error) {
          console.error('Erro ao favoritar artista:', error);
      }
  }
</script>

<!-- Estrutura do componente -->
<div class="content">
  <!-- Barra de Pesquisa -->
  <div class="search">
      <form on:submit|preventDefault={handleClick}>
          <input bind:value={nameArtist} type="text" placeholder="Pesquisar" />
          <button type="submit">Buscar</button>
      </form>
  </div>

  <!-- Lista de Artistas -->
  <div class="artists">
      <h1>Artistas</h1>
      {#await promise}
          <p>Buscando...</p>
      {:then artistas}
          {#each artistas as artista}
              <!-- Card do Artista -->
              <div class="artist boxBorder">
                  <img src={`https://image.tmdb.org/t/p/w185/${artista.profile_path}`} alt={artista.name} class="artist-image" />
                  <div class="artist-details">
                      <h2>{artista.name}</h2>
                      <p>ID: {artista.id}</p>
                      <p>Nível de Popularidade: {artista.popularity}</p>
                      <p>{artista.biography}</p>
                      <button on:click={() => favoritarArtista(artista.id, artista.name)}>Favoritar</button>
                  </div>
              </div>
          {/each}
      {:catch error}
          <p>Nenhum Artista encontrado.</p>
      {/await}
  </div>

  <!-- Alerta de Favoritado -->
  <div id="alert">
      Favoritado ❤️‍🔥: <span id="alert-name"></span>
  </div>
</div>

<style>
  /* Estilos para o conteúdo */
  .content {
      display: flex;
      flex-direction: column;
      align-items: center;
  }

  /* Estilos para a barra de pesquisa */
  .search {
      padding: 1rem;
      margin-bottom: 20px;
  }

  /* Estilos para o card do artista */
  .artist {
      width: 60%;
      margin: 0 auto;
      padding: 2rem;
      flex: 1;
      box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
      margin-bottom: 20px;
  }

  .artist {
      width: 60%;
      margin: 0 auto;
      margin-bottom: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: justify;
  }

  .artist-image {
      max-width: 200px; /* Largura da imagem conforme o exemplo */
      margin-bottom: 1rem;
      border-radius: 10px;
  }

  .artist-details {
      background: white;
      padding: 1rem;
      border-radius: 10px;
      box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  }

  .artist-details h2 {
      margin-top: 0;
  }

  button {
      margin-top: 1rem;
  }

  /* Estilos para o alerta de favoritado */
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
