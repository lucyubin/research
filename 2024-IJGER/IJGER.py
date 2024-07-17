import pandas as pd
import geokakao as gk
import geopandas as gpd
from shapely.geometry import Point

# geocoding
file_path = '*'
data = pd.read_csv(file_path + '병원목록.csv', encoding='euc-kr')

gk.add_coordinates_to_dataframe(data, '주소')
data.to_csv(file_path + '병원목록_geocd.csv', index=False, encoding='euc-kr')

geometry = [Point(xy) for xy in zip(data.decimalLongitude, data.decimalLatitude)]
gdf = gpd.GeoDataFrame(data, geometry=geometry)
gdf.set_crs(epsg=4326, inplace=True)
gdf.to_file(file_path + '병원목록_goecd.shp', driver='ESRI Shapefile', encoding='euc-kr')


# as type
shp = gpd.read_file('*.shp')
shp.dtypes
shp['SGGCD'] = shp['SGGCD'].astype('int64')
shp['COUNT'] = shp['COUNT'].astype('int64')
shp['POP'] = shp['POP'].astype('int64')
shp.to_file(file_path + 'pop.shp')

den = gpd.read_file('*.shp')
den.dtypes
den.to_file(file_path + 'den.shp')

den.crs #5179

# 포인트 객체 생성
den_point = den.copy()
den_point['geometry'] = den_point['geometry'].centroid
den_point.set_crs(epsg=5179, inplace=True)

den_point.to_file(file_path + 'den_point.shp', driver='ESRI Shapefile', encoding='euc-kr')
