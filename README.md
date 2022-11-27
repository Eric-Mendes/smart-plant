# smart-plant backend
Projeto de uma fábrica inteligente para a matéria MC855. 

## Rodando o projeto
Há um ambiente Docker para facilitar no encapsulamento do projeto. Para rodá-lo basta digitar o comando abaixo:
```bash
# Necessário ter sudo da máquina
mkdir -p ~/.mytb-data && sudo chown -R 799:799 ~/.mytb-data
mkdir -p ~/.mytb-logs && sudo chown -R 799:799 ~/.mytb-logs

# docker-compose up --build em windows e mac
docker compose up --build
```
Após isto, é possível acessar a API no endereço [localhost:8000](localhost:8000), o Keycloak no endereço [localhost:8080](localhost:8080) (instruções abaixo), e o thingsboard no endereço [localhost:9090](localhost:9090) (informações de login nas envvars no docker-compose.yaml).

Para corretamente derrubar este projeto após o uso, rode o comando abaixo:
```bash
# docker-compose down --remove-orphans em windows e mac
docker compose down --remove-orphans
```

### Keycloak
O serviço utilizado para gerenciar os usuários é o [Keycloak](https://www.keycloak.org/).

Após subir os containers, é possível acessar o painel de administrador através do endereço [http://localhost:8080/auth/admin](http://localhost:8080/auth/admin),
usando, por padrão, as credenciais username: admin e password: admin para acessar o painel. 

Pelo painel é possível gerenciar os usuários existentes, criar novos usuários, adicionar grupos, entre outras funcionalidades.

### Variáveis de ambiente
Você deve notar que o projeto depende de algumas variáveis de ambiente para rodar. 
Para subir os containeres com elas, crie na raiz um arquivo chamado de `.env` com as chaves e valores destas variáveis (entre em contato com os responsáveis para saber quais são).

Por exemplo, as variáveis de ambiente são usadas pelos endpoints de autenticação do Keycloak. 
Um exemplo de .env para poder usar os endpoints de autenticação está no arquivo **.env.example** na raíz do projeto.

Para o thingsboard, é necessario definir a url utilizada e usuario/senha de um usuario Tenant. No arquivo .env.exemple estão definidas as variaveis para rodar utilizando o container do docker.