from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from pathlib import Path
import json
import os

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
STATE_FILE = BASE / "state.json"
ADMIN_KEY = os.getenv("ADMIN_KEY", "troque-esta-chave")

app = FastAPI(
    title="DATA CRISIS 2026 — Operação Sinal Fraco",
    version="1.0.0",
    description="API pública do hackathon de Data Science da cidade fictícia de Nova Aurora.",
)

CIDADE = {
    "nome": "Nova Aurora",
    "estado": "Rio de Janeiro",
    "populacao": 318420,
    "descricao": (
        "Nova Aurora opera uma rede integrada de sensores em hospitais, energia, "
        "abastecimento de água, trânsito e telecomunicações. Nas últimas semanas, "
        "a Central Integrada de Operações registrou falhas inesperadas em unidades "
        "que, em alguns casos, pareciam operar normalmente poucas horas antes."
    ),
    "missao": (
        "Usar os dados operacionais para identificar unidades com maior risco de falha "
        "e apoiar a priorização das equipes de manutenção."
    ),
}

COMUNICADOS = [
    {
        "id": 1,
        "titulo": "Nova remessa de dados",
        "texto": (
            "A Central informa que uma nova remessa de dados operacionais foi recebida. "
            "Os novos registros deverão ser analisados e considerados na continuidade "
            "da investigação e da modelagem."
        ),
    },
    {
        "id": 2,
        "titulo": "Dados corrompidos",
        "texto": (
            "Após verificação técnica, foi confirmado um problema no processo de coleta "
            "da variável temperatura. Os valores registrados nessa coluna não podem mais "
            "ser considerados confiáveis. A partir deste comunicado, a variável temperatura "
            "deverá ser desconsiderada nas análises e nos modelos."
        ),
    },
    {
        "id": 3,
        "titulo": "Substituição de controladores",
        "texto": (
            "A equipe de campo confirmou que uma parte dos controladores das unidades presentes "
            "na nova remessa foi substituída recentemente. Há indícios de que pelo menos uma "
            "grandeza numérica passou a ser transmitida em uma escala diferente do padrão histórico. "
            "Não existe uma lista confiável das unidades afetadas, e a Central ainda não identificou "
            "qual campo sofreu a alteração. As equipes deverão investigar os dados e decidir como "
            "tratar o problema antes da versão final do modelo."
        ),
    },
]


def read_state():
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps({"nivel": 0}), encoding="utf-8")
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"nivel": 0}


def write_state(nivel: int):
    STATE_FILE.write_text(json.dumps({"nivel": nivel}), encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
def home():
    nivel = read_state()["nivel"]
    cards = "".join(
        f"<div class='card'><span class='badge'>COMUNICADO {c['id']}</span><h3>{c['titulo']}</h3><p>{c['texto']}</p></div>"
        for c in COMUNICADOS[:nivel]
    )
    if not cards:
        cards = "<div class='card muted'><h3>Nenhum comunicado extraordinário</h3><p>A operação segue com a base inicial.</p></div>"
    novo = "<a class='button secondary' href='/dados/novos.csv'>Baixar nova remessa</a>" if nivel >= 1 else ""

    return f"""
<!doctype html>
<html lang='pt-BR'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>DATA CRISIS 2026</title>
<style>
:root {{--bg:#09111f;--panel:#121d2d;--text:#edf4ff;--muted:#a9b7ca;--accent:#48a7ff;--border:#26364b;--warn:#ffd166}}
* {{box-sizing:border-box}}
body {{margin:0;background:var(--bg);color:var(--text);font-family:Arial,sans-serif;line-height:1.55}}
.hero {{padding:72px 8vw 56px;background:linear-gradient(135deg,#0c1728,#142c47)}}
.kicker {{letter-spacing:.16em;text-transform:uppercase;color:#75bdff;font-size:.8rem;font-weight:700}}
h1 {{font-size:clamp(2.4rem,6vw,5rem);margin:.2rem 0}}
.subtitle {{font-size:1.25rem;max-width:780px;color:#cfdaea}}
main {{max-width:1180px;margin:auto;padding:36px 24px 70px}}
.grid {{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}
.card {{background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:22px}}
.muted {{color:var(--muted)}}
.badge {{font-size:.72rem;padding:5px 8px;border-radius:99px;background:#233c57;color:#bfe1ff;font-weight:700}}
.button {{display:inline-block;margin:8px 8px 8px 0;padding:12px 16px;border-radius:10px;background:var(--accent);color:#05101c;text-decoration:none;font-weight:800}}
.secondary {{background:#dbeeff}}
.section {{margin-top:34px}}
.notice {{border-left:4px solid var(--warn)}}
footer {{color:var(--muted);margin-top:40px;border-top:1px solid var(--border);padding-top:24px}}
</style>
</head>
<body>
<section class='hero'>
  <div class='kicker'>Hackathon de Data Science</div>
  <h1>DATA CRISIS 2026</h1>
  <div class='subtitle'><strong>Operação Sinal Fraco.</strong> Vocês integram a equipe de Data Science da Central Integrada de Operações de Nova Aurora.</div>
</section>
<main>
  <section class='grid'>
    <div class='card'><h3>Nova Aurora</h3><p>{CIDADE['descricao']}</p></div>
    <div class='card'><h3>Missão</h3><p>{CIDADE['missao']}</p></div>
    <div class='card notice'><h3>Regra operacional</h3><p>Os dados e as condições do problema podem mudar ao longo da atividade. Toda alteração metodológica deverá ser justificada.</p></div>
  </section>
  <section class='section'>
    <h2>Dados disponíveis</h2>
    <p>Comecem pela base histórica. Novos recursos podem ser liberados durante a operação.</p>
    <a class='button' href='/dados/iniciais.csv'>Baixar dados iniciais</a>
    {novo}
    <a class='button secondary' href='/docs'>Documentação da API</a>
  </section>
  <section class='section'>
    <h2>Comunicados da Central</h2>
    <div class='grid'>{cards}</div>
  </section>
  <section class='section card'>
    <h2>Problema</h2>
    <p>Construam uma solução capaz de estimar o risco de falha de uma unidade a partir dos dados disponíveis. Não existe garantia de que todos os registros, variáveis ou padrões permaneçam válidos até o encerramento da operação.</p>
    <p><strong>A pergunta final é:</strong> em quais unidades a cidade deveria concentrar suas equipes de manutenção primeiro, e por quê?</p>
  </section>
  <footer>Nova Aurora é uma cidade fictícia criada exclusivamente para fins educacionais.</footer>
</main>
</body>
</html>
"""


@app.get("/api/cidade")
def cidade():
    return CIDADE


@app.get("/api/situacao")
def situacao():
    nivel = read_state()["nivel"]
    return {
        "hackathon": "DATA CRISIS 2026",
        "operacao": "Sinal Fraco",
        "cidade": CIDADE,
        "comunicados_liberados": COMUNICADOS[:nivel],
        "recursos": {
            "dados_iniciais": "/dados/iniciais.csv",
            "novos_dados": "/dados/novos.csv" if nivel >= 1 else None,
        },
    }


@app.get("/api/comunicados")
def comunicados():
    nivel = read_state()["nivel"]
    return {"nivel": nivel, "comunicados": COMUNICADOS[:nivel]}


@app.get("/dados/iniciais.csv")
def dados_iniciais():
    return FileResponse(DATA / "dados_iniciais.csv", filename="dados_iniciais.csv", media_type="text/csv")


@app.get("/dados/novos.csv")
def dados_novos():
    if read_state()["nivel"] < 1:
        raise HTTPException(status_code=403, detail="A nova remessa ainda não foi liberada.")
    return FileResponse(DATA / "novos_dados.csv", filename="novos_dados.csv", media_type="text/csv")


class Nivel(BaseModel):
    nivel: int


@app.post("/admin/liberar")
def liberar(payload: Nivel, x_admin_key: str | None = Header(default=None)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Chave administrativa inválida.")
    if payload.nivel not in (0, 1, 2, 3):
        raise HTTPException(status_code=400, detail="O nível deve ser 0, 1, 2 ou 3.")
    write_state(payload.nivel)
    return {"status": "ok", "nivel": payload.nivel, "comunicados_visiveis": COMUNICADOS[:payload.nivel]}


@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    nivel = read_state()["nivel"]
    return f"""
<!doctype html>
<html lang='pt-BR'>
<head><meta charset='utf-8'><title>Controle — DATA CRISIS 2026</title>
<style>body{{font-family:Arial,sans-serif;max-width:720px;margin:40px auto;padding:20px}}button,input{{padding:12px;margin:6px;font-size:16px}}.box{{padding:20px;border:1px solid #ccc;border-radius:12px}}</style></head>
<body>
<h1>Controle da professora</h1>
<div class='box'>
<p>Nível atual: <strong id='nivel'>{nivel}</strong></p>
<input id='key' type='password' placeholder='ADMIN_KEY'>
<div>
<button onclick='go(0)'>Reiniciar</button>
<button onclick='go(1)'>Liberar comunicado 1</button>
<button onclick='go(2)'>Liberar comunicado 2</button>
<button onclick='go(3)'>Liberar comunicado 3</button>
</div>
<pre id='out'></pre>
</div>
<script>
async function go(n) {{
  const r = await fetch('/admin/liberar', {{
    method: 'POST',
    headers: {{'Content-Type':'application/json','X-Admin-Key':document.getElementById('key').value}},
    body: JSON.stringify({{nivel:n}})
  }});
  const d = await r.json();
  document.getElementById('out').textContent = JSON.stringify(d,null,2);
  if (r.ok) document.getElementById('nivel').textContent = n;
}}
</script>
</body></html>
"""
