from analyzer.rules import (
    rule_function_on_column,
    rule_leading_wildcard_like,
    rule_missing_where,
    rule_or_in_where,
    rule_select_star,
)


def test_select_star_detecta_problema():
    achados = rule_select_star("SELECT * FROM performance_tests.pessoa_fisica")
    assert len(achados) == 1
    assert achados[0].rule_id == "SELECT_STAR"


def test_select_star_nao_aciona_com_colunas_explicitas():
    achados = rule_select_star("SELECT cd_pessoa_fisica, ds_nome FROM performance_tests.pessoa_fisica")
    assert achados == []


def test_leading_wildcard_like_detecta_problema():
    sql = "SELECT ds_nome FROM performance_tests.pessoa_fisica WHERE ds_nome LIKE '%Silva%'"
    achados = rule_leading_wildcard_like(sql)
    assert len(achados) == 1
    assert achados[0].rule_id == "LEADING_WILDCARD_LIKE"


def test_leading_wildcard_like_nao_aciona_sem_wildcard_inicial():
    sql = "SELECT ds_nome FROM performance_tests.pessoa_fisica WHERE ds_nome LIKE 'Silva%'"
    assert rule_leading_wildcard_like(sql) == []


def test_function_on_column_detecta_problema():
    sql = "SELECT ds_nome FROM performance_tests.pessoa_fisica WHERE UPPER(cd_cpf) = '12345678901'"
    achados = rule_function_on_column(sql)
    assert len(achados) == 1
    assert achados[0].rule_id == "FUNCTION_ON_COLUMN"


def test_function_on_column_nao_aciona_sem_funcao():
    sql = "SELECT ds_nome FROM performance_tests.pessoa_fisica WHERE cd_cpf = '12345678901'"
    assert rule_function_on_column(sql) == []


def test_missing_where_detecta_problema():
    achados = rule_missing_where("SELECT * FROM performance_tests.pessoa_fisica")
    assert len(achados) == 1
    assert achados[0].rule_id == "MISSING_WHERE"


def test_missing_where_nao_aciona_com_where():
    sql = "SELECT * FROM performance_tests.pessoa_fisica WHERE cd_pessoa_fisica = 1"
    assert rule_missing_where(sql) == []


def test_or_in_where_detecta_problema():
    sql = "SELECT * FROM performance_tests.pessoa_fisica WHERE cd_cpf = '1' OR cd_cpf = '2'"
    achados = rule_or_in_where(sql)
    assert len(achados) == 1
    assert achados[0].rule_id == "OR_IN_WHERE"


def test_or_in_where_nao_aciona_sem_or():
    sql = "SELECT * FROM performance_tests.pessoa_fisica WHERE cd_cpf = '1' AND ds_nome = 'a'"
    assert rule_or_in_where(sql) == []
