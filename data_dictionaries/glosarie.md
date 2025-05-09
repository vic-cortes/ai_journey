# Descripción de Variables de Datos Abiertos de Asegurados

## Variables de Identificación Geográfica

- **cve_delegacion**: Clave numérica que identifica la delegación de adscripción operativa del IMSS. Existen 35 delegaciones en total.

- **cve_subdelegacion**: Clave numérica que identifica la subdelegación de adscripción operativa del IMSS. Existen 133 subdelegaciones en total.

- **cve_entidad**: Clave numérica que identifica la entidad federativa asociada a la ubicación del patrón asegurado ante el IMSS.

- **cve_municipio**: Clave numérica que identifica el municipio asociado a la ubicación del patrón asegurado ante el IMSS.

## Variables de Sector Económico

- **sector_economico_1**: Clasificación de primer nivel de la actividad económica de los patrones afiliados al IMSS.

- **sector_economico_2**: Clasificación de segundo nivel de la actividad económica de los patrones afiliados al IMSS.

- **sector_economico_4**: Clasificación de cuarto nivel de la actividad económica de los patrones afiliados al IMSS.

## Variables de Características del Trabajador

- **tamaño_patron**: Tamaño del patrón determinado con base en el número de asegurados vigentes que registra ante el IMSS. Se clasifica en rangos desde S1 (con un puesto de trabajo) hasta S7 (con más de 1,000 puestos de trabajo).

- **sexo**: Clasificación del asegurado como hombre (1), mujer (2) o no binario (3).

- **rango_edad**: Rango de edad asociado al asegurado, clasificado desde E1 (menor de 15 años) hasta E14 (mayor de 75 años).

- **rango_salarial**: Rango salarial en número de veces el salario mínimo de la Ciudad de México, desde W1 (hasta 1 vez el salario mínimo) hasta W25 (mayor a 24 y hasta 25 veces el salario mínimo).

- **rango_uma**: Rango salarial en número de veces la Unidad de Medida y Actualización (UMA), desde U1 (hasta 1 vez el salario mínimo) hasta U25 (mayor a 24 y hasta 25 veces el valor de la UMA).

## Variables de Conteo

- **asegurados**: Personas que están aseguradas en el IMSS de manera directa como titulares, incluye todas las modalidades de aseguramiento. La cifra contabiliza a todas las personas afiliadas en el IMSS, ya sea como "puestos trabajo afiliados al IMSS (empleos asegurados)" o como "asegurados sin un empleo (cotizantes sin un puesto de trabajo asociado)". Aquellas personas afiliadas con más de un tipo de afiliación (ej. estudiantes y trabajador) se contabilizan tantas veces como tipos de afiliación mantengan.

- **no_trabajadores**: Número de trabajadores.

- **ta**: Total de puestos de trabajo afiliados al IMSS (empleo asegurado o asegurados asociados a un empleo).

- **teu**: Total de puestos de trabajo eventuales urbanos.

- **tec**: Total de puestos de trabajo eventuales del campo.

- **tpu**: Total de puestos de trabajo permanentes urbanos.

- **tpc**: Total de puestos de trabajo permanentes del campo.

## Variables de Salario

- **ta_sal**: Total de puestos de trabajo afiliados con un salario asociado. Incluye las modalidades de aseguramiento asociadas a un empleo y con salario relativo a un ingreso real otorgado por parte de un patrón (10, 13, 14, 17, 34, 36, 38 y 42).

- **teu_sal**: Total de puestos de trabajo eventuales urbanos con salario asociado.

- **tec_sal**: Total de puestos de trabajo eventuales del campo con salario asociado.

- **tpu_sal**: Total de puestos de trabajo permanentes urbanos con salario asociado.

- **tpc_sal**: Total de puestos de trabajo permanentes del campo con salario asociado.

## Variables de Masa Salarial

- **masa_sal_ta**: Masa salarial total de puestos de trabajo afiliados. Se refiere a la nómina que considera tanto el salario como la plantilla de trabajadores. El salario base de cotización reportado por los patrones al IMSS integra pagos en efectivo por cuota diaria, gratificaciones, percepciones, alimentación, habitación, primas, comisiones, prestaciones en especie y cualquier otra cantidad o prestación entregada al trabajador por su trabajo, con las excepciones previstas en el artículo 27 de la Ley del Seguro Social.

- **masa_sal_teu**: Masa salarial de puestos de trabajo eventuales urbanos.

- **masa_sal_tec**: Masa salarial de puestos de trabajo eventuales del campo.

- **masa_sal_tpu**: Masa salarial de puestos de trabajo permanentes urbanos.

- **masa_sal_tpc**: Masa salarial de puestos de trabajo permanentes del campo.

## Modalidades de Aseguramiento

### Aseguramiento asociado a puestos de trabajo:
- **10**: Permanentes y eventuales de la ciudad (10.1 Permanentes, 10.2 y 10.3 Eventuales)
- **13**: Permanentes y eventuales del campo (13.1 Permanentes, 13.2 y 13.4 Eventuales del campo)
- **14**: Eventuales del campo cañero
- **17**: Reversión de cuotas por subrogación de servicios (17.1 Permanentes, 17.2 Eventuales)
- **30**: Productores de caña de azúcar
- **34**: Domésticos
- **35**: Patrones personas físicas con trabajadores a su servicio
- **36, 38, 42**: Al servicio de gobiernos estatales, municipales y organismos descentralizados/administración pública federal
- **43**: Incorporación voluntaria del campo al régimen obligatorio
- **44**: Independientes

### Aseguramiento sin un empleo asociado:
- **32**: Seguro facultativo, familiares del IMSS y CFE (principalmente estudiantes)
- **33**: Seguro de salud para la familia
- **40**: Continuación voluntaria en el régimen obligatorio