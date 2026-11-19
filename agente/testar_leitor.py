"""Testa a leitura de orçamentos com o Gemini.

Uso, na pasta agente:  uv run python testar_leitor.py caminho1.pdf caminho2.pdf
A chave GOOGLE_API_KEY vem do arquivo .env (nunca é mostrada).
"""

import json
import os
import sys
from pathlib import Path

for linha in Path(__file__).with_name(".env").read_text(encoding="utf-8").splitlines():
    linha = linha.strip()
    if linha and not linha.startswith("#") and "=" in linha:
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave, valor)

sys.path.insert(0, str(Path(__file__).parent))
from tools.leitor_orcamento import ler_orcamento_bytes  # noqa: E402

for caminho in sys.argv[1:]:
    tipo = "image/jpeg" if caminho.lower().endswith((".jpg", ".jpeg")) else "image/png" if caminho.lower().endswith(".png") else "application/pdf"
    print(f"===== {Path(caminho).name}")
    print(json.dumps(ler_orcamento_bytes(Path(caminho).read_bytes(), tipo), ensure_ascii=False, indent=2))
