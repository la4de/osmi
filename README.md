# osmi

OSM data importer. Package uses `osmium` executable for filtering.

## Usage

```python
import osmi
filename = 'finland-latest.osm.pbf'
df = osmi.read_file(filename, ['n/amenity=shelter'])
df.to_file('shelter.gpkg')
```
