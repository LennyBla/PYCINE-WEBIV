<script>
    import { onMount, onDestroy } from 'svelte';
    let isOpen = false;
  
    function toggleDropdown() {
      isOpen = !isOpen;
    }
    function handleKeydown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      toggleDropdown();
    }
  }
    // Função para fechar o dropdown quando o usuário clica fora dele
    function handleClickOutside(event) {
      if (!event.target.closest('.dropdown-container')) {
        isOpen = false;
      }
    }
  
    // Ouvinte para detectar cliques fora do dropdown
    onMount(() => {
      window.addEventListener('click', handleClickOutside);
    });
  
    onDestroy(() => {
      window.removeEventListener('click', handleClickOutside);
    });
  </script>
  
  <div class="dropdown-container" 
  on:click|stopPropagation={toggleDropdown}
  on:keydown={handleKeydown}
  role="button" 
  tabindex="0" 
  aria-haspopup="true" 
  aria-expanded={isOpen.toString()}>

<button class="dropbtn">Gênero ▼</button>
{#if isOpen}
 <div class="dropdown-content">
   <!-- Links atualizados com href válidos ou substituídos por botões, se apropriado -->
   <a href="/genero/acao">Ação</a>
   <a href="/genero/comedia">Comédia</a>
   <a href="/genero/drama">Drama</a>
   <!-- Adicione mais opções de gêneros aqui -->
 </div>
{/if}
</div>

  <style>
    .dropdown-container {
      position: relative;
      display: inline-block;
    }
  
    .dropbtn {
      background-color: #4CAF50;
      color: white;
      padding: 16px;
      font-size: 16px;
      border: none;
      cursor: pointer;
    }
  
    .dropdown-content {
      display: none;
      position: absolute;
      background-color: #f9f9f9;
      min-width: 160px;
      box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
      z-index: 1;
    }
  
    .dropdown-content a {
      color: black;
      padding: 12px 16px;
      text-decoration: none;
      display: block;
    }
  
    .dropdown-content a:hover {background-color: #f1f1f1}
  
    /* Atualizado para usar a variável isOpen para controle de exibição */
    .dropdown-container .dropdown-content {
      display: block;
    }
  
    /* Removido o :hover CSS que causava conflito com a lógica do Svelte */
  </style>
  