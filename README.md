# 🚗 Sistema de Aluguel de Carros: RentSchema

Este projeto é um sistema de gerenciamento e aluguel de carros, desenvolvido em **Python**, com interface gráfica usando **Tkinter**, seguindo uma arquitetura limpa e modular.  
A persistência dos dados é feita em **MariaDB**.

---

## 📁 Estrutura do Projeto

```
rent_schema/
│
├── app/
│ ├── config/ # Configurações
│ ├── controllers/ # Controladores (parte do MVC)
│ ├── core/ # Regras de negócio / serviços
│ ├── database/ # Conexão e consultas ao MariaDB
│ ├── main.py # Arquivo inicial do projeto
│ ├── models/ # Modelos (parte do MVC)
│ ├── utils/ # Funções auxiliares
│ └── views/ # Visualizações (parte do MVC)
│
├── requirements.txt # Dependências do projeto
├── README.md # Documentação do projeto
└── .gitignore # Arquivos ignorados pelo Git
```

A arquitetura segue o padrão **MVC + Services**, garantindo separação entre:

- Interface (Tkinter)
- Lógica de negócio
- Acesso ao banco
- Configurações

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter** (GUI)
- **MariaDB**
- Arquitetura modular (MVC + Services)

---

## 🚀 Como Rodar o Projeto

### 1) Instalar dependências

```bash
pip install -r requirements.txt
```
Antes de instalar as dependências, é necessário ter a biblioteca [MariaDB Connector/C](https://mariadb.com/docs/connectors/mariadb-connector-c/install-mariadb-connector-c) instalada no sistema, para que o pacote **mariadb** seja instalado corretamente.

### 2) Criar o arquivo de configuração do banco

Crie o arquivo:

```
app/config/database.ini
```

Com o conteúdo:

```ini
[DATABASE]
host = localhost
user = root
password = sua_senha
database = nome_do_banco
port = 3306
```

### 3) Executar o projeto

```bash
python3 app/main.py
```

---

## 🗂️ Banco de Dados

Crie o banco antes de rodar:

```sql
CREATE DATABASE nome_do_banco;
```

Exemplo de tabela inicial:

```sql
CREATE TABLE usuarios (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(100)
)
```

---

## 🤝 Contribuição

Sinta-se à vontade para abrir PRs, issues e sugestões.
Este projeto foi estruturado para ser didático, escalável e fácil de evoluir.

---

## 📜 Licença

Este projeto pode ser usado livremente para fins acadêmicos ou pessoais.

---

## 👨‍💻 Autores

Projeto desenvolvido por **Armando e Equipe** para o trabalho de Fundamentos de Banco de Dados e prática de:

- Python
- Tkinter
- Arquitetura de software
- Banco de Dados
- Clean Code
- Boas práticas em desenvolvimento