# %%
import unittest

from randombox import random_box
from shapely.geometry import Polygon
import geopandas as gpd

square = [(0, 45), (5, 45), (5, 40), (0, 40)]
point_coord = Polygon(square)
poly = gpd.GeoDataFrame(
    data={"name": ["AOI"], "geometry": [point_coord]},
    geometry="geometry",
    crs="EPSG:4326",
)
poly.to_file("data/square.geojson", driver="GeoJSON")


class TestProperties(unittest.TestCase):
    def test_random_box(self):
        geo_path = "data/square.geojson"
        num_points = 10
        size = 0.1
        squares_gdf = random_box(geo_path, num_points, size)
        assert squares_gdf.shape[0] == num_points
        assert squares_gdf.crs == "EPSG:4326"


if __name__ == "__main__":
    unittest.main()

# %%
