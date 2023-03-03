# %%
import unittest
from randombox import random_box, Random_Points_In_Polygon
from shapely.geometry import Polygon
import geopandas as gpd
import random
import numpy as np
from rasterio.transform import Affine
import rasterio


random.seed(10)

poly = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
poly.loc[poly["name"] == "Tanzania"].to_file("./data/square.geojson", driver="GeoJSON")

x = np.linspace(-20, 20, 6)
y = np.linspace(20, -20, 6)
X, Y = np.meshgrid(x, y)
Z1 = np.abs(((X - 10) ** 2 + (Y - 10) ** 2) / 1**2)
Z2 = np.abs(((X + 10) ** 2 + (Y + 10) ** 2) / 2.5**2)
Z = Z1 - Z2
xres = (x[-1] - x[0]) / len(x)
yres = (y[-1] - y[0]) / len(y)

transform = Affine.translation(x[0] - xres / 2, y[0] - yres / 2) * Affine.scale(
    xres, yres
)


with rasterio.open(
    "data/square.tif",
    "w",
    driver="GTiff",
    height=Z.shape[0],
    width=Z.shape[1],
    count=1,
    dtype=Z.dtype,
    crs="+proj=latlong",
    transform=transform,
) as dst:
    dst.write(Z, 1)


class TestProperties(unittest.TestCase):
    def test_random_box_geopandas(self):
        geo_path = "data/square.geojson"
        num_points = 5
        size = 0.1
        squares_gdf = random_box(
            geo_path, num_points, size, year="2020", crs="EPSG:32737"
        )
        assert squares_gdf.shape[0] == num_points
        assert squares_gdf.crs == "EPSG:32737"

    # test if rasterio can read the file
    def test_random_box_rasterio(self):
        geo_path = "data/square.tif"
        num_points = 5
        size = 0.1
        squares_gdf = random_box(
            geo_path, num_points, size, year="2020", crs="EPSG:32737"
        )
        assert squares_gdf.shape[0] == num_points
        assert squares_gdf.crs == "EPSG:32737"

    def test_Random_Points_In_Polygon(self):
        poly = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        poly = poly[poly.name == "United States of America"]
        points = Random_Points_In_Polygon(poly, 5)
        assert len(points) == 5


if __name__ == "__main__":
    unittest.main()


# %%
