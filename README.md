# smart-plant backend
Projeto de uma fábrica inteligente para a matéria MC855. 

## Rodando o projeto
Há um ambiente Docker para facilitar no encapsulamento do projeto. Para rodá-lo basta digitar o comando abaixo:
```bash
# docker-compose up em windows e mac
docker compose up
```
Após isto, é possível acessar a API no endereço [localhost:8000](localhost:8000).

Para corretamente derrubar este projeto após o uso, rode o comando abaixo:
```bash
# docker-compose down --remove-orphans em windows e mac
docker compose down --remove-orphans
```

### Variáveis de ambiente
Você deve notar que o projeto depende de algumas variáveis de ambiente para rodar. 
Para subir os containeres com elas, crie na raiz um arquivo chamado de `.env` com as chaves e valores destas variáveis (entre em contato com os responsáveis para saber quais são).