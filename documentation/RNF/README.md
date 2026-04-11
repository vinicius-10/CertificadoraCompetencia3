# 🛡️ Requisitos Não Funcionais - MeninasHub

Este documento define as restrições técnicas, padrões de qualidade e exigências de infraestrutura do projeto.

**Índice:**
- [1. Tecnologias e Stack](#1-tecnologias-e-stack-restrições-de-implementação)
- [2. Usabilidade e Interface](#2-usabilidade-e-interface-uxui)
- [3. Segurança e Proteção de Dados](#3-segurança-e-proteção-de-dados)
- [4. Confiabilidade e Infraestrutura](#4-confiabilidade-e-infraestrutura)
- [5. Arquitetura e Qualidade de Código](#5-arquitetura-e-qualidade-de-código)
- [6. Desempenho](#6-desempenho)
- [7. Voltar para o Índice da Documentação](../README.md)


> **Legenda de Prioridade:**
> * **Crítica:** O sistema não pode ser implantado sem isso.
> * **Alta:** O sistema precisa ter para uma versão estável.
> * **Média:** Necessário para uma boa experiência, mas pode ficar para v1.1.
> * **Baixa:** Melhoria contínua / Diferencial.

---
<!-- | ** ** | ** ** |  | Alta | - | -->

## 1. Segurança
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RNF001 | Armazenamento de Senhas | Armazenar senhas com algoritmo de hash seguro (mínimo bcrypt com fator de custo 12), nunca em texto puro, inclusive a senha padrão gerada automaticamente | RNF | Alta | [ ] |
| RNF002 | Controle de Acesso no Servidor | Validar o controle de acesso por perfil no backend, nunca apenas no frontend | RNF | Alta | [ ] |
| RNF003 | Criptografia de Dados Sensíveis | Armazenar CPF e RG de forma criptografada no banco de dados | RNF | Alta | [ ] |
| RNF004 | Validade do Link de Recuperação | Links de recuperação de senha devem ser de uso único e expirar em até 1 hora após o envio | RNF | Alta | [ ] |
| RNF005 | Proteção contra Força Bruta | Bloquear acesso após 5 tentativas incorretas de login, conforme RF009 | RNF | Média | [ ] |

## 2. Desempenho
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RNF007 | Carregamento da Landing Page | A landing page deve carregar completamente em até 3 segundos em conexões de 10 Mbps | RNF | Média | [ ] |
| RNF008 | Tempo de Resposta das Telas | As telas autenticadas devem responder a qualquer ação do usuário em até 2 segundos | RNF | Média | [ ] |

## 3. Escalabilidade
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RNF009 | Capacidade do Banco de Dados | O banco de dados deve suportar o cadastro de até 500 voluntárias sem necessidade de reestruturação | RNF | Baixa | [ ] |

## 4. Usabilidade e Acessibilidade
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RNF010 | Responsividade | O sistema deve funcionar corretamente em telas de smartphone (mínimo 360px), tablet e desktop | RNF | Alta | [ ] |
| RNF011 | Mensagens de Erro | Mensagens de erro de formulário devem ser exibidas em português, de forma clara e próximas ao campo com problema | RNF | Média | [ ] |
| RNF012 | Acessibilidade WCAG | A landing page deve seguir as diretrizes WCAG 2.1 nível AA, com contraste mínimo de 4,5:1 para textos e suporte a navegação por teclado | RNF | Média | [ ] |

## 5. Compatibilidade
| ID   | Funcionalidade               | Descrição                                                                 | Tipo | Prioridade | Status |
|:----:|------------------------------|---------------------------------------------------------------------------|:----:|:-----------:|:------:|
| RNF013 | Compatibilidade de Navegadores | O sistema deve funcionar corretamente nas duas versões mais recentes de Chrome, Firefox, Edge e Safari | RNF | Alta | [ ] |
| RNF014 | Independência de Plugins | O sistema não deve depender de plugins externos para nenhuma funcionalidade | RNF | Alta | [ ] |












