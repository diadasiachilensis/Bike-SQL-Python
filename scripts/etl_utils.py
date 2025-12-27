def consult_orders_by_customer_and_period(db, first_name, last_name):
    query = """
    SELECT 
        p."PrimerNombre" AS Nombre, 
        p."Apellido1" AS Apellido, 
        f."fecha-solicitud-facturacion" AS FechaSolicitud
    FROM 
        public."Persona" p
    JOIN 
        public."Cliente" c ON p.id_persona = c.persona
    JOIN 
        public."Pedido" pd ON c.id_cliente = pd.cliente
    JOIN 
        public."FechaLimite" f ON pd.fecha = f.id_fecha
    WHERE 
        LOWER(p."PrimerNombre") = %s AND LOWER(p."Apellido1") = %s;
    """
    return db.execute_query(query, (first_name, last_name))

def list_most_requested_components(db):
    query = """
    SELECT 
        c.tipo AS NombreComponente, 
        SUM(pc.cantidad) AS TotalSolicitado
    FROM 
        public."Componente" c
    JOIN 
        public."PedidoComponente" pc ON c.id_componente = pc.componente
    GROUP BY 
        c.tipo
    ORDER BY 
        TotalSolicitado DESC;
    """
    return db.execute_query(query)

def list_sold_bicycles_and_warranties(db):
    query = """
    SELECT 
        p.id_pedido AS IDPedido,
        g.detalle_garantia AS DetalleGarantia,
        g."años" AS AnhosGarantia
    FROM 
        public."Pedido" p
    JOIN 
        public."Garantia" g ON p.garantia = g.id_garantia;
    """
    return db.execute_query(query)

def list_top_technicians(db):
    query = """
    WITH PedidosAnuales AS (
        SELECT 
            DATE_PART('month', f."fecha-solicitud-facturacion") AS Mes,
            COUNT(p.id_pedido) AS TotalPedidos
        FROM 
            public."Pedido" p
        JOIN 
            public."FechaLimite" f ON p.fecha = f.id_fecha
        WHERE 
            DATE_PART('year', f."fecha-solicitud-facturacion") = 2024
        GROUP BY 
            DATE_PART('month', f."fecha-solicitud-facturacion")
    ),
    PromedioMensual AS (
        SELECT 
            AVG(TotalPedidos) AS Promedio
        FROM 
            PedidosAnuales
    ),
    TecnicosPedidos AS (
        SELECT 
            t.persona AS PersonaID,
            COUNT(tp.pedido) AS TotalPedidosTecnico
        FROM 
            public."TecnicoPedido" tp
        JOIN 
            public."Tecnico" t ON tp.tecnico = t.id_tecnico
        JOIN 
            public."Pedido" p ON tp.pedido = p.id_pedido
        JOIN 
            public."FechaLimite" f ON p.fecha = f.id_fecha
        WHERE 
            DATE_PART('year', f."fecha-solicitud-facturacion") = 2024
        GROUP BY 
            t.persona
    )
    SELECT 
        per."PrimerNombre" AS Nombre,
        per."Apellido1" AS Apellido,
        tp.TotalPedidosTecnico AS TotalPedidos
    FROM 
        TecnicosPedidos tp
    JOIN 
        PromedioMensual pm ON tp.TotalPedidosTecnico > pm.Promedio
    JOIN 
        public."Persona" per ON tp.PersonaID = per.id_persona
    ORDER BY 
        TotalPedidos DESC;
    """
    return db.execute_query(query)

def list_technicians_with_increase(db, year1, year2):
    query = """
    WITH PedidosPorAnho AS (
        SELECT 
            t.persona AS PersonaID,
            DATE_PART('year', f."fecha-solicitud-facturacion") AS Anho,
            COUNT(tp.pedido) AS TotalPedidos
        FROM 
            public."TecnicoPedido" tp
        JOIN 
            public."Tecnico" t ON tp.tecnico = t.id_tecnico
        JOIN 
            public."Pedido" p ON tp.pedido = p.id_pedido
        JOIN 
            public."FechaLimite" f ON p.fecha = f.id_fecha
        WHERE 
            DATE_PART('year', f."fecha-solicitud-facturacion") IN (%s, %s)
        GROUP BY 
            t.persona, DATE_PART('year', f."fecha-solicitud-facturacion")
    ),
    ComparacionPedidos AS (
        SELECT 
            p1.PersonaID,
            p1.TotalPedidos AS PedidosAnho1,
            p2.TotalPedidos AS PedidosAnho2
        FROM 
            PedidosPorAnho p1
        LEFT JOIN 
            PedidosPorAnho p2 ON p1.PersonaID = p2.PersonaID AND p2.Anho = %s
        WHERE 
            p1.Anho = %s
    ),
    TecnicosIncremento AS (
        SELECT 
            PersonaID
        FROM 
            ComparacionPedidos
        WHERE 
            PedidosAnho2 > PedidosAnho1
    )
    SELECT 
        per."PrimerNombre" AS Nombre,
        per."Apellido1" AS Apellido
    FROM 
        TecnicosIncremento ti
    JOIN 
        public."Persona" per ON ti.PersonaID = per.id_persona;
    """
    return db.execute_query(query, (year1, year2, year2, year1))

def get_component_usage_data(db):
    """
    Obtiene el tipo de componente y su cantidad total de uso en los pedidos.
    """
    query = """
    SELECT 
        c.tipo AS TipoComponente, 
        SUM(pc.cantidad) AS TotalCantidad
    FROM 
        public."Componente" c
    JOIN 
        public."PedidoComponente" pc ON c.id_componente = pc.componente
    GROUP BY 
        c.tipo
    ORDER BY 
        TotalCantidad DESC;
    """
    return db.execute_query(query)

