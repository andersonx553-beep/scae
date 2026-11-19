# SCAE: instruções para o Claude Code

**SCAE = Sistema de Controle de Almoxarifado e Estoque.** É um produto novo, multiempresa, para vender a várias empresas (condomínios, hotéis, escolas, indústrias pequenas). Ele nasce da experiência do **Almox**, o sistema que roda hoje no Condomínio Aqua Ville, mas **não é o Almox** e não mexe nele.

Quem decide é o **Anderson**. Nos registros antigos do Almox ele aparece como "Rainara", que era o nome de outra conta Claude dele; é a mesma pessoa. Você é o dev sênior: planeja, executa, testa e dá opinião sincera.

## Como trabalhar com o Anderson

- **Idioma:** tudo em português do Brasil: interface, textos, comentários, commits e documentação.
- **Planejamento primeiro.** Estamos na fase de **planejamento e protótipo**. Antes de qualquer coisa grande, apresente o plano e espere o "ok". Ele prefere montar o plano inteiro antes de aplicar.
- **Seja sincero e dê sugestões.** Não siga cegamente o que ele propõe; se houver um jeito melhor, diga e explique de forma simples. Ele aprende junto ("me ensine, você é o professor aqui").
- Ele costuma ditar por voz, então algumas palavras chegam trocadas. "Sky", "Skype" e "Scae" querem dizer **SCAE**. "Blazor" quer dizer o plano **Blaze** do Firebase. "Amoxágua" e "inbox" querem dizer o **Almox** (Almox.aqua).
- **Mudanças pequenas e revisáveis.** Não reescreva arquivos inteiros sem necessidade.
- **Não mexer no Almox** (repositório `andersonx553-beep/Almox.aqua`, Firebase `almox-aqua`, endereço na Cloudflare). Ele é o sistema em produção do Aqua Ville. Serve só de referência.
- **Uso sem internet** é implementação futura. Não proponha nem levante o assunto sem ele pedir.

## Regras de produto (sempre)

- **Visual profissional e confiável.** Azul-marinho escuro com preto, tema claro e tema escuro. **Nunca use emojis na interface.** Ícones de traço 24×24 (`stroke="currentColor"`), um estilo só.
- **Marca:** a logo do SCAE fica **fixa no código**, na tela de login, no rodapé do menu e no rodapé dos documentos. A **logo e o nome da empresa cliente** são editáveis pelo administrador dela, no **Perfil da empresa**, e aparecem no menu, no topo, nos comprovantes, no histórico, nas cotações e em todos os documentos.
- **Três telas iguais:** PC, celular e o futuro .exe. Teste em **1366×900** e **390×844**. A página nunca rola para os lados.
- **Sem dependência de IA:** o sistema funciona sem IA. Agentes e automações entram como extras (avisos, relatórios), nunca como peça de que o estoque dependa.
- **Nada se apaga em registro operacional.** Saída errada vira estorno; saldo errado vira ajuste com motivo; documento assinado nunca é editado.

## Onde fica o projeto

A pasta oficial do SCAE é **`C:\scae`**, desde 18/11/2026. Ela saiu de `Desktop\scae.almox\SCAE` porque o `mda` (ferramenta do agente) não funciona em caminhos com espaço, e o usuário do Windows se chama "Iure Motos". A cópia antiga na Área de Trabalho não deve mais ser editada.

## GitHub, Cloudflare e Firebase

- **Repositório:** `andersonx553-beep/scae` (público). Antes se chamava `suprimo.html`; o código do Suprimo continua no histórico.
- **Site oficial: Cloudflare Pages, projeto `scae` → `https://scae.pages.dev`** (o protótipo fica em `/prototipo/scae`). Publica sozinho a cada merge na `main`, sem build, servindo a raiz do repositório. O GitHub Pages (`https://andersonx553-beep.github.io/scae/`) ainda está ligado. Na mesma conta da Cloudflare existe o Worker `almox-aquaville`, do Almox: **não mexer**.
- **Firebase:** projeto **SCAE**, de ID `suprimo-fb90d`. O ID veio do Suprimo e não pode ser trocado. **Não é o `almox-aqua`**, que é do Almox e nunca deve ser tocado. Plano Spark (gratuito). Login com Google ativado; os domínios `scae.pages.dev` e `andersonx553-beep.github.io` estão autorizados. **Domínio novo** precisa entrar em três lugares: Authentication → Domínios autorizados, a chave do reCAPTCHA e, se for o caso, a Cloudflare.
- **IA (Firebase AI Logic):** ativada com a Gemini Developer API (gratuita; o Google pode usar o conteúdo enviado). Protegida pelo **App Check** com o provedor **reCAPTCHA (v3, clássico)**. A chave pública do site está em `RECAPTCHA_SITE_KEY` no `scae.html`; a chave secreta fica só no console, no provedor "reCAPTCHA" do App Check. A chave é clássica: **não serve** para o provedor Fraud Defense (reCAPTCHA Enterprise). Em `localhost` o SCAE usa um token de depuração, que precisa estar cadastrado em App Check → scae → Gerenciar tokens de depuração (o deste PC é "PC de casa (localhost)").
- **Regras do Firestore:** ficam em `firestore.rules`. Só os e-mails da lista acessam `empresas/{id}/...`. Os dados antigos do Suprimo, em `users/...`, ficaram guardados. Para mudar as regras, edite o arquivo e publique igual em Firestore → Regras, no console.
- **Fluxo de mudanças:** criar um branch, commitar, abrir PR com o `gh` e fazer o merge só quando o Anderson aprovar. A Cloudflare e o GitHub Pages publicam a `main` sozinhos.

## Onde estamos (19/11/2026)

1. **Protótipo pronto e ligado à nuvem:** `prototipo/scae.html`. Desde 18/11/2026 é **o sistema do Almox inteiro adaptado para o SCAE**, num arquivo HTML único (cerca de 5,8 MB). Desde 19/11/2026 **sincroniza com o Firestore**, com login Google, quando aberto pelo site ou por um servidor local. Aberto por duplo clique ou com `?local` no endereço, usa só o `localStorage`. A ponte com o Firebase é o `<script type="module">` logo no começo do arquivo (cria `window.FB`). A sincronização é o objeto `Nuvem`. A lista de e-mails autorizados é `EMAILS_AUTORIZADOS`, que precisa ser igual à de `firestore.rules`. Tem várias empresas, com troca pelo topo do menu. Na nuvem, a lista de empresas também sincroniza: cada empresa é um documento `empresas/{id}` com o campo `nome` (função `SCAE_EMPRESAS.sincronizar()`). Já traz entrada por NF, cotações, ferramentas, fardamento, saída em vários destinos, backup e PDFs. A versão anterior (protótipo de telas feito do zero) está em `prototipo/versoes-antigas/`. Detalhes em `docs/prototipo.md`.
2. **Marca SCAE desenhada:** SVGs em `marca/`. Conceito em `docs/marca.md`.
3. **Arquitetura decidida no papel** (`docs/arquitetura.md`): um projeto Firebase no plano Blaze, multiempresa, front em TypeScript e automações em Python.
3a. **Leitura de orçamento com IA nas Cotações** (19/11/2026): na aba Propostas, o PDF ou a foto do orçamento vai para o Gemini (`SCAE_IA` e `CotIA` no `scae.html`), que devolve os dados e liga cada linha a um item da cotação. O resultado cai na mesma tela de conferência do leitor sem IA (`LeitorOrcamento`), que continua de reserva quando a IA falha ou não há internet. Nada é gravado sem a pessoa clicar em "Usar estes dados".
3b. **Agente de almoxarifado começado** em `agente/` (Managed Deep Agents, Python). Tem as instruções em `agente/instructions.md` e a ferramenta `agente/tools/leitor_orcamento.py`, com as mesmas regras de leitura do SCAE (testar com `testar_leitor.py`). Ainda não tem acesso aos dados do SCAE. Modelo: `google_genai:gemini-3.5-flash-lite`, plano grátis. As chaves ficam em `agente/.env`, que nunca vai para o GitHub. Nunca peça nem leia o valor das chaves.
4. **Próximos passos:** convites e papéis de cada pessoa por empresa (hoje só o Anderson entra); revisar o protótipo tela por tela, trocando os textos que ainda falam em "Almox"; testar os fluxos de ponta a ponta com a nuvem.

## Onde está cada coisa

| Caminho | O que é |
|---|---|
| `prototipo/scae.html` | Protótipo navegável. Abra no navegador. É de onde continuar. Arquivo grande: procure pelo nome da função em vez de ler inteiro |
| `prototipo/versoes-antigas/` | Cópias de segurança das versões anteriores do protótipo |
| `marca/` | Logo do SCAE em SVG: símbolo e versões horizontais para fundo claro e escuro |
| `docs/plano.md` | Plano por fases e decisões tomadas |
| `docs/arquitetura.md` | Linguagens, Firebase multiempresa, modelo de dados, regras de segurança, papéis |
| `docs/regras-de-negocio.md` | As regras herdadas do Almox: custo médio, reconhecimento de itens, conversão de embalagem, saída, estorno, cotações |
| `docs/prototipo.md` | Como o HTML está organizado, o que já faz e o que falta |
| `docs/marca.md` | Conceito da logo, cores e fontes |
| `docs/historico-da-conversa.md` | Resumo do que foi conversado e decidido, em ordem |
| `agente/` | Agente de almoxarifado (Python, `mda`). `agent.py` define o agente e `instructions.md` é o comportamento |

## Como rodar o agente

No painel de Terminal, sempre com estes três detalhes, que são contornos deste PC: o cache do uv fora do AppData, o caminho sem espaço e o `--no-reload`, porque o recarregamento derruba o servidor no Windows.

```powershell
$env:UV_CACHE_DIR = 'C:\curso\.uv-cache'; & 'C:\Users\Iure Motos\.local\bin\mda.exe' dev 'C:\scae\agente' --no-reload --no-browser
```

Para conversar com ele, use o Studio: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`. Depois de mudar `agent.py` ou `instructions.md`, pare o servidor e rode de novo. Não rode `mda deploy` sem o Anderson pedir.

## Como testar o protótipo

- Abra `prototipo/scae.html` no navegador (duplo clique) para o modo local. O navegador interno do Claude não abre arquivo do disco: sirva a pasta `prototipo/` com `python -m http.server 8765` e abra `http://localhost:8765/scae.html`, que usa a nuvem e pede login; acrescente `?local` para testar sem nuvem. Na nuvem, use a empresa de demonstração para testes e apague o que criar.
- Antes de mexer, guarde uma cópia em `prototipo/versoes-antigas/` com a data e o motivo no nome.
- Antes de entregar uma mudança, confira em 1366×900 e em 390×844, nos temas claro e escuro, sem rolagem lateral. Abra todas as rotas (`#painel`, `#entrada`, `#cotacoes`, `#produtos`, `#notas`, `#fornecedores`, `#ferramentas`, `#movimentos`, `#organizar`, `#dados`; pelo console, `go('rota')`) e faça uma saída, uma entrada pela nota de exemplo e uma aprovação de cotação, conferindo que não há erro no console.
