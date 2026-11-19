# Regras de negócio herdadas do Almox

Regras que já funcionam no Almox (Aqua Ville) e que o SCAE mantém. O protótipo (`prototipo/scae.html`) já implementa as marcadas com **[protótipo]**.

## Estoque e custo médio [protótipo]

- Cada produto guarda `estoque` (saldo), `valorEstoque` (R$) e `custoMedio = valorEstoque / estoque`.
- **Entrada** soma quantidade e valor pelo custo da nota. Se o saldo estava negativo, a entrada absorve a diferença.
- **Saída** tira pelo custo médio atual.
- **Estorno** devolve pelo custo da saída original.
- **Ajuste** (inventário) soma ou tira a diferença pelo custo médio, sempre com **motivo** e **nome de quem contou**.
- Saldo negativo **não bloqueia**: aparece o alerta "Saldo negativo" para alguém conferir e ajustar.
- Todo movimento guarda `saldoAntes`, `saldo` (depois), `valor` (variação em R$), `lancadoPor` e a data.
- Na nuvem: saldo e valor somados com `increment()` e operações confirmadas em **transação** no servidor, para dois aparelhos lançarem ao mesmo tempo sem perder nada.
- Código do produto `P0001`… gerado por contador em transação.

## Entrada de NF-e [protótipo]

- Lê o **XML** da nota (`infNFe`): emitente, destinatário, itens (`cProd`, `cEAN`, `xProd`, `uCom`, `qCom`, `vUnCom`, `vProd`, frete, seguro, desconto e outros), total.
- **Avisos:** nota já lançada (pela chave), destinatário com CNPJ diferente do da empresa, fornecedor novo (cadastrado ao confirmar).
- Campo obrigatório **"Nome de quem deu a entrada"**.
- Nota estornada e relançada recebe um código próprio (`nf-<chave>-2`); a estornada nunca é sobrescrita.

### Reconhecimento dos itens (nessa ordem)
1. **Código do fornecedor** já usado antes (vínculo fornecedor + `cProd`): liga direto e lembra a conversão.
2. **EAN** (código de barras).
3. **Apelido**: nome já aprendido de uma nota anterior.
4. **Nome parecido** (nota de 0 a 100): **90 ou mais** liga sozinho; **60 a 89** aparece como sugestão; **abaixo de 60** vira produto novo, marcado para revisar.
- Todo item lançado grava o nome da nota como apelido do produto. É assim que o sistema aprende.

### Conversão de embalagem
- "Como vem 1 FD desta nota?": `1 FD = N UN`. O saldo entra em unidades, porque a saída é por unidade.
- Ordem: conversão **lembrada** no vínculo > **sugestão pela descrição** ("C/ 12", "CX 24", "12UN"; nunca confirma sozinha) > fator 1 com alerta.
- Entrada automática só com conversão lembrada e conferida.

## Saída [protótipo]

- Lista de itens + **Responsável pela retirada / Destino** (funcionários e destinos na mesma busca, com etiqueta do tipo) + data (hoje como padrão) + "lançado por" + observação.
- Passos: **itens e destino → revisão → comprovante**.
- Número `S-00001`. Comprovante com a **logo da empresa**, quem recebeu, quem entregou, itens, custo e espaço para assinatura.
- **Estorno** com motivo: devolve tudo, marca a saída como estornada e não apaga nada.
- No Almox também existe "Vários destinos" (cada item com o seu destinatário, uma saída por destinatário no mesmo lançamento) e a correção de saída com motivo. Ainda não estão no protótipo.

## Painel [protótipo]

- Valor em estoque, consumo em 30 dias (descontando estornos), entradas em 30 dias, itens abaixo do mínimo.
- Consumo por destino. Retirada de funcionário sem destino vai para a barra "Retiradas por funcionário".
- Saídas por dia e últimos lançamentos.

## Cotações [protótipo, versão simples]

- Número `COT-0001`. Itens do estoque ou fora dele. Propostas de fornecedores do cadastro ou de loja sem CNPJ.
- Mapa comparativo: menor preço de cada item em destaque, frete, total por fornecedor, proposta incompleta.
- Sugestão: menor total entre as propostas completas, e quanto economizaria dividindo a compra.
- Decisão: "Autorizado por" e "Registrado por"; aprovada trava; reabrir com motivo; marcar como comprada.
- No Almox há mais: preço por embalagem, frete grátis acima de um valor, validade da proposta, preço discrepante, envio da mensagem pelo WhatsApp, PDF do pedido de cotação e leitura do PDF do orçamento sem IA.

## Ainda não prototipado (existe no Almox)

- **Ferramentas e empréstimos:** patrimônio `FER-001`, retirada e devolução com **duas assinaturas** desenhadas na tela, cancelamento com motivo (nunca editar nem apagar).
- **Fardamento:** entrega com assinatura de quem recebe e baixa do estoque na mesma transação.
- **Importar saldo** do sistema antigo (CSV) e **desfazer importação**.
- **Importar funcionários e ferramentas** (CSV ou XLSX).
- **Conferir cadastros:** mesclar nomes repetidos sem reescrever registros antigos.
- **Backup completo** (exportar tudo em JSON).
- Atalhos de teclado (F2 busca, Ctrl+Enter confirma) e rascunhos por conta.
