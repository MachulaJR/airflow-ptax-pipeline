INSERT INTO bronze.ptax_raw(
    moeda,
    data_ref,
    payload,
    qtd_registros,
    source_url,
    arquivo_origem,
    run_id
)
VALUES (
    %(moeda)s,
    %(data_ref)s,
    %(payload)s::jsonb,
    %(qtd_registros)s,
    %(source_url)s,
    %(arquivo_origem)s,
    %(run_id)s,
)
ON CONFLICT (moeda, data_ref) DO UPDATE SET
    payload = EXCLUDE.payload,
    qtd_registros = EXCLUDE.qtd_registros,
    source_url = EXCLUDE.source_url,
    arquivo_origem = EXCLUDE.arquivo_origem,
    run_id = EXCLUDE.run_id,
    ingested_at = now();