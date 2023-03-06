# %%
import numpy as np
from shapely.geometry import Polygon, Point, box
import geopandas as gpd
import os
import rasterio
from geopandas import GeoDataFrame


# create random points within polygon
def Random_Points_In_Polygon(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds.values[0]
    points = []
    while len(points) < num_points:
        random_point = Point(
            [np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)]
        )
        if any(random_point.within(poly.geometry)):
            points.append(random_point)

    return points


# create square polygons around each point
def create_square(point, size):
    x, y = point.x, point.y
    square = Polygon(
        [
            (x - size * 0.5, y - size * 0.5),
            (x + size * 0.5, y - size * 0.5),
            (x + size * 0.5, y + size * 0.5),
            (x - size * 0.5, y + size * 0.5),
        ]
    )
    return square


# apply create_square function to each point and create geoDataFrame with crs of polygon
def create_square_gdf(points, size, polygon):
    squares = [create_square(point, size) for point in points]
    squares_gdf = gpd.GeoDataFrame(squares, columns=["geometry"])
    squares_gdf.crs = polygon.crs
    return squares_gdf


# try reading shapfile using geopandas except read file with rasterio from input file path, then get bounds and create polygon from bounds
def read_a_file(geo_path):
    try:
        polygon = gpd.read_file(geo_path)
    except:
        with rasterio.open(geo_path) as src:
            bounds = src.bounds
            geom = box(*bounds)
            polygon = gpd.GeoDataFrame(geometry=[geom], crs=src.crs.to_string())
    return polygon


# iterate through features of squares_gdf and write each feature to a new geojson file
def write_to_geojson(squares_gdf, geo_path, name_prefix, name_postfix):
    for i, row in squares_gdf.iterrows():
        # get square from squares_gdf
        square = squares_gdf.loc[[i]]

        # use index as name_prefix if name_prefix is None
        if name_prefix is None:
            name_prefix = f"{i:06d}"

        # write grid to geojson
        filename = os.path.join(
            os.path.dirname(geo_path),
            f"{name_prefix}_grid_{name_postfix}" + ".geojson",
        )
        square.to_file(
            filename,
            driver="GeoJSON",
        )

        # write ploy to geojson
        square.to_file(
            os.path.join(
                os.path.dirname(geo_path),
                f"{name_prefix}_poly_{name_postfix}" + ".geojson",
            ),
            driver="GeoJSON",
        )


# read in shapefile create random points inside of it and create square polygons around each point of a given size return geodataframe of squares with crs of polygon
def random_box(
    geo_path, num_points, size, name_prefix=None, name_postfix=None, crs="EPSG:3395"
):
    """
    Writes a geojson file for random squares of a given size in a given crs
    within polygon or raster bounds in geo_path

    geo_path: path to shapefile or raster
    num_points: number of random boxes to create
    size: size of square in linear unit of crs
    name_prefix: name_prefix of data - prepended to filename

    name_postfix: name_postfix of data - appended to filename
    crs: crs of output with linear unit for use in size

    returns: geodataframe of squares with crs of polygon
    """
    polygon = read_a_file(geo_path).to_crs(crs)
    points = Random_Points_In_Polygon(polygon.geometry, num_points)
    squares_gdf = create_square_gdf(points, size, polygon)
    write_to_geojson(squares_gdf, geo_path, name_prefix, name_postfix)
    return squares_gdf


# # %%

# poly = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
# poly = poly[poly.name == "Tanzania"]
# points = Random_Points_In_Polygon(poly, 5)
# assert len(points) == 5

# # %%
# geo_path = "/home/mmann1123/Documents/github/randombox/data/square.tif"
# num_points = 5
# size = 0.1
# squares_gdf = random_box(geo_path, num_points, size, name_postfix="2020", crs="EPSG:32737")
# assert squares_gdf.shape[0] == num_points
# assert squares_gdf.crs == "EPSG:32737"

# # %%
# geo_path = "/home/mmann1123/Documents/github/randombox/data/square.geojson"
# num_points = 5
# size = 0.1
# squares_gdf = random_box(geo_path, num_points, size, name_postfix="2020", crs="EPSG:32737")
# assert squares_gdf.shape[0] == num_points
# assert squares_gdf.crs == "EPSG:32737"
# %%
