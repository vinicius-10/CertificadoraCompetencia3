## Banco de dados

## 📑 Sumário
- [MER](#-Modelo-entidade-relacionamento)
- [Dicionario de dados user](#-)
- [Dicionario de dados ](#-)
- [Dicionario de dados ](#-)
- [Dicionario de dados ](#-)
- [Dicionario de dados ](#-)
- [Dicionario de dados ](#-)
- [Documetação](../README.md)

---

<!-- 

|o	o|	0/1
||	||	1/1
}o	o{	0/n
}|	|{	1/n

-->

## Modelo entidade relacionamento
```mermaid
erDiagram
    
    users {
        bigInt id PK
        bigInt ranks_id FK
        boolean enable
        string name
        string email "Unique, Index"
        string password
        string avatar_path
        timestamp email_verified_at "nullable"
        timestamp created_at
        timestamp updated_at
    }


    
```


## 📕 Dicionário de Dados

## 
| Coluna | Tipo | PK/FK? | Obrigatório? | Descrição |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT | **PK** | Sim | Identificador único auto-incremento. |
| `name` | VARCHAR(100) | | Sim | Nome completo do usuário. |
| `email` | VARCHAR(255) | | Sim | Deve ser único no sistema. |
