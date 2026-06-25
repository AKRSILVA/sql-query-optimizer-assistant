import argparse
import random
import re

from faker import Faker

from database.connection import get_connection

fake = Faker("pt_BR")

BATCH_SIZE = 10_000


def gerar_cpf_unico(cpfs_usados):
    while True:
        cpf = re.sub(r"\D", "", fake.cpf())[:11]
        if cpf not in cpfs_usados:
            cpfs_usados.add(cpf)
            return cpf


def gerar_telefone():
    ddd = random.randint(11, 99)
    numero = random.randint(900_000_000, 999_999_999)
    return f"55{ddd}{numero}"


def copiar_pessoas(cur, lote, cpfs_usados):
    pessoas = []
    for _ in range(lote):
        nome = fake.name()
        nome_social = fake.first_name() if random.random() < 0.3 else None
        cpf = gerar_cpf_unico(cpfs_usados)
        anotacoes = fake.sentence(nb_words=5)[:50] if random.random() < 0.2 else None
        pessoas.append((nome, nome_social, cpf, anotacoes))

    with cur.copy(
        "COPY performance_tests.pessoa_fisica "
        "(ds_nome, ds_nome_social, cd_cpf, ds_anotacoes) FROM STDIN"
    ) as copy:
        for row in pessoas:
            copy.write_row(row)

    cpfs_lote = [p[2] for p in pessoas]
    cur.execute(
        "SELECT cd_pessoa_fisica FROM performance_tests.pessoa_fisica "
        "WHERE cd_cpf = ANY(%s)",
        (cpfs_lote,),
    )
    return [row[0] for row in cur.fetchall()]


def copiar_filhos(cur, ids_pessoas):
    with cur.copy(
        "COPY performance_tests.pessoa_fisica_email "
        "(cd_pessoa_fisica, ds_email) FROM STDIN"
    ) as copy:
        for pessoa_id in ids_pessoas:
            for _ in range(random.randint(1, 3)):
                copy.write_row((pessoa_id, fake.email()))

    with cur.copy(
        "COPY performance_tests.pessoa_fisica_telefone "
        "(cd_pessoa_fisica, cd_telefone) FROM STDIN"
    ) as copy:
        for pessoa_id in ids_pessoas:
            for _ in range(random.randint(1, 3)):
                copy.write_row((pessoa_id, gerar_telefone()))

    with cur.copy(
        "COPY performance_tests.pessoa_fisica_endereco "
        "(cd_pessoa_fisica, ds_endereco, ds_cidade, ds_estado, cd_cep) FROM STDIN"
    ) as copy:
        for pessoa_id in ids_pessoas:
            for _ in range(random.randint(0, 2)):
                copy.write_row((
                    pessoa_id,
                    fake.street_address()[:200],
                    fake.city()[:100],
                    fake.estado_sigla(),
                    re.sub(r"\D", "", fake.postcode())[:10],
                ))


def seed(total):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT cd_cpf FROM performance_tests.pessoa_fisica")
    cpfs_usados = {row[0] for row in cur.fetchall()}

    gerados = 0
    while gerados < total:
        lote = min(BATCH_SIZE, total - gerados)
        ids_pessoas = copiar_pessoas(cur, lote, cpfs_usados)
        copiar_filhos(cur, ids_pessoas)
        conn.commit()
        gerados += lote
        print(f"{gerados}/{total} pessoas inseridas")

    cur.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Popula o banco com dados sinteticos.")
    parser.add_argument("--count", type=int, default=500_000, help="Quantidade de pessoas a gerar")
    args = parser.parse_args()
    seed(args.count)
