<script>
  import Artista from "./Artista.svelte";
  import Movie from "./Movie.svelte";
  import User from "./User.svelte";
  import Nav from "./Nav.svelte"
  import UserList from "./UserList.svelte";
  import Favoritos from "./Favoritos.svelte";  

  let menu = 1; // Defina o valor inicial do menu

  function switchPage(page) {
    menu = page;
  }
</script>

<nav class="menu-horizontal">
  <div class="components-nav">
    <ul>
     
      <li><a href="/" on:click|preventDefault={() => (menu = 1)}>Filmes</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 2)}>Artista</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 3)}>User</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 4)}>User List</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 5)}>Meus Favoritos</a></li>
    </ul>
  </div>

  <!-- Barra de Pesquisa e Ícone do Perfil -->
  <div class="right-content">
    <div class="perfil-container">
      <a href="/">
        <div class="Perfil">
          <i class="bi bi-person-circle perfil-icon"></i>
        </div>
      </a>
    </div>
  </div>
</nav>

<Nav bind:menu={menu} />


{#if menu === 1}
  <Movie />
{:else if menu === 2}
  <Artista />
{:else if menu === 3}
  <User />
{:else if menu === 4}
  <UserList />
{:else if menu === 5}
  <Favoritos />
{/if}

<style>
  nav.menu-horizontal {
    background-color: #000000d8;
    color: #fff;
    padding: 8px;
    display: flex;
    justify-content: space-between;
    box-shadow: 0px 1px 5px #373737;
    align-items: center;
  }

  nav.menu-horizontal ul {
    list-style: none;
    display: flex;
  }

  nav.menu-horizontal ul li {
    margin-left: 20px; /* Espaço entre os itens do menu */
  }

  nav.menu-horizontal a {
    text-decoration: none;
    color: #fdf8f8; /* Cor dos links */
    font-weight: 300;
  }

  .right-content {
    display: flex;
    align-items: center;
  }

  .perfil-container {
    margin-left: 15px; /* Espaço entre o ícone de pesquisa e o ícone do perfil */
  }

  .perfil-icon {
    font-size: 35px; /* Tamanho maior para o ícone de perfil */
    margin-right: 20px; /* Espaço entre o ícone de perfil e a barra de pesquisa */
    cursor: pointer;
    color: #676666;
  }
</style>