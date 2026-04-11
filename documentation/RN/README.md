# ![Business Rules](https://img.shields.io/badge/Regras%20de%20Negócio-Lógica-blue?style=flat-square&logo=diagrams.net)

Este documento lista todas as funcionalidades que o sistema deve possuir para atender aos objetivos do projeto.

**Índice:**

- [1. Regras de negócio](#1-Regras-de-negócio)
- [2. Voltar para o Índice da Documentação](../README.md)


> **Legenda de Prioridade:**
Alta: Essencial para o MVP (Mínimo Produto Viável).
Média: Importante, mas pode ficar para a versão 1.1.
Baixa: Desejável, funcionalidade extra.

## 1. Regras de negócio
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RN001 | Usuário de Acesso | O identificador de acesso (login) de toda voluntária é o seu RA | RN | Alta | [ ] |
| RN002 | Composição da Senha Padrão | A senha padrão gerada no cadastro segue o padrão: primeiro nome + último nome, em letras minúsculas, sem espaços e sem acentos. Exemplo: "Ana Paula Ferreira" → senha: anaferreira | RN | Alta | [ ] |
| RN003 | Retenção de Dados ao Excluir | Voluntárias com status Excluída têm o acesso bloqueado imediatamente, mas seus dados permanecem no banco para fins de histórico e rastreabilidade | RN | Alta | [ ] |
| RN004 | Exclusividade da Coordenadora | Somente a Coordenadora pode criar, promover ou remover Admins | RN | Alta | [ ] |
| RN005 | Limitação de Admins | Admins não podem alterar dados de outras Admins nem da Coordenadora | RN | Alta | [ ] |
| RN006 | Herança de Privilégios | A Coordenadora possui todos os privilégios de Admin, além dos exclusivos do seu perfil | RN | Alta | [ ] |
| RN007 | Uso do E-mail | O e-mail da voluntária é obrigatório no cadastro e utilizado exclusivamente para recuperação de senha | RN | Alta | [ ] |
