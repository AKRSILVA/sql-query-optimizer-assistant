import re
from dataclasses import dataclass


@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    suggestion: str


def rule_select_star(sql):
    if re.search(r"select\s+\*", sql, re.IGNORECASE):
        return [Finding(
            rule_id="SELECT_STAR",
            severity="MEDIA",
            message="Uso de SELECT * traz todas as colunas da tabela, mesmo as que nao sao usadas.",
            suggestion="Liste explicitamente apenas as colunas necessarias.",
        )]
    return []


def rule_leading_wildcard_like(sql):
    if re.search(r"like\s+'%", sql, re.IGNORECASE):
        return [Finding(
            rule_id="LEADING_WILDCARD_LIKE",
            severity="ALTA",
            message="LIKE com wildcard no inicio ('%termo') impede o uso de indices B-tree.",
            suggestion="Considere um indice GIN/trigram (extensao pg_trgm) ou busca full-text.",
        )]
    return []


def rule_function_on_column(sql):
    padrao = r"where\s+.*?\b(upper|lower|date|trim|cast)\s*\("
    if re.search(padrao, sql, re.IGNORECASE | re.DOTALL):
        return [Finding(
            rule_id="FUNCTION_ON_COLUMN",
            severity="ALTA",
            message="Uso de funcao sobre uma coluna no WHERE impede o uso de indice normal na coluna.",
            suggestion="Crie um indice de expressao (CREATE INDEX ON tabela (FUNCAO(coluna))) ou normalize o dado.",
        )]
    return []


def rule_missing_where(sql):
    tem_select = re.search(r"\bselect\b", sql, re.IGNORECASE)
    tem_where = re.search(r"\bwhere\b", sql, re.IGNORECASE)
    if tem_select and not tem_where:
        return [Finding(
            rule_id="MISSING_WHERE",
            severity="MEDIA",
            message="SELECT sem clausula WHERE forca a leitura completa da tabela (seq scan).",
            suggestion="Adicione uma condicao WHERE seletiva, caso nao seja intencional ler a tabela inteira.",
        )]
    return []


def rule_or_in_where(sql):
    trecho_where = re.search(r"where\s+(.*?)(?:order by|group by|limit|;|$)", sql, re.IGNORECASE | re.DOTALL)
    if trecho_where and re.search(r"\bor\b", trecho_where.group(1), re.IGNORECASE):
        return [Finding(
            rule_id="OR_IN_WHERE",
            severity="BAIXA",
            message="Condicoes OR no WHERE podem impedir o uso eficiente de indices compostos.",
            suggestion="Avalie reescrever como UNION de consultas indexadas, se a tabela for grande.",
        )]
    return []


RULES = [
    rule_select_star,
    rule_leading_wildcard_like,
    rule_function_on_column,
    rule_missing_where,
    rule_or_in_where,
]
