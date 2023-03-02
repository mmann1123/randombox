import numpy as np
from shapely.geometry import Polygon, Point
import geopandas as gpd
import os


# create random points within polygon
def Random_Points_In_Polygon(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    while len(points) < num_points:
        random_point = Point(
            [np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)]
        )
        if random_point.within(poly):
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


# read in shapefile create random points inside of it and create square polygons around each point of a given size return geodataframe of squares with crs of polygon
def random_box(geo_path, num_points, size, year):
    polygon = gpd.read_file(geo_path)
    points = Random_Points_In_Polygon(polygon.geometry[0], num_points)
    squares_gdf = create_square_gdf(points, size, polygon)
    write_to_geojson(squares_gdf, geo_path, year)
    return squares_gdf


# iterate through features of squares_gdf and write each feature to a new geojson file
def write_to_geojson(squares_gdf, geo_path, year):
    for i, row in squares_gdf.iterrows():
        square = squares_gdf.loc[[i]]
        print(square)
        filename = os.path.join(
            os.path.dirname(geo_path), f"{i:06d}_grid_{year}" + ".geojson"
        )
        square.to_file(
            filename,
            driver="GeoJSON",
        )
        square.to_file(
            os.path.join(
                os.path.dirname(geo_path), f"{i:06d}_poly_{year}" + ".geojson"
            ),
            driver="GeoJSON",
        )
