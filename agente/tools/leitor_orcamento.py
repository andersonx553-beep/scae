"""Leitura de orçamentos (PDF ou foto) com o Gemini.

Devolve os dados no mesmo formato do leitor sem IA do SCAE (prototipo/scae.html,
LeitorOrcamento): fornecedor, CNPJ, contato, prazo, pagamento, validade, frete,
totais e itens. Nada é gravado aqui: o resultado vai para a tela de conferência
do SCAE, e quem confirma é sempre a pessoa.
"""

from __future__ import annotations

import os
from typing import Optional

from google import genai
from google.genai import types
from langchain_core.tools import tool
from pydantic import BaseModel, Field

MODELOS = ("gemini-3.5-flash", "gemini-3.5-flash-lite")


class ItemOrcamento(BaseModel):
    descricao: str = Field(description="Descrição do produto exatamente como no documento, sem o código interno do fornecedor")
    codigo: Optional[str] = Field(None, description="Código do produto no fornecedor, se houver")
    unidade: Optional[str] = Field(None, description="Unidade como aparece: UN, UNID, RL, CX, M, KG, L...")
    quantidade: float
    preco_unitario: float = Field(description="Preço unitário final, já com desconto, em reais")
    total: float = Field(description="Total da linha em reais")


class Orcamento(BaseModel):
    fornecedor: str = Field(description="Nome ou razão social do FORNECEDOR que emitiu o orçamento (nunca o cliente)")
    cnpj: Optional[str] = Field(None, description="CNPJ do fornecedor, formato 00.000.000/0000-00")
    telefone: Optional[str] = None
    vendedor: Optional[str] = Field(None, description="Nome do vendedor ou contato do fornecedor")
    numero: Optional[str] = Field(None, description="Número do orçamento ou da proposta")
    emissao: Optional[str] = Field(None, description="Data de emissão no formato AAAA-MM-DD")
    validade_texto: Optional[str] = Field(None, description="Validade como escrita no documento")
    validade_dias: Optional[int] = Field(None, description="Validade em dias, se der para saber")
    validade_uteis: bool = Field(False, description="True quando a validade for em dias úteis")
    prazo_entrega: Optional[str] = Field(None, description="Prazo ou disponibilidade de entrega, como escrito")
    pagamento: Optional[str] = Field(None, description="Condição de pagamento, como escrita")
    frete_valor: Optional[float] = Field(None, description="Valor do frete em reais; 0 só se o documento disser grátis, CIF ou incluso; vazio se o documento não falar de frete")
    frete_texto: Optional[str] = Field(None, description="Como o frete aparece: CIF, FOB, valor, cidade")
    subtotal: Optional[float] = None
    total: Optional[float] = Field(None, description="Total geral do orçamento em reais")
    itens: list[ItemOrcamento]
    observacoes: Optional[str] = None


INSTRUCOES = """Você lê orçamentos e propostas comerciais de fornecedores brasileiros para um almoxarifado.
Extraia os dados do documento anexo com precisão total. Regras:
- O fornecedor é quem EMITE o orçamento (cabeçalho, logo, CNPJ do emissor). O cliente (quem recebe) nunca é o fornecedor.
- Números no padrão brasileiro: 1.234,56 significa mil duzentos e trinta e quatro reais e cinquenta e seis centavos. Devolva como número (1234.56).
- Cada linha de item tem quantidade, preço unitário e total. Confira: quantidade x preço unitário deve dar o total da linha. Se houver desconto por item, use o preço já com desconto.
- Não invente nada. Campo que não está no documento fica vazio.
- Não inclua linhas de subtotal, frete, logística, impostos ou totais como itens."""


def ler_orcamento_bytes(conteudo: bytes, tipo: str = "application/pdf") -> dict:
    """Lê um orçamento (PDF, JPG ou PNG) e devolve os dados como dicionário."""
    cliente = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    ultimo_erro: Exception | None = None
    for modelo in MODELOS:
        try:
            resposta = cliente.models.generate_content(
                model=modelo,
                contents=[types.Part.from_bytes(data=conteudo, mime_type=tipo), "Extraia os dados deste orçamento."],
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCOES,
                    response_mime_type="application/json",
                    response_schema=Orcamento,
                    temperature=0,
                ),
            )
            dados = Orcamento.model_validate_json(resposta.text).model_dump()
            dados["modelo"] = modelo
            dados["conferencia"] = conferir(dados)
            return dados
        except Exception as erro:  # modelo sobrecarregado ou indisponível: tenta o próximo
            ultimo_erro = erro
    raise RuntimeError(f"Não foi possível ler o orçamento: {ultimo_erro}")


def conferir(dados: dict) -> dict:
    """Confere as contas do que foi lido, para a tela de conferência avisar o que não fecha."""
    problemas = []
    soma = 0.0
    for n, item in enumerate(dados.get("itens") or [], 1):
        calculado = round(item["quantidade"] * item["preco_unitario"], 2)
        soma += item["total"]
        if abs(calculado - item["total"]) > 0.05:
            problemas.append(f"Item {n}: {item['quantidade']} x {item['preco_unitario']} = {calculado}, mas o documento diz {item['total']}")
    soma = round(soma, 2)
    referencia = dados.get("subtotal") or dados.get("total")
    if referencia is not None and abs(referencia - soma) > 0.05 and abs((dados.get("total") or 0) - (soma + (dados.get("frete_valor") or 0))) > 0.05:
        problemas.append(f"Soma dos itens {soma} diferente do total do documento {referencia}")
    return {"soma_itens": soma, "confere": not problemas, "problemas": problemas}


@tool
def ler_orcamento(caminho_arquivo: str) -> dict:
    """Lê um orçamento de fornecedor (PDF, JPG ou PNG) e devolve fornecedor, CNPJ, prazo, pagamento, validade, frete, totais e itens."""
    tipo = "application/pdf"
    if caminho_arquivo.lower().endswith((".jpg", ".jpeg")):
        tipo = "image/jpeg"
    elif caminho_arquivo.lower().endswith(".png"):
        tipo = "image/png"
    with open(caminho_arquivo, "rb") as arquivo:
        return ler_orcamento_bytes(arquivo.read(), tipo)
