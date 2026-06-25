import glob

import streamlit as st

from analyzer.sql_analyzer import analisar_query, explicar_plano
from database.connection import get_connection

st.title("SQL Optimizer Assistant")

if st.button("Testar Conexao"):
    try:
        conn = get_connection()
        st.success("Conectado com sucesso!")
        conn.close()
    except Exception as e:
        st.error(str(e))

st.divider()
st.subheader("Analisar Query")

exemplos = sorted(glob.glob("examples/*.sql"))
exemplo_escolhido = st.selectbox(
    "Carregar um exemplo (opcional)",
    ["-- escrever manualmente --"] + exemplos,
)

texto_inicial = ""
if exemplo_escolhido != "-- escrever manualmente --":
    with open(exemplo_escolhido, "r", encoding="utf-8") as arquivo:
        texto_inicial = arquivo.read()

sql = st.text_area("Cole a query SQL aqui", value=texto_inicial, height=150)

SEVERIDADE_COR = {
    "ALTA": "🔴",
    "MEDIA": "🟠",
    "BAIXA": "🟡",
}

if st.button("Analisar"):
    if not sql.strip():
        st.warning("Cole uma query antes de analisar.")
    else:
        resultado = analisar_query(sql)

        st.markdown(f"**{resultado['total_problemas']} problema(s) encontrado(s)**")
        for achado in resultado["achados"]:
            icone = SEVERIDADE_COR.get(achado.severity, "⚪")
            with st.expander(f"{icone} [{achado.severity}] {achado.rule_id}"):
                st.write(achado.message)
                st.caption(f"Sugestao: {achado.suggestion}")

        st.markdown("**Plano de execucao real (EXPLAIN ANALYZE)**")
        try:
            conn = get_connection()
            sql_sem_ponto_virgula = resultado["query"].rstrip(";")
            plano = explicar_plano(sql_sem_ponto_virgula, conn)
            conn.close()

            if plano["seq_scans"]:
                st.warning("Seq Scan detectado nas seguintes tabelas:")
                seq_scans_formatado = [
                    {
                        **scan,
                        "custo_total": f"{scan['custo_total']:.2f}",
                        "tempo_real_ms": f"{scan['tempo_real_ms']:.2f}",
                    }
                    for scan in plano["seq_scans"]
                ]
                st.table(seq_scans_formatado)
            else:
                st.success("Nenhum Seq Scan detectado no plano de execucao.")

            with st.expander("Ver plano completo (JSON)"):
                st.json(plano["plano"])
        except ValueError as e:
            st.error(f"Query bloqueada: {e}")
        except Exception as e:
            st.error(f"Nao foi possivel executar EXPLAIN ANALYZE: {e}")
