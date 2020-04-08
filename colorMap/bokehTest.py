from bokeh.plotting import figure, save, show
import bokeh
p = figure(title="My first interactive plot!")
"""x_coords = [0,1,2,3,4]
y_coords = [5,4,1,2,0]
p.circle(x=x_coords, y=y_coords, size=10, color="red")
# Give output filepath
outfp = r"points.html"
# Save the plot by passing the plot -object and output path
save(obj=p, filename=outfp)
show(p)"""
import geopandas as gpd

# File path
points_fp = r"/home/geo/data/addresses.shp"

# Read the data
points = gpd.read_file(points_fp)