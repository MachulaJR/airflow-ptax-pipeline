CREATE TABLE IF NOT EXISTS bronze.ptax_raw (
    moeda VARCHAR(10) NOT NULL,
    data_ref DATE NOT NULL,
    payload JSONB NOT NULL,
    qtd_registros INTEGER NOT NULL,
    source_url TEXT,
    arquivo_origem TEXT,
    run_id TEXT,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (moeda, data_ref) 
);