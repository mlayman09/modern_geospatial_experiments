# Modern Geospatial Experiments

This repo contains scripts I've put together using modern geospatial tools like DuckDB and SedonaDB.

## Overview

As of now, this repository contains two scripts that download Cook County, IL building footprints from [Overture Maps](https://overturemaps.org).
One uses [DuckDB](https://duckdb.org), and the other uses [SedonaDB](https://sedona.apache.org/sedonadb/latest/). Both run relatively quickly, but the SedonaDB script only takes 1.5 minutes to run,
while the DuckDB script takes 5 minutes to run, at least on my machine.

## Software you'll need

- Python 3.8+
- DuckDB (with spatial extension)
- SedonaDB (python library)
- GeoPandas (python library)


## Running the scripts

SedonaDB script | cook_county_buildings.py
```
python3 -m cook_county_buildings
```

DuckDB script | cook_county_buildings.sql
```
duckdb -init cook_county_buildings.sql
```


## Background

Geospatial tools keep getting better, and it's pretty incredible what we can do nowadays. I've been hearing about DuckDB for a while through various channels, and SedonaDB got released this fall, so I decided to check them out for myself and see how they perform.

Let's say you want to download building footprints for your county. You used to have to download an entire file that likely covered an area much larger than your area of interest, and then transform it later in a desktop GIS or with a python script. Now, with tools like DuckDB and file formats like GeoParquet, I can write a script to download just what I need and nothing more. I can clip those building footprints to a county boundary, reproject them if needed, keep only the columns of data I'm interested in, and then download the results to my machine, all in one script. No massive initial download required- that alone is a big step forward in my view.




