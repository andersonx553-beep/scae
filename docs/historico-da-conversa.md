# Histórico da conversa (17 e 18/11/2026)

Resumo, em ordem, do que foi pedido e decidido na sessão do Claude Code na nuvem que deu origem ao SCAE.

1. **CLAUDE.md do Almox corrigido (PR #39, integrado):** quem decide é o **Anderson** ("Rainara" era outra conta Claude dele). O uso sem internet ficou anotado como implementação futura, sem ser levantado em toda tarefa.
2. **Endereço do Almox:** o Anderson quis tirar "andersonx553" do endereço da Cloudflare e trocar o nome "Almox Aqua Ville" por um nome oficial. Escolheu **SCAE** (Sistema de Controle de Almoxarifado e Estoque) e o endereço `scae.almox.workers.dev`. O PR do Almox (#40, `chore/endereco-scae`) ficou **em rascunho**, sem merge. Para aplicar: Firebase Authorized domains, depois o subdomínio da conta Cloudflare para `almox`, depois renomear o Worker para `scae`, e só então o merge.
3. **Logo editável:** levantamento de onde o Almox usa logo e nome fixos (menu, topo, login, Painel, PDFs). O Anderson quer o nome e a logo da empresa editáveis em todo lugar que a empresa usa, e a logo do SCAE fixa.
4. **Mudança de rumo:** o Almox **não será alterado** agora, porque está em produção. Nasce o **SCAE**, um produto novo para vender a várias empresas, planejado do zero com base no que o Almox já faz.
5. **Firebase:** a recomendação foi um **projeto novo** no Blaze para o SCAE, sem mexer no do Almox, e **um projeto só para todas as empresas** (multiempresa), não um projeto por cliente. Foi explicado como sistemas como Bling e Omie fazem: gaveta por empresa, pessoas ligadas por e-mail com papel e regras do servidor garantindo a separação.
6. **Logo da empresa:** enviada pelo responsável no **Perfil da empresa**. Aparece no menu, no topo, nos comprovantes, no histórico e nas cotações. Planilhas sem logo e só se o cliente quiser.
7. **Protótipo em HTML:** o Anderson pediu o máximo do que o Almox entrega num HTML, sem banco de dados, em azul-marinho escuro com preto, tema claro e escuro, profissional e confiável. **A logo do SCAE é a prioridade.** O protótipo foi feito e testado.
8. **Linguagens:** a pergunta foi se JavaScript está desatualizado e se Python seria melhor. Resposta: JavaScript (TypeScript) é obrigatório na tela, porque é o que o navegador roda; Python fica nas automações, nas notificações e no agente.
9. **Ambiente:** o Anderson prefere continuar com o **Claude Code no PC dele**, com o VS Code e as pastas locais.
10. **Sem login por enquanto:** o protótipo passou a abrir direto por dentro do sistema, com "Trocar de empresa" e "Ver como".
11. **Este pacote:** ZIP com protótipo, marca e documentação, para continuar no PC.

## 18/11/2026, no PC de casa

12. **Repositório:** o Anderson quer o SCAE no repositório **"suprimo"** do GitHub, limpo e só com o SCAE, e autorizou apagar o que está lá. O GitHub CLI foi instalado no PC, mas o login e o envio ficaram para depois. Por enquanto o trabalho é na pasta local `Desktop\scae.almox`.
13. **Nova versão do protótipo:** o Anderson trouxe uma versão nova do `scae.html` (o sistema do Almox inteiro adaptado para o SCAE, cerca de 5,8 MB), que passou a ser o protótipo oficial. A versão anterior foi guardada em `prototipo/versoes-antigas/`.
14. **Logo do SCAE:** a versão nova procurava um arquivo `assets/img/scae-logo.png` que não existia. A logo passou a ficar embutida no HTML, a partir dos SVGs de `marca/`, com a versão certa para cada fundo e tema.
15. **Documentação:** `CLAUDE.md` e `docs/prototipo.md` foram atualizados para a versão nova.
16. **Pasta nova e agente:** o projeto passou para `C:\scae` (sem espaço no caminho) e ganhou o agente de almoxarifado em `agente/`.
17. **GitHub:** o repositório `suprimo.html` recebeu o SCAE no lugar do Suprimo (o código antigo continua no histórico). As 11 branches antigas foram apagadas.

## 19/11/2026

18. **Nomes:** o repositório virou `scae`. No Firebase, o projeto do Suprimo virou **SCAE** (nome do projeto, nome público e apelido do app). O ID `suprimo-fb90d` não pode ser trocado. O Almox (`almox-aqua`) não foi tocado.
19. **Sincronização:** o SCAE ganhou a ponte com o Firebase e passou a sincronizar com o Firestore, com login Google, em `empresas/{id}/...`. As regras novas foram publicadas (`firestore.rules`). Teste: um setor cadastrado pela tela chegou ao servidor em `empresas/demo/setores/...`.
20. **Lista de empresas na nuvem:** as empresas passaram a ficar em `empresas/{id}`, iguais em todos os aparelhos. Teste: uma empresa criada pela tela apareceu num "aparelho novo" (lista do navegador apagada); depois a empresa de teste foi apagada da nuvem.
21. **Leitura de orçamento com IA:** com dois orçamentos reais (Solução e Supramat), o leitor sem IA errou os itens de um e o fornecedor do outro; o Gemini acertou todos os campos e itens. Foi ativado o Firebase AI Logic (Gemini Developer API, gratuito) com App Check (reCAPTCHA Enterprise), e a leitura entrou na aba Propostas das Cotações, ligando cada linha ao item da cotação. Ajustes depois do teste: frete não informado fica "a confirmar" (não zero) e validade em dias úteis pula o fim de semana.
22. **Cloudflare:** o SCAE passou a ser publicado na Cloudflare Pages, em `scae.pages.dev`, ligado ao repositório. Domínio autorizado no Firebase e no reCAPTCHA.
