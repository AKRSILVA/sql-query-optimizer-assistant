-- Problema: funcao sobre a coluna indexada (cd_cpf) impede o uso do idx_pessoa_cpf
SELECT cd_pessoa_fisica, ds_nome
FROM performance_tests.pessoa_fisica
WHERE UPPER(cd_cpf) = '12345678901';
