-- 0. Entendiendo los datos
-- ¿Qué datos contiene la tabla a analizar?
SELECT *
FROM tickets
LIMIT 100;

-- 1. Visión General de Ventas Totales
-- ¿Cuál es el ingreso total generado por el negocio?
SELECT sum(precio_total) as ingresos
FROM tickets;

-- 2. Tendencias de Ventas en el Tiempo
-- ¿Cómo ha sido la tendencia de ingresos mensuales?
select strftime('%Y, %m', fecha) as mes ,sum(precio_total) as ingresos
FROM tickets
group by mes
ORDER by mes;

-- 3. Análisis por Departamento y Sección
-- ¿Cuál es el rendimiento de cada departamento en términos de ventas?
select id_departamento, sum(precio_total) as ventas_departamento
from tickets
group by id_departamento
order by ventas_departamento DESC;

-- ¿Cómo se distribuyen las ventas entre las diferentes secciones?
select id_seccion, sum(precio_total) as ingresos_seccion
from tickets
group by id_seccion
order by ingresos_seccion DESC;

-- 4. Análisis de Productos
-- ¿Cuáles son los 10 productos más vendidos en cantidad?
select id_producto, sum(cantidad) as cantidad_total
from tickets
group by id_producto
order by cantidad_total;

-- ¿Qué 10 productos generan más ingresos?
select nombre_producto, sum(precio_total) as ingresos_producto
from tickets
group by nombre_producto
order by ingresos_producto DESC
limit 10;

-- 5. Comportamiento de los Clientes
-- ¿Quiénes son los 20 clientes que más compran en términos de ingresos?
select id_cliente, sum(precio_total) as ingresos_cliente
from tickets
GROUP by id_cliente
ORDER by ingresos DESC
limit 20;

-- Pregunta 8: ¿Cuál es la compra media por cliente?
SELECT AVG(ingresos_cliente) AS compra_media_cliente
from (select id_cliente, sum(precio_total) as ingresos_cliente
from tickets
GROUP by id_cliente);

-- Análisis de Pedidos
-- Pregunta 9: ¿Cuántos pedidos totales se han realizado?
SELECT count(DISTINCT(id_pedido)) as pedidos_totales
from tickets

-- valor promedio por pedido
select AVG(valor_pedido) as valor_promedio_pedido
from (SELECT id_pedido, sum(precio_total) as valor_pedido 
from tickets
group by id_pedido);


