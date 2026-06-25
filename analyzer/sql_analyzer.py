import re

from analyzer.rules import RULES


PALAVRAS_PROIBIDAS = (
    "insert", "update", "delete", "drop", "alter", "truncate",
    "create", "grant", "revoke", "execute", "call", "copy", "merge",
)


def _remover_comentarios(sql):
    sql = re.sub(r"--.*", "", sql)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    return sql


def validar_select_seguro(sql):
    sql_limpo = _remover_comentarios(sql).strip().rstrip(";").strip()

    if not re.match(r"^select\b", sql_limpo, re.IGNORECASE):
        return False, "Apenas comandos SELECT sao permitidos."

    if ";" in sql_limpo:
        return False, "Multiplos comandos SQL na mesma query nao sao permitidos."

    padrao_proibido = r"\b(" + "|".join(PALAVRAS_PROIBIDAS) + r")\b"
    if re.search(padrao_proibido, sql_limpo, re.IGNORECASE):
        return False, "A query contem palavras-chave nao permitidas para esta ferramenta."

    return True, None


def analisar_query(sql):
    sql_sem_comentarios = _remover_comentarios(sql)

    achados = []
    for regra in RULES:
        achados.extend(regra(sql_sem_comentarios))

    return {
        "query": sql.strip(),
        "achados": achados,
        "total_problemas": len(achados),
    }


def analisar_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        sql = arquivo.read()
    return analisar_query(sql)


def explicar_plano(sql, conn):
    seguro, motivo = validar_select_seguro(sql)
    if not seguro:
        raise ValueError(motivo)

    cur = conn.cursor()
    cur.execute(f"EXPLAIN (FORMAT JSON, ANALYZE) {sql}")
    plano = cur.fetchone()[0][0]["Plan"]
    cur.close()

    return {
        "plano": plano,
        "seq_scans": _coletar_seq_scans(plano),
    }


def _coletar_seq_scans(node):
    encontrados = []
    if node.get("Node Type") == "Seq Scan":
        encontrados.append({
            "tabela": node.get("Relation Name"),
            "linhas_estimadas": int(round(node.get("Plan Rows", 0))),
            "linhas_reais": int(round(node.get("Actual Rows", 0))),
            "custo_total": round(node.get("Total Cost", 0), 2),
            "tempo_real_ms": round(node.get("Actual Total Time", 0), 2),
        })
    for filho in node.get("Plans", []):
        encontrados.extend(_coletar_seq_scans(filho))
    return encontrados
