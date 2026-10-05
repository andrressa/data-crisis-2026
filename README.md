# DATA CRISIS 2026 — Back-end público

## Rodar localmente

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

- `/` — página pública dos alunos
- `/docs` — documentação da API
- `/admin` — painel da professora

## Comunicados

1. **Nova remessa**: libera `novos_dados.csv`.
2. **Dados corrompidos**: a coluna `temperatura` deve ser desconsiderada.
3. **Substituição de controladores**: existe uma grandeza numérica em escala diferente na nova remessa e os alunos precisam descobrir qual é e como tratar.

## Gabarito do incidente 3 — somente professora

Parte de `carga_sistema` em `novos_dados.csv` foi gravada em escala 0–1, enquanto o histórico utiliza 0–100.

## Publicação

O projeto já inclui `render.yaml`, portanto está preparado para um Web Service Python no Render.
Defina/consulte a variável de ambiente `ADMIN_KEY` e utilize essa chave no painel `/admin`.

Observação: `state.json` fica no disco da instância. Em hospedagem com disco efêmero, um redeploy ou restart pode restaurar o nível dos comunicados para 0.
