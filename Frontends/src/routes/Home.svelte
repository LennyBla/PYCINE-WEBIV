<script>
    // Variável reativa para armazenar a promessa da busca de filmes
    let promise = getFilmes();
    // Variável para armazenar o termo de pesquisa
    let searchTerm = ""; 

    // Função assíncrona para obter a lista de filmes
    async function getFilmes() {
        try {
            // Faz uma solicitação GET para o endpoint /filmes
            const res = await fetch(`http://localhost:8000/filmes`);
            const text = await res.json();
            if (res.ok) {
                // Retorna a lista de filmes caso a requisição seja bem-sucedida
                return text;
            } else {
                // Lança um erro com a mensagem de erro da requisição em caso de falha
                throw new Error(text);
            }
        } catch (error) {
            // Exibe detalhes do erro no console para fins de depuração
            console.error('Erro ao obter filmes:', error);
            // Propaga o erro para que ele possa ser tratado no bloco catch na marcação Svelte
            throw error;
        }
    }

    // Função exportada chamada ao clicar no botão para recarregar a lista de filmes
    export function handleClick() {
        promise = getFilmes();
    }
</script>

<!-- Link para o stylesheet das Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">

{#await promise}
    <!-- Exibido durante a espera pela resposta da API -->
    <p>...aguardando</p>
{:then filmes}
    <!-- Renderização condicional da lista de filmes -->
    <div class="content flexCenter">
        {#each filmes as filme}
            <!-- Exibição de informações de cada filme -->
            <div class="movies boxBorder">
                <p>{filme.title}</p>
                <img src={filme.image} alt="capa" />
                <!-- Botão com ícone de coração -->
                <button class="icon"><i class="bi bi-heart"></i></button>             
            </div>
        {/each}
    </div>
{:catch error}
    <!-- Exibição de mensagens de erro em caso de falha na requisição -->
    <p style="color: red">{error.message}</p>
{/await}

<style>
    /* Estilos CSS para a marcação Svelte */

    .content {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }

    .movies {
        text-align: center;
    }

    .title {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    button {
        margin: .3rem auto;
        display: block;
    }

    .title {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }

    input[type="text"] {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        margin-right: 10px;
        font-size: 16px;
        width: 600px;
    }

    button {
        padding: 10px 20px;
        background-color: #007BFF;
        color: #fff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: #0056b3;
    }
</style>
