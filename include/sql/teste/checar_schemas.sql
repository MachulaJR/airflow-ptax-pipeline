SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = ANY(%(schemas)s)
ORDER BY schema_name;