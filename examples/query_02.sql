-- Problema: LIKE com wildcard no inicio impede uso de indice B-tree
SELECT cd_pessoa_fisica, ds_nome
FROM performance_tests.pessoa_fisica
WHERE ds_nome LIKE '%Silva%';
