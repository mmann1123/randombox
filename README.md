Creates randomly located points of a fixed size

# randombox

## Installation


```bash
git clone https://github.com/mmann1123/randombox.git
cd randombox
pip install -e .
```


## Usage

```python
 from randombox import random_box

 geo_path = "data/shapefile.shp"
 num_points = 10
 size = 0.1
 squares_gdf = random_box(geo_path, num_points, size)
```

## Development

```bash
git clone
cd randombox
pip install -e .
```

## Testing

```bash
pytest
```

## License
 MIT
