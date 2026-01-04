import sedona.db, os, geopandas

os.environ["AWS_SKIP_SIGNATURE"] = "true"
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

sd = sedona.db.connect()

df = sd.read_parquet("s3://overturemaps-us-west-2/release/2025-12-17.0/theme=buildings/type=building/")
df.to_view("buildings")
print("made buildings view")

df = sd.read_parquet("s3://overturemaps-us-west-2/release/2025-12-17.0/theme=divisions/type=division_area/")
df.to_view("division_area")
print("made divisions view")

cc_wkt = sd.sql(f"""
    SELECT
        geometry
    FROM division_area
    WHERE
        region = 'US-IL'
    AND 
        names.primary = 'Cook County'
""").to_pandas()['geometry'].iloc[0]
print("extracted cook county wkt")

cc = sd.sql(f"""
SELECT
    id, names.primary as primary_name, class, subtype, height, geometry
FROM buildings
WHERE
    ST_Intersects(
        geometry,
        ST_SetSRID(ST_GeomFromText('{cc_wkt}'), 4326)
    )
""").to_pandas()
print("extracted cook county buildings, now projecting to state plane and saving to geopackage")

output_path = '/Users/mattlayman/Downloads/test.gpkg'

try:
    projected_cc = cc.to_crs("EPSG:3435")
    projected_cc.to_file(output_path, driver='GPKG')
    print(f"Successfully saved data to {output_path}")
except Exception as e:
    print(f"An error occurred: {e}")


