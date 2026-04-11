# 📋 Requisitos Funcionais - Gerenciamento de voluntários Meninas Digitais

Este documento lista todas as funcionalidades que o sistema deve possuir para atender aos objetivos do projeto. A lista está dividida por módulos de acordo com o perfil de usuário que interage com a funcionalidade.

**Índice:**
- [1. Módulo Voluntario](#1-módulo-administrativo)
- [2. Módulo Público](#3-módulo-público-visitante)
- [3. Voltar para o Índice da Documentação](../README.md)


> **Legenda de Prioridade:**
> * **Alta:** Essencial para o MVP (Mínimo Produto Viável).
> * **Média:** Importante, mas pode ficar para a versão 1.1.
> * **Baixa:** Desejável, funcionalidade extra.

---
<!-- | **RF** | ** ** | des | rel | pri | [ ] | -->
## 1. Landing Page
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RF001 | Exibição da Landing Page | Exibir uma página pública com informações institucionais do projeto, acessível sem autenticação | Rel  | Alta        | [ ]    |
| RF002 | Acesso ao Login | Exibir link ou botão na landing page que redireciona para a tela de login | Rel  | Alta        | [ ]    |
| RF003 | Conteúdo Estático | O conteúdo da landing page deve ser estático, gerenciado diretamente no código-fonte                | Rel  | Média        | [ ]    |
## 2. Módulo Autenticação
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RF004 | Login | Permitir que usuárias realizem login com RA (usuário) e senha | RF | Alta | [ ] |
| RF005 | Redirecionamento por Perfil | Redirecionar a usuária após login para a tela correspondente ao seu perfil | RF | Alta | [ ] |
| RF006 | Senha Padrão | Gerar automaticamente a senha padrão no cadastro: primeiro nome + último nome, minúsculos, sem espaços e sem acentos | RF | Alta | [ ] |
| RF007 | Alteração de Senha | Permitir que a usuária altere sua própria senha a qualquer momento | RF | Alta | [ ] |
| RF008 | Recuperação de Senha | Permitir recuperação de senha via e-mail, com link de redefinição de uso único e validade máxima de 1 hora | RF | Alta | [ ] |
| RF009 | Bloqueio por Tentativas | Bloquear o acesso após 5 tentativas de login incorretas consecutivas, exigindo aguardar 15 minutos | RF | Média | [ ] |
| RF010 | Logout | Permitir que a usuária encerre sua sessão a qualquer momento | RF | Alta | [ ] |
| RF011 | Expiração de Sessão | Encerrar automaticamente a sessão após 8 horas, exigindo novo login | RF | Média | [ ] |
