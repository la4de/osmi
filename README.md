# osmi

OSM data importer. Package uses `osmium` executable for filtering.

## Why?

Many python packages are very memory hungry and slow especially with large osm export files. This uses `tags-filter` filter command from `osmium` which is very fast and memory efficient.

## Usage

```python
import osmi

# read all shelter nodes to GeoDataFrame, only name and shelter_type fields are imported
df = osmi.read_file('finland-latest.osm.pbf', filters=['n/amenity=shelter'], fields=['name', 'shelter_type'])

# write output to geopackage file
df.to_file('shelter.gpkg')
```
