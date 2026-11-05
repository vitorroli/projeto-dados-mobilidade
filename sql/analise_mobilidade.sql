-- 1. Identificando as 3 rotas mais longas da cidade (Impacto direto em consumo de combustível e tempo de frota)
WITH RankingExtensao AS (
    SELECT 
        linha,
        sentido,
        db_extensao AS extensao_metros,
        ROUND(db_extensao / 1000.0, 2) AS extensao_km,
        RANK() OVER(ORDER BY db_extensao DESC) as rank_tamanho
    FROM dim_linhas_onibus
)
SELECT * 
FROM RankingExtensao 
WHERE rank_tamanho <= 3;

-- 2. Diferença de trajeto entre Ida e Volta 
SELECT 
    i.linha,
    i.db_extensao AS extensao_ida_metros,
    v.db_extensao AS extensao_volta_metros,
    ABS(i.db_extensao - v.db_extensao) AS diferenca_trajeto_metros
FROM dim_linhas_onibus i
JOIN dim_linhas_onibus v 
  ON i.linha = v.linha 
  AND i.sentido = 'Ida' 
  AND v.sentido = 'Volta'
ORDER BY diferenca_trajeto_metros DESC;