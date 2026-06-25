from analyzer.sql_analyzer import validar_select_seguro


def test_select_simples_e_permitido():
    seguro, motivo = validar_select_seguro("SELECT * FROM performance_tests.pessoa_fisica")
    assert seguro is True
    assert motivo is None


def test_select_com_comentario_e_permitido():
    sql = "-- comentario qualquer\nSELECT cd_pessoa_fisica FROM performance_tests.pessoa_fisica"
    seguro, _ = validar_select_seguro(sql)
    assert seguro is True


def test_insert_e_bloqueado():
    seguro, motivo = validar_select_seguro("INSERT INTO performance_tests.pessoa_fisica VALUES (1)")
    assert seguro is False
    assert motivo is not None


def test_drop_table_e_bloqueado():
    seguro, _ = validar_select_seguro("DROP TABLE performance_tests.pessoa_fisica")
    assert seguro is False


def test_delete_e_bloqueado():
    seguro, _ = validar_select_seguro("DELETE FROM performance_tests.pessoa_fisica")
    assert seguro is False


def test_multiplos_comandos_sao_bloqueados():
    sql = "SELECT 1; DROP TABLE performance_tests.pessoa_fisica;"
    seguro, _ = validar_select_seguro(sql)
    assert seguro is False


def test_palavra_proibida_dentro_de_select_e_bloqueada():
    sql = "SELECT * FROM performance_tests.pessoa_fisica WHERE ds_nome = (SELECT 'x'); DROP TABLE x"
    seguro, _ = validar_select_seguro(sql)
    assert seguro is False
