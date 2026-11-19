# Arquitetura do SCAE

## Linguagens: o que vai em cada parte

| Parte | Linguagem / serviço | Por quê |
|---|---|---|
| Telas (PC, celular e .exe) | **TypeScript** | O navegador só roda JavaScript. TypeScript é o JavaScript com tipos: o editor avisa do erro antes de o sistema ir para o ar. É o padrão atual para sistemas web sérios |
| Login | **Firebase Auth** com Google | Mesmo esquema do Almox, que já funciona |
| Banco | **Firestore** | Tempo real entre aparelhos e transações para o saldo |
| Arquivos (logos e, no futuro, fotos) | **Firebase Storage** | Liberado pelo plano Blaze |
| Servidor e automações | **Python** nas **Cloud Functions** do Firebase | Python é a melhor linguagem para automações, integrações e IA |
| Agente (futuro) | **Python** | É a linguagem com mais ferramentas para agentes. Sempre opcional |

**Por que não tudo em Python?** O Python não roda dentro do navegador. A tela sempre vai ser JavaScript/TypeScript. JavaScript não está desatualizado: é a base de todo sistema web hoje (Gmail, Bling, Conta Azul).

## Multiempresa (multi-tenant)

**Ideia central:** um código, um endereço e um banco de dados. Cada empresa tem uma "gaveta" e só enxerga a dela.

```
empresas/{empresaId}                      dados da empresa: nome, nomeCurto, cnpj, endereco, cidade, telefone,
                                          logoUrl (Storage), status ('ativa' | 'suspensa'), criadaEm, plano
empresas/{empresaId}/membros/{email}      papel: 'administrador' | 'operador' | 'consulta'
empresas/{empresaId}/produtos/{id}
empresas/{empresaId}/movimentos/{id}
empresas/{empresaId}/operacoesSaida/{id}
empresas/{empresaId}/notas/{id}
empresas/{empresaId}/fornecedores/{id}
empresas/{empresaId}/cotacoes/{id}
empresas/{empresaId}/grupos/{id}, destinos/{id}, funcionarios/{id}
empresas/{empresaId}/config/contadores    P0001, S-00001, COT-0001 (em transação)
usuarios/{uid}                            email, nome, empresas: { [empresaId]: papel }, dono: bool
Storage: empresas/{empresaId}/logo.png
```

O Almox já usa o mesmo formato com uma gaveta fixa (`condominios/aquaville/...`). No SCAE a gaveta vem do usuário logado.

### Entrada de uma pessoa
1. Ela entra com o Google no endereço único do SCAE.
2. O sistema lê `usuarios/{uid}` e vê de quais empresas ela participa.
3. Se for uma empresa só, abre direto. Se forem várias, pergunta qual. O dono do SCAE vê todas.
4. A tela carrega a logo e o nome da empresa e mostra os menus conforme o papel.

### Empresa nova
1. O dono do SCAE cria a empresa no painel dele e informa o e-mail do responsável. Uma Cloud Function cria a empresa e o convite.
2. O responsável entra, envia a logo e preenche nome e CNPJ no Perfil da empresa.
3. Ele convida a equipe por e-mail e escolhe o papel de cada um.

### Papéis

| Papel | Pode |
|---|---|
| Dono do SCAE | Tudo em todas as empresas; criar, suspender e reativar empresas |
| Administrador | Tudo na própria empresa, inclusive Perfil da empresa e quem acessa |
| Operador | Lançar entradas, saídas, ajustes e cotações; cadastrar produtos e fornecedores |
| Consulta | Só ver |

Empresa suspensa: todos os membros ficam só com leitura.

## Segurança (o ponto mais importante)

- A separação entre empresas é garantida pelas **regras do Firestore e do Storage**, não pela tela. Esboço:

```
match /empresas/{e}/{doc=**} {
  allow read:  if membro(e) || dono();
  allow write: if (papel(e) in ['administrador','operador'] && ativa(e)) || dono();
}
match /empresas/{e} {            // perfil da empresa
  allow update: if (papel(e) == 'administrador' && ativa(e)) || dono();
}
```

- Testes automáticos das regras no **emulador do Firebase**, incluindo tentativas de ler e gravar na empresa vizinha. Um vazamento entre clientes é o pior erro possível (LGPD).
- Registros assinados, operações de saída e notas nunca são apagados: só estorno ou cancelamento com motivo, como no Almox.
- O nome digitado ("lançado por") é declaratório; a identidade verificada é a conta Google (`contaLogin`, `usuarioUid`). Guardar as duas.

## Custos (plano Blaze)

- Paga pelo uso. Para poucas empresas pequenas, o custo fica perto de zero.
- **Configurar alerta de orçamento** no Google Cloud desde o primeiro dia.
- Carregar movimentações por período (como o Almox faz com 90 dias) para economizar leituras.

## Hospedagem

- Opções: **Cloudflare** (o Almox já publica lá) ou **Firebase Hosting**. A decidir.
- Domínio próprio quando for vender. Adicionar o domínio em *Authorized domains* do Firebase Auth.
