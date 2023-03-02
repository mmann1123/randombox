Creates randomly located boxes of a fixed size

# randombox

## Installation

```bash
git clone https://github.com/mmann1123/randombox.git
cd randombox
pip install -r ./requirements.txt
```

## Usage

The shapefile.shp should be a polygon representing the area of interest within which small boxes will be created.

```python
 from randombox import random_box

 geo_path = "data/shapefile.shp"
 num_points = 10
 size = 0.1
 squares_gdf = random_box(geo_path, num_points, size)
 squares_gdf.to_file("folder/squares.geojson", driver="GeoJSON")
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
