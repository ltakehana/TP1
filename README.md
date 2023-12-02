# Trabalho Prático 1 - Tecnicas de Programação em Plataformas Emergentes

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Como Iniciar

1. **Clonar o Repositório:**

    ```bash
    git clone https://github.com/ltakehana/TP1-TPPE-2023.2-Grupo4.git
    cd seu-projeto
    ```

2. **Construir e Iniciar os Contêineres Docker:**

    ```bash
    docker-compose up --build
    ```

3. **Acessar a Aplicação:**

    A aplicação estará disponível em [http://localhost:8000](http://localhost:8000).

4. **Como rodar os testes**
    Para rodar os testes deve-se fazer a instalação das dependencias. Nesse caso, rode no diretorio:

    ```bash
    pip install -r requirements.txt
    ```
    
    ou

    ```
    pip3 install -r requirements.txt
    ```

    Por fim, para rodar os testes basta rodar o comando:

    ```
    pytests
    ```

## Estrutura do Projeto

- `app/`: Contém o código-fonte da aplicação.
- `tests/`: Contém os testes da aplicação.
- `docker-compose.yml`: Configuração do Docker Compose para a aplicação.

## Padrão de Commits

Este projeto segue a convenção de commits [Conventional Commits](https://www.conventionalcommits.org/).

Exemplos de mensagens de commit:
- `feat: adiciona nova funcionalidade`
- `fix: corrige um bug`
- `chore: realiza tarefas de manutenção`