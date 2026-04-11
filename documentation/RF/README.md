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

## 3. Módulo Gerenciamento de Voluntárias
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RF012 | Cadastro de Voluntária | Permitir que Coordenadora e Admins cadastrem novas voluntárias com nome completo, RA, CPF, RG, e-mail, nacionalidade, estado civil, profissão e endereço completo | RF | Alta | [ ] |
| RF013 | Validação de CPF | Validar o CPF informado quanto ao formato e unicidade, não permitindo CPF duplicado | RF | Alta | [ ] |
| RF014 | Validação de RA | Validar o RA informado quanto à unicidade, não permitindo RA duplicado | RF | Alta | [ ] |
| RF015 | Geração de Senha Padrão | Gerar automaticamente a senha padrão da voluntária ao concluir o cadastro | RF | Alta | [ ] |
| RF016 | Edição de Voluntária | Permitir que Coordenadora e Admins editem os dados cadastrais de qualquer voluntária | RF | Alta | [ ] |
| RF017 | Alteração de Status | Permitir alteração do status de uma voluntária entre: Ativa, Desligada e Excluída | RF | Alta | [ ] |
| RF018 | Bloqueio ao Excluir | Bloquear imediatamente o acesso de voluntárias com status Excluída, mantendo seus dados no banco para histórico | RF | Alta | [ ] |
| RF019 | Listagem de Voluntárias | Exibir lista completa de voluntárias com indicação visual de status, ocultando Excluídas por padrão | RF | Alta | [ ] |
| RF020 | Filtro por Status | Permitir filtrar a lista de voluntárias por status: Ativa, Desligada ou Excluída | RF | Média | [ ] |
| RF021 | Busca de Voluntária | Permitir buscar voluntárias pelo nome ou RA na listagem | RF | Média | [ ] |
| RF022 | Exportação de Lista | Permitir que Coordenadora e Admins exportem a lista de voluntárias nos formatos Excel (.xlsx) e PDF | RF | Média | [ ] |
| RF023 | Confirmação de Ação Crítica | Exibir janela de confirmação antes de executar as ações de Desligar ou Excluir uma voluntária | RF | Média | [ ] |

## 4. Módulo Gerenciamento de Admins
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RF024 | Cadastro de Admin | Permitir que somente a Coordenadora cadastre novas usuárias com perfil Admin | RF | Alta | [ ] |
| RF025 | Alteração de Perfil | Permitir que somente a Coordenadora promova ou rebaixe o perfil de uma usuária entre Admin e Voluntária | RF | Alta | [ ] |
| RF026 | Remoção de Admin | Permitir que somente a Coordenadora desative ou remova o acesso de uma Admin | RF | Alta | [ ] |
| RF027 | Listagem de Admins | Exibir para a Coordenadora uma lista separada de todas as Admins cadastradas com indicação de status | RF | Média | [ ] |

## 5. Módulo Perfil da Voluntária
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RF028 | Visualização do Próprio Perfil | Exibir para a voluntária comum exclusivamente os seus próprios dados cadastrais após o login | RF | Alta | [ ] |
| RF029 | Restrição de Acesso a Terceiros | Impedir que a voluntária comum acesse dados de outras voluntárias em qualquer circunstância | RF | Alta | [ ] |
| RF030 | Restrição de Funcionalidades | Impedir que a voluntária comum acesse funcionalidades de cadastro, edição de terceiros ou alteração de status | RF | Alta | [ ] |
| RF031 | Alteração de Senha Própria | Permitir que a voluntária comum altere sua própria senha a qualquer momento | RF | Alta | [ ] |
