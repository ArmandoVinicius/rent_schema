# 🚗 RentSchema — Sistema de Aluguel de Carros

Sistema de gerenciamento e aluguel de carros desenvolvido em **Python**, com interface gráfica utilizando **Tkinter + ttkbootstrap**, seguindo a arquitetura **MVC + Services**.  
Os dados são persistidos em **MariaDB**, integrando conceitos de modelagem e implementação de banco de dados.

Este projeto foi desenvolvido como trabalho prático da disciplina de **Banco de Dados**.

---

## 📌 Funcionalidades

### 🔐 Autenticação

- Cadastro de clientes
- Login de usuários
- Controle de acesso por cargo (`user` ou `admin`)

### 📊 Dashboard

- Listagem de carros cadastrados
- Exibição de informações do modelo do carro
- Acesso à tela de detalhes do carro

### 👨‍💼 Funcionalidades do Administrador

- CRUD de carros
- Gerenciamento de modelos de veículos
  - Marca
  - Descrição
  - Categoria
  - Valor da diária
- Atualização de dados dos carros

### 🚘 Aluguel de Carros

- Visualização de detalhes do carro
- Seleção de período de aluguel (data início e fim)
- Validação de disponibilidade do carro por data
- Bloqueio de aluguel para carros:
  - em manutenção
  - inativos
- Tela de pagamento (simulada)
  - escolha da forma de pagamento
  - confirmação de pagamento
- Após pagamento, o carro passa para o status **alugado**

---

## 📁 Estrutura do Projeto

```txt
rent_schema/
│
├── app/
│   ├── config/          # Configurações (database.ini)
│   ├── controllers/     # Controllers (MVC)
│   ├── core/            # Services, regras de negócio e sessão
│   ├── database/        # Conexão com o banco e setup
│   ├── models/          # Models (acesso a dados / SQL)
│   ├── utils/           # Funções utilitárias (UI, helpers)
│   ├── views/           # Views (Tkinter / ttkbootstrap)
│   └── main.py          # Arquivo principal (entrypoint)
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 💿 Setup e Execução

### Pré-requisitos

- Python 3.8+

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/ArmandoVinicius/rent_schema
   ```

2. Navegue até o diretório do projeto:

   ```bash
    cd rent_schema
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados MySQL conforme o arquivo `database.ini` em `app/config/`.

   ```ini
   [mysql]
   host = seu_host
   database = seu_banco_de_dados
   user = seu_usuario
   password = sua_senha
   port = sua_porta (padrão 3306)
   ```

5. Execute o setup do banco:

   ```bash
   python -m app.database.setup
   ```

6. Inicie a aplicação:
   ```bash
   python -m app.main
   ```

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.
