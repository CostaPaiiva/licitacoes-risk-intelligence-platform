# Licitacoes Risk Intelligence Platform

## Acesso local

O projeto sobe dois servicos via Docker Compose:

- `postgres`: banco PostgreSQL
- `pgadmin`: interface web para administrar o banco

## Credenciais padrao

### pgAdmin

- URL: `http://localhost:8081`
- Email: `admin@admin.com`
- Senha: `admin`

### PostgreSQL

- Host: `localhost` quando acessado da maquina host
- Porta: `5432`
- Usuario: `admin`
- Senha: `admin`
- Banco: `licitacoes_db`

## Se o login do pgAdmin nao entrar

O pgAdmin pode ter ficado com estado antigo em um container ja criado. Nesse caso, recrie tudo com:

```bash
docker compose down -v
docker compose up -d
```

Depois tente novamente:

- `admin@admin.com`
- `admin`

## Se o pgAdmin abrir, mas a conexao com o banco falhar

Ao cadastrar o servidor do PostgreSQL dentro do pgAdmin, use:

- Host name/address: `postgres`
- Port: `5432`
- Maintenance database: `licitacoes_db`
- Username: `admin`
- Password: `admin`

Isso funciona porque o `pgAdmin` fala com o banco pela rede interna do Docker, nao por `localhost`.
