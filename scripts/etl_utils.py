import os
import pandas as pd
from sqlalchemy import create_engine

def get_db_engine():
    """Crea la conexión usando variables de entorno inyectadas por Docker"""
    user = os.getenv('POSTGRES_USER', 'custom_user')
    password = os.getenv('POSTGRES_PASSWORD', 'secure_password')
    host = os.getenv('POSTGRES_HOST', 'custombikes_db_container')
    db = os.getenv('POSTGRES_DB', 'custombike')
    port = '5432'
    
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

def extract_top_technicians():
    """
    Lógica de negocio: Identifica técnicos destacados (refactor de queries.py)
    Retorna: DataFrame de Pandas
    """
    query = """
    WITH PedidosAnuales AS (
        SELECT 
            DATE_PART('month', f."fecha-solicitud-facturacion") AS Mes,
            COUNT(p.id_pedido) AS TotalPedidos
        FROM public."Pedido" p
        JOIN public."FechaLimite" f ON p.fecha = f.id_fecha
        WHERE DATE_PART('year', f."fecha-solicitud-facturacion") = 2024
        GROUP BY DATE_PART('month', f."fecha-solicitud-facturacion")
    ),
    PromedioMensual AS (
        SELECT AVG(TotalPedidos) AS Promedio FROM PedidosAnuales
    ),
    TecnicosPedidos AS (
        SELECT 
            t.persona AS PersonaID,
            COUNT(tp.pedido) AS TotalPedidosTecnico
        FROM public."TecnicoPedido" tp
        JOIN public."Tecnico" t ON tp.tecnico = t.id_tecnico
        JOIN public."Pedido" p ON tp.pedido = p.id_pedido
        JOIN public."FechaLimite" f ON p.fecha = f.id_fecha
        WHERE DATE_PART('year', f."fecha-solicitud-facturacion") = 2024
        GROUP BY t.persona
    )
    SELECT 
        per."PrimerNombre" AS Nombre,
        per."Apellido1" AS Apellido,
        tp.TotalPedidosTecnico AS TotalPedidos
    FROM TecnicosPedidos tp
    JOIN PromedioMensual pm ON tp.TotalPedidosTecnico > pm.Promedio
    JOIN public."Persona" per ON tp.PersonaID = per.id_persona
    ORDER BY TotalPedidos DESC;
    """
    
    engine = get_db_engine()
    return pd.read_sql(query, engine)