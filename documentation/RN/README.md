# ![Business Rules](https://img.shields.io/badge/Regras%20de%20Negócio-Lógica-blue?style=flat-square&logo=diagrams.net)

Este documento lista todas as funcionalidades que o sistema deve possuir para atender aos objetivos do projeto.

**Índice:**

- [1. Regras de negócio](#1-Regras-de-negócio)
- [2. Voltar para o Índice da Documentação](../README.md)


## 1. Regras de negócio
| ID   | Funcionalidade               | Descrição                                                                 |
|:----:|------------------------------|---------------------------------------------------------------------------|
| RN001 | Usuário de Acesso | O identificador de acesso (login) de toda voluntária é o seu RA |
| RN002 | Composição da Senha Padrão | A senha padrão gerada no cadastro segue o padrão: primeiro nome + último nome, em letras minúsculas, sem espaços e sem acentos. Exemplo: "Ana Paula Ferreira" → senha: anaferreira | 
| RN003 | Retenção de Dados ao Excluir | Voluntárias com status Excluída têm o acesso bloqueado imediatamente, mas seus dados permanecem no banco para fins de histórico e rastreabilidade | 
| RN004 | Exclusividade da Coordenadora | Somente a Coordenadora pode criar, promover ou remover Admins | 
| RN005 | Limitação de Admins | Admins não podem alterar dados de outras Admins nem da Coordenadora | 
| RN006 | Herança de Privilégios | A Coordenadora possui todos os privilégios de Admin, além dos exclusivos do seu perfil | 
| RN007 | Uso do E-mail | O e-mail da voluntária é obrigatório no cadastro e utilizado exclusivamente para recuperação de senha | 
