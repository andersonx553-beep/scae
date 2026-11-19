# Plano do SCAE

## Objetivo

Transformar a experiência do Almox (que roda no Condomínio Aqua Ville) num **produto único para várias empresas**: um endereço, um sistema e um banco de dados, com cada empresa vendo só os próprios dados, a própria logo e a própria equipe. O Anderson vende o acesso para outras empresas.

## Decisões já tomadas

| Assunto | Decisão |
|---|---|
| Nome | **SCAE**, Sistema de Controle de Almoxarifado e Estoque |
| Almox | Fica **intacto** e em produção. Não é alterado. Serve só de referência |
| Começo | Planejar bem antes de construir. Primeiro protótipo em HTML, refinado com o Anderson tela por tela |
| Login no protótipo | **Sem login por enquanto.** O protótipo abre direto por dentro do sistema |
| Firebase | **Um projeto novo**, separado do Almox, no plano **Blaze**, para **todas** as empresas. Nada de um projeto por cliente |
| Multiempresa | Cada empresa numa pasta própria do banco (`empresas/{id}/...`). Pessoas ligadas a empresas por e-mail Google, com papel |
| Papéis | Dono do SCAE (Anderson, vê todas), Administrador, Operador e Consulta |
| Marca | Logo do SCAE fixa no código. Logo e nome da empresa editáveis no Perfil da empresa, pelo administrador |
| Onde vai a logo da empresa | Menu, topo, comprovantes (saída, entrada, empréstimo, fardamento), histórico, cotações e PDFs |
| Planilhas | Exportação só se o cliente quiser. Sem logo, por enquanto |
| Visual | Azul-marinho escuro com preto, profissional e confiável, tema claro e escuro, sem emojis |
| Linguagens | **TypeScript** nas telas e **Python** nas automações e agentes (veja `arquitetura.md`) |
| Ambiente de trabalho | Claude Code **no PC do Anderson**, com a pasta do projeto aberta no VS Code |
| Uso sem internet | Implementação futura, só quando o Anderson pedir |

## Fases

### Fase 0: protótipo e plano (em andamento)
- [x] Marca SCAE (símbolo e logo horizontal)
- [x] Protótipo navegável com as telas principais e várias empresas
- [x] Sem login: entra direto, com "Trocar de empresa" e "Ver como"
- [ ] Revisar tela por tela com o Anderson e ajustar
- [ ] Prototipar o que falta: ferramentas e empréstimos (com assinatura), fardamento, importar saldo por planilha, relatórios em PDF
- [ ] Fechar a lista do que entra na primeira versão para vender (o "mínimo vendável")

### Fase 1: projeto de verdade
- [ ] Repositório novo e privado no GitHub (`scae`)
- [ ] Front em TypeScript com Vite. Decidir com o Anderson se fica em JavaScript/TypeScript puro, como o Almox, ou com React
- [ ] Projeto Firebase novo no Blaze: Auth (Google), Firestore, Storage e Functions
- [ ] **Alerta de orçamento** no Google Cloud desde o primeiro dia (por exemplo R$ 50 por mês)
- [ ] Regras de segurança multiempresa com testes automáticos no emulador, inclusive testes que tentam ler a empresa vizinha
- [ ] Hospedagem: Cloudflare (como o Almox) ou Firebase Hosting, a decidir. Domínio próprio quando for vender

### Fase 2: telas ligadas ao Firebase
- [ ] Login Google e escolha de empresa
- [ ] Perfil da empresa com envio da logo para o Storage
- [ ] Estoque, entrada de NF-e, saída, histórico, cotações e cadastros, com transações no servidor (veja `regras-de-negocio.md`)
- [ ] Comprovantes em PDF com a logo da empresa

### Fase 3: painel do dono e venda
- [ ] Criar empresa, convidar o responsável, suspender e reativar
- [ ] Cobrança (mensalidade por empresa): forma a decidir
- [ ] Termos de uso e política de privacidade (LGPD)

### Fase 4: automações e agente (Python)
- [ ] Aviso de estoque abaixo do mínimo (e-mail ou WhatsApp)
- [ ] Relatório semanal de consumo por destino
- [ ] Leitura automática do XML de NF-e que chega por e-mail
- [ ] Agente que responde perguntas sobre o estoque e avisa sobre problemas. É sempre um extra: o sistema funciona sem ele

### Depois
- Aplicativo .exe para Windows (casca do site, como planejado no Almox)
- Instalar no celular (PWA)
- Migrar o Aqua Ville do Almox para o SCAE, quando o SCAE estiver pronto e testado, num dia combinado e com backup

## Perguntas em aberto

1. Lista final do que entra na primeira versão para vender.
2. React ou JavaScript/TypeScript puro nas telas.
3. Hospedagem: Cloudflare ou Firebase Hosting.
4. Como cobrar as empresas (valor, forma e o que acontece quando não pagam).
5. Domínio do SCAE (exemplo: `scae.com.br`, se estiver livre) e o endereço provisório. Já existe o PR em rascunho do Almox para `scae.almox.workers.dev`, mas ele é do Almox, não do SCAE.
