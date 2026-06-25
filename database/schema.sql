--
-- PostgreSQL database dump
--

\restrict ACLf5y7NHRLV5ULDOYo2dgUfuE6E5Wsad9CRVGFXghE02NrYKMZ30cqi9nzDdbp

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: performance_tests; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA performance_tests;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: pessoa_fisica; Type: TABLE; Schema: performance_tests; Owner: -
--

CREATE TABLE performance_tests.pessoa_fisica (
    cd_pessoa_fisica integer NOT NULL,
    ds_nome character varying(100) NOT NULL,
    ds_nome_social character varying(100),
    cd_cpf character varying(11) NOT NULL,
    ds_anotacoes character varying(50),
    CONSTRAINT chk_cpf_tamanho CHECK ((length((cd_cpf)::text) = 11))
);


--
-- Name: pessoa_fisica_cd_pessoa_fisica_seq; Type: SEQUENCE; Schema: performance_tests; Owner: -
--

ALTER TABLE performance_tests.pessoa_fisica ALTER COLUMN cd_pessoa_fisica ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME performance_tests.pessoa_fisica_cd_pessoa_fisica_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pessoa_fisica_email; Type: TABLE; Schema: performance_tests; Owner: -
--

CREATE TABLE performance_tests.pessoa_fisica_email (
    cd_email_id integer NOT NULL,
    cd_pessoa_fisica integer NOT NULL,
    ds_email character varying(150) NOT NULL
);


--
-- Name: pessoa_fisica_email_cd_email_id_seq; Type: SEQUENCE; Schema: performance_tests; Owner: -
--

ALTER TABLE performance_tests.pessoa_fisica_email ALTER COLUMN cd_email_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME performance_tests.pessoa_fisica_email_cd_email_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pessoa_fisica_endereco; Type: TABLE; Schema: performance_tests; Owner: -
--

CREATE TABLE performance_tests.pessoa_fisica_endereco (
    cd_endereco_id integer NOT NULL,
    cd_pessoa_fisica integer NOT NULL,
    ds_endereco character varying(200) NOT NULL,
    ds_cidade character varying(100),
    ds_estado character varying(50),
    cd_cep character varying(10)
);


--
-- Name: pessoa_fisica_endereco_cd_endereco_id_seq; Type: SEQUENCE; Schema: performance_tests; Owner: -
--

ALTER TABLE performance_tests.pessoa_fisica_endereco ALTER COLUMN cd_endereco_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME performance_tests.pessoa_fisica_endereco_cd_endereco_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pessoa_fisica_telefone; Type: TABLE; Schema: performance_tests; Owner: -
--

CREATE TABLE performance_tests.pessoa_fisica_telefone (
    cd_telefone_id integer NOT NULL,
    cd_pessoa_fisica integer NOT NULL,
    cd_telefone character varying(13) NOT NULL,
    CONSTRAINT chk_tel_tamanho CHECK ((length((cd_telefone)::text) = 13))
);


--
-- Name: pessoa_fisica_telefone_cd_telefone_id_seq; Type: SEQUENCE; Schema: performance_tests; Owner: -
--

ALTER TABLE performance_tests.pessoa_fisica_telefone ALTER COLUMN cd_telefone_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME performance_tests.pessoa_fisica_telefone_cd_telefone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pessoa_fisica pessoa_fisica_cd_cpf_key; Type: CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica
    ADD CONSTRAINT pessoa_fisica_cd_cpf_key UNIQUE (cd_cpf);


--
-- Name: pessoa_fisica_email pessoa_fisica_email_pkey; Type: CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica_email
    ADD CONSTRAINT pessoa_fisica_email_pkey PRIMARY KEY (cd_email_id);


--
-- Name: pessoa_fisica_endereco pessoa_fisica_endereco_pkey; Type: CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica_endereco
    ADD CONSTRAINT pessoa_fisica_endereco_pkey PRIMARY KEY (cd_endereco_id);


--
-- Name: pessoa_fisica pessoa_fisica_pkey; Type: CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica
    ADD CONSTRAINT pessoa_fisica_pkey PRIMARY KEY (cd_pessoa_fisica);


--
-- Name: pessoa_fisica_telefone pessoa_fisica_telefone_pkey; Type: CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica_telefone
    ADD CONSTRAINT pessoa_fisica_telefone_pkey PRIMARY KEY (cd_telefone_id);


--
-- Name: idx_pessoa_cpf; Type: INDEX; Schema: performance_tests; Owner: -
--

CREATE INDEX idx_pessoa_cpf ON performance_tests.pessoa_fisica USING btree (cd_cpf);


--
-- Name: pessoa_fisica_email fk_email_pessoa; Type: FK CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica_email
    ADD CONSTRAINT fk_email_pessoa FOREIGN KEY (cd_pessoa_fisica) REFERENCES performance_tests.pessoa_fisica(cd_pessoa_fisica) ON DELETE CASCADE;


--
-- Name: pessoa_fisica_endereco fk_endereco_pessoa; Type: FK CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica_endereco
    ADD CONSTRAINT fk_endereco_pessoa FOREIGN KEY (cd_pessoa_fisica) REFERENCES performance_tests.pessoa_fisica(cd_pessoa_fisica) ON DELETE CASCADE;


--
-- Name: pessoa_fisica_telefone fk_tel_pessoa; Type: FK CONSTRAINT; Schema: performance_tests; Owner: -
--

ALTER TABLE ONLY performance_tests.pessoa_fisica_telefone
    ADD CONSTRAINT fk_tel_pessoa FOREIGN KEY (cd_pessoa_fisica) REFERENCES performance_tests.pessoa_fisica(cd_pessoa_fisica) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict ACLf5y7NHRLV5ULDOYo2dgUfuE6E5Wsad9CRVGFXghE02NrYKMZ30cqi9nzDdbp

