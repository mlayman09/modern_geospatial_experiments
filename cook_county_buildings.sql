LOAD spatial;
LOAD httpfs;

--Extract Cook County WKT from Overture Maps
SET variable cook_county_wkt = (
    SELECT
        geometry
    FROM
        read_parquet('az://overturemapswestus2.blob.core.windows.net/release/2025-12-17.0/theme=divisions/type=division_area/*', filename=true, hive_partitioning=1)
    WHERE
        region = 'US-IL'
        AND names.primary = 'Cook County'
);

--Query buildings from Overture Maps using the Cook County boundary queried above. Save to Geopackage.
COPY(
  SELECT
        id,
        names.primary as primary_name,
        class,
        subtype,
        height,
        geometry
  FROM
        read_parquet('az://overturemapswestus2.blob.core.windows.net/release/2025-12-17.0/theme=buildings/type=building/*', filename=true, hive_partitioning=1) AS buildings
  WHERE
        bbox.xmin BETWEEN -88.555545 AND -86.936375
        AND bbox.ymin BETWEEN 41.393940 AND 42.634270
        AND ST_Intersects(
            geometry,
            CAST(getvariable('cook_county_wkt') AS GEOMETRY))
    )
TO '/Users/mattlayman/Downloads/test.gpkg' 
WITH (FORMAT GDAL, DRIVER 'GPKG');

