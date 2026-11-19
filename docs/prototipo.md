# Protótipo: `prototipo/scae.html`

Desde 18/11/2026 o protótipo é **o sistema do Almox inteiro adaptado para o SCAE**, num arquivo HTML único (cerca de 5,8 MB, porque leva junto as fontes, o gerador de PDF, o leitor de planilhas e o leitor de código de barras). Os dados ficam no navegador, sem servidor e sem Firebase.

A versão anterior, um protótipo de telas feito do zero (193 KB), ficou guardada em `prototipo/versoes-antigas/scae-prototipo-2026-11-17.html`, só como referência.

## Como funciona

- **Modo local, sem login.** O arquivo define `window.SCAE_LOCAL = true`. Com isso, `iniciarAcesso()` libera o sistema direto, sem tela de login e sem nuvem. O código de login do Almox (`telaLogin`, `FB.*`, `Nuvem`, `emailAutorizado`) continua no arquivo, desligado.
- **Várias empresas no mesmo navegador** (`SCAE_EMPRESAS`, no fim do arquivo). Começa com a "Empresa de demonstração". O botão da empresa, no topo do menu, troca de empresa ou cria uma nova. A separação é **só do navegador**: o acesso de verdade vai exigir login e regras no servidor (veja `arquitetura.md`).
- **Logo da empresa:** enviada em **Dados e backup → Identidade da empresa** (PNG ou JPG de até 5 MB, reduzida para no máximo 600 px). Aparece no menu e nos comprovantes.
- **Logo do SCAE:** embutida no arquivo. As constantes `LOGO_SCAE_CLARO` e `LOGO_SCAE_ESCURO` guardam o SVG da pasta `marca/`. O destaque do painel e o login usam a versão de texto branco, sobre a placa azul-marinho. A identificação do painel troca de versão conforme o tema. As logos do menu lateral, do celular e do topo são PNGs embutidos que vieram do Almox.
- **Chaves no `localStorage`:**

| Chave | O que guarda |
|---|---|
| `scae.empresas.v1` | Lista de empresas |
| `scae.empresa.ativa` | Empresa aberta |
| `scae.empresa.{id}.v1` | Todos os dados de uma empresa |
| `scae.theme` | Tema claro ou escuro |
| `scae.cam` | Preferência da câmera |

## Telas (rotas por `#`)

| Rota | Título na tela | O que faz |
|---|---|---|
| `#painel` | Painel | Indicadores, consumo por setor, vencimentos, últimos lançamentos. Sem produtos, mostra o destaque "Dê entrada no estoque direto da nota fiscal" |
| `#entrada` | Entrada de NF-e | XML (um ou vários), chave de acesso pela câmera ou digitada, lançamento manual, reconhecimento de itens, conferência e confirmação |
| `#cotacoes` | Cotações | Pedidos de preço, mapa comparativo e aprovação |
| `#produtos` | Estoque | Produtos, saldos, grupos e locais. Ficha, ajuste, edição em lote, mesclar produtos, foto |
| `#notas` | Notas fiscais | Notas lançadas, comprovante de entrada e estorno |
| `#fornecedores` | Fornecedores | Cadastro (com consulta de CNPJ) e histórico de compras |
| `#ferramentas` | Relatórios | Funcionários, ferramentas (empréstimo e devolução com assinatura), fardamento e consultas |
| `#movimentos` | Histórico | Entradas, saídas (inclusive em vários destinos), ajustes e estornos |
| `#organizar` | Grupos e locais | Grupos, subgrupos, locais de guarda e setores |
| `#dados` | Dados e backup | Identificação, identidade da empresa, preferências, backup, exportações e importação de saldo |

## Bibliotecas embutidas

jsPDF (comprovantes e relatórios em PDF, com as fontes DejaVu), SheetJS/XLSX (planilhas) e ZXing (leitura de código de barras e da chave da NF pela câmera).

## Como testar

O navegador interno do Claude não abre o arquivo direto do disco. Sirva a pasta `prototipo/` com um servidor local (por exemplo `python -m http.server 8765`) e abra `http://localhost:8765/scae.html`. Também dá para abrir com duplo clique no navegador normal.

Passe por todas as rotas da tabela acima (a função `go('rota')` troca de tela pelo console), em **1366×900** e **390×844**, nos temas claro e escuro, conferindo que não há erro no console nem rolagem para os lados.

## Testado em 18/11/2026

- As 10 rotas abrem sem erro de JavaScript.
- Em 390 px de largura, nenhuma tela rola para os lados.
- A logo do SCAE aparece certa nos dois temas, sem buscar arquivo externo.

Ainda não foram testados nesta versão: lançar uma nota de ponta a ponta, registrar uma saída, aprovar uma cotação e gerar os PDFs.

## Pontos de atenção

- Ainda há textos herdados do Almox na interface. Exemplos: o subtítulo "· Almox" nos documentos de ferramentas e fardamento, a frase "Já existe um produto parecido no Almox" na importação e o aviso de login que fala em "acessar o Almox". Também há nomes internos como `marcaAlmox`, `DatasAlmox` e as classes `aquaville-*`. Vale trocar os textos visíveis para SCAE quando formos revisar as telas.
- O arquivo é grande e parte dele é código de biblioteca minificado. Para editar, procure pelo nome da função (`grep`) em vez de ler o arquivo inteiro.
