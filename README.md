Creates randomly located boxes of a fixed size

# randombox

## Installation

```bash
git clone https://github.com/mmann1123/randombox.git
cd randombox
pip install -r ./requirements.txt
```

## Usage

The `geo_path` should be a polygon or raster image representing the area of interest within which small boxes will be created.

The size of the box is determined by the linear unit of `crs`

```python
 from randombox import random_box

# read in a geotif
geo_path = "/some/folder/image.tif"
num_points = 5
size = 1000
squares_gdf = random_box(geo_path, num_points, size, name_postfix="2020", crs="EPSG:3395")

# Alternatively pass a geojson file defining the area of interest. 
geo_path = "/some/data/square.geojson"
num_points = 5
size = 1000
squares_gdf = random_box(geo_path, num_points, size, name_postfix="2020", crs="EPSG:3395")

```

## Development

```bash
git clone
cd randombox
pip install -e .
```

## Testing

```bash
pip install testfixtures
python -m unittest
```

## License

 MIT

## Contribute

As you make local edits, install them using the following from the terminal:

``` bash
pip install e . 
```
