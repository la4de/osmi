from contextlib import contextmanager
import geopandas
import os
import osmium
import shapely
import subprocess
import tempfile

@contextmanager
def filter(filename, filters):
    assert len(filters) > 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfilename = os.path.join(tmpdir, 'tmp.osm.pbf')
        p = subprocess.run([
            'osmium',
            'tags-filter',
            '--no-progress',
            filename,
            '--output', tmpfilename,
            *filters,
        ], check=True)
        yield tmpfilename


class OsmiHandler(osmium.SimpleHandler):
    def __init__(self, fields=None):
        super().__init__()
        self.fields = fields
        self.items = []
        self.wkbfab = osmium.geom.WKBFactory()

    def add_item(self, tags, wkb):
        if len(self.fields) > 0:
            tags = { field: tags.get(field) for field in self.fields }
        geometry = shapely.wkb.loads(wkb, hex=True)
        self.items.append({**tags, 'geometry': geometry })

    def node(self, n):
        try:
            wkb = self.wkbfab.create_point(n)
            self.add_item(dict(n.tags), wkb)
        except RuntimeError:
            print('err node', n.tags.get('name'))

    def way(self, w):
        try:
            wkb = self.wkbfab.create_multipolygon(w)
            self.add_item(dict(w.tags), wkb)
        except RuntimeError:
            print('err node', w.tags.get('name'))

    def area(self, a):
        try:
            wkb = self.wkbfab.create_multipolygon(a)
            self.add_item(dict(a.tags), wkb)
        except RuntimeError:
            print('err node', a.tags.get('name'))


def read_file(filename: str, filters: list[str], fields : list[str] = []):
    osm = OsmiHandler(fields)
    with filter(filename, filters) as tmp:
        osm.apply_file(tmp, locations=True)
    return geopandas.GeoDataFrame(osm.items, crs=4326)
