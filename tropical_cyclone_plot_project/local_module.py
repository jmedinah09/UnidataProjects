import pandas
import geopandas 
import matplotlib.pyplot as plt
from   matplotlib.pyplot import imread
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from   cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from   shapely.geometry import Point, LineString, Polygon, MultiPoint

import requests
from   zipfile import ZipFile
import datetime 
import feedparser


class NhcDownloaderBot:
    def __init__(self, storm_number = 1, year = 2020):
        self.file_names   = file_names = [
                                            f'al{storm_number}{year}_5day_latest.zip',
                                            f'al{storm_number}{year}_fcst_latest.zip',
                                            f'al{storm_number}{year}_best_track.zip',
                                            f'gtwo_shapefiles.zip',
                                            f'wsp_120hrhalfDeg_latest.zip',
                                            f'wsp_120hr5km_latest.zip'
                                         ]
        self.urls         = urls       = [
                                            f'https://www.nhc.noaa.gov/gis/forecast/archive',
                                            f'https://www.nhc.noaa.gov/gis/forecast/archive',
                                            f'https://www.nhc.noaa.gov/gis/best_track',
                                            f'https://www.nhc.noaa.gov/xgtwo',
                                            f'https://www.nhc.noaa.gov/gis/forecast/archive',
                                            f'https://www.nhc.noaa.gov/gis/forecast/archive'
                                         ]
        self.gdf_names   =  gdf_names  = {
                                            file_names[0] : ['track_line_gdf', 'cone_gdf', 'points_gdf'],
                                            file_names[1] : ['init_radii_gdf', 'fcst_radii_gdf'],
                                            file_names[2] : ['best_track_points_gdf', 'best_track_line_gdf', 'best_track_radii_gdf', 'best_track_swath_gdf'],
                                            file_names[3] : ['gtwo_areas_gdf', 'gtwo_lines_gdf', 'gtwo_points_gdf'],
                                            file_names[4] : ['wsp_34_gdf_points', 'wsp_50_gdf_points', 'wsp_64_gdf_points'],
                                            file_names[5] : ['wsp_34_gdf_polygons', 'wsp_50_gdf_polygons', 'wsp_64_gdf_polygons']
                                          }
    def nhc_gis_downloader(self, file_names, urls, gdf_names):

        for idx, file_name in enumerate(file_names):
            url = f'{urls[idx]}/{file_name}'
            r = requests.get(url)
            with open(f'nhc_latest/{file_name}', 'wb') as code:
                code.write(r.content)
        _  = [0, 3, 4, 5]
        __ = [2, 7, 12]
        for idx, file_name in enumerate([file_names[0],  file_names[3],
                                        file_names[4],  file_names[5]]):
            with ZipFile(f'nhc_latest/{file_name}', 'r') as zip_file_name:
                for idx2 in range(len(gdf_names[file_names[_[idx]]])):
                    gdf_names[file_names[_[idx]]][idx2]  = geopandas.read_file(
                    f'zip://./nhc_latest/{file_name}!{zip_file_name.namelist()[__[idx2]]}')
        _  = [0,5]
        with ZipFile(f'nhc_latest/{file_names[1]}', 'r') as zip_file_name:
                for idx in range(2):
                    gdf_names[file_names[1]][idx]  = geopandas.read_file(
                    f'zip://./nhc_latest/{file_names[1]}!{zip_file_name.namelist()[_[idx]]}')
        _  = [2, 7, 13, 16]
        with ZipFile(f'nhc_latest/{file_names[2]}', 'r') as zip_file_name:
            for idx in range(4):
                try:
                    gdf_names[file_names[2]][idx]  = geopandas.read_file(
                    f'zip://./nhc_latest/{file_names[2]}!{zip_file_name.namelist()[_[idx]]}')
                except IndexError:
                    gdf_names[file_names[2]][idx] = None
        return gdf_names
    @classmethod
    def gdf_file(cls, storm_number, year):
        _ = NhcDownloaderBot(storm_number, year)
        cls.track_line_gdf        = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[0]][0]
        cls.cone_gdf              = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[0]][1]
        cls.points_gdf            = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[0]][2]
        cls.init_radii_gdf        = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[1]][0]
        cls.fcst_radii_gdf        = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[1]][1]
        cls.best_track_points_gdf = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[2]][0]
        cls.best_track_line_gdf   = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[2]][1]
        cls.best_track_radii_gdf  = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[2]][2]
        cls.best_track_swath_gdf  = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[2]][3]
        cls.gtwo_areas_gdf        = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[3]][0]
        cls.gtwo_lines_gdf        = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[3]][1]
        cls.gtwo_points_gdf       = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[3]][2]
        cls.wsp_34_gdf_points     = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[4]][0]
        cls.wsp_50_gdf_points     = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[4]][1]
        cls.wsp_64_gdf_points     = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[4]][2]
        cls.wsp_34_gdf_polygons   = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[5]][0]
        cls.wsp_50_gdf_polygons   = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[5]][1]
        cls.wsp_64_gdf_polygons   = _.nhc_gis_downloader(_.file_names, _.urls, _.gdf_names)[_.file_names[5]][2]
        
        
        
        
class MapTemplate:
    def __init__(self, extent     = [-72, -68, 17.5, 20]):
        self.extent               = extent
        self.path                 = path               = '../shape_files/rd_shapes/vectores'
        #self.hispaniola_gdf       = hispaniola_gdf    = geopandas.read_file(f'{ self.path }/hispaniola.shp').to_crs("EPSG:4326")
        #self.municipios           = municipios        = geopandas.read_file(f'{ self.path }/División_Prov_Muni_y_Dist_MuniUTM.shp').to_crs("EPSG:4326")
        #self.limite_gdf           = limite_gdf        = geopandas.read_file(f'{ self.path }/limite_frontera.shp').to_crs("EPSG:4326")
        self.silueta_haiti_gdf    = silueta_haiti_gdf = geopandas.read_file(f'{ self.path }/silueta_haiti.shp').to_crs("EPSG:4326")
        self.silueta_rd_gdf       = silueta_rd_gdf    = geopandas.read_file(f'{ self.path }/silueta_rd.shp').to_crs("EPSG:4326")
        self.provincias_gdf       = provincias_gdf    = geopandas.read_file(f'{ self.path }/PROVINCIAS.shp').to_crs("EPSG:4326")
        #self.rios_gdf             = rios_gdf          = geopandas.read_file(f'{ self.path }/RIOS.shp').to_crs("EPSG:4326")
        #self.cuencas_hidro_gdf    = cuencas_hidro_gdf = geopandas.read_file(f'{ self.path }/Cuencas_Hidrograficas_RD.shp').to_crs("EPSG:4326")
        #self.cuencas_presas_gdf   = cuencas_presas_gdf= geopandas.read_file(f'{ self.path }/Presas-CuencasAporte.shp').to_crs("EPSG:4326")
        #self.states_provinces_gdf = geopandas.read_file(f'{self.path}/ne_10m_admin_1_states_provinces.shp')
        self.land_gdf             = geopandas.read_file(f'{self.path}/ne_10m_land.shp')
        #self.ocean_gdf            = geopandas.read_file(f'{self.path}/ne_10m_ocean.shp')
        self.coastline_gdf        = geopandas.read_file(f'{self.path}/ne_10m_coastline.shp')
        self.countries_gdf        = geopandas.read_file(f'{self.path}/ne_10m_admin_0_countries.shp')
        
        self.map_crs = ccrs.PlateCarree()
    data_crs= ccrs.PlateCarree()
        
    def base_map(self):
        fig = plt.figure(figsize=(20, 20))
        ax  = plt.subplot(1, 1, 1, projection = self.map_crs)

        ax.add_feature(cfeat.OCEAN.with_scale('10m'))

        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=0.5, color='black', linestyle='--')
        gl.xlabels_bottom = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.ylocator = mticker.FixedLocator([0, 10, 20, 30, 40, 50, 55])
        gl.xlabel_style = {'weight': 'bold'}
        gl.ylabel_style = {'weight': 'bold'}
        
        logos = ['iglogo40x40', 'fblogo40x40', 'ttlogo50x50', 'onamet-150X43']
        x, y = 652, 13
        for logo in logos: 
            if logo == 'ttlogo50x50':
                y = y-5
            elif logo == 'onamet-150X43':
                x, y = 45, 13
            logo = imread(f'../{logo}.png')
            fig.figimage(logo, x, y, zorder=100)
            x = x + 170
        
        props = dict(boxstyle='round', facecolor='white', alpha=1)
        xtxt = [0.546, 0.549, 0.552, 0.555]
        ytxt = -0.64
        text = '       @onamet            @onamet             @onamet'
        for x in xtxt:
            ax.text(x, ytxt, text, transform=ax.transAxes, fontsize=18, verticalalignment='top', bbox=props, 
                weight = 'bold', color = 'blue')
        xtxt = 0.04
        ytxt = -0.67
        text = 'www.onamet.gob.do'
        ax.text(xtxt, ytxt, text, transform=ax.transAxes, fontsize=12, verticalalignment='top',
                weight = 'bold', color = 'red')
        props = dict(facecolor='whitesmoke')
        xtxt = 0.0055
        ytxt = -0.01
        a = 239*'.'
        text = f'''{a}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{a}'''
        ax.text(xtxt, ytxt, text, transform=ax.transAxes, fontsize=12, verticalalignment='top',
                weight = 'bold', color = 'b', bbox=props, zorder = -1)
        return fig, ax
        
    @classmethod    
    def zoomed_map(cls):
        _  = MapTemplate()
        fig, ax = _.base_map()
        ax.set_extent([-72, -68, 17.5, 20])
        ax.add_geometries(_.silueta_haiti_gdf['geometry'], crs=cls.data_crs, facecolor='none',
                 edgecolor='black', linewidth=0.5)
        ax.add_geometries(_.provincias_gdf['geometry'], crs=cls.data_crs, facecolor='honeydew',
                 edgecolor='black', linewidth=0.5)
        return fig, ax
    @classmethod     
    def wide_map(cls):
        _  = MapTemplate()
        fig, ax = _.base_map()
        ax.set_extent([-100, 0, 0, 40])
        ax.stock_img()
#         ax.add_geometries(_.land_gdf['geometry'], crs=_.data_crs, facecolor='none',
#                               edgecolor='black', linewidth=1, alpha=0.7)
#         ax.add_geometries(_.coastline_gdf['geometry'], crs=_.data_crs, facecolor='none',
#                              edgecolor='black', linewidth=0.5)
        ax.add_geometries(_.countries_gdf['geometry'], crs=_.data_crs, facecolor='whitesmoke',
                             edgecolor='black', linewidth=0.5, zorder = 10, alpha = 0.7)
        return fig, ax
    
    
class NhcRssParser:
    def __init__(self, url):    
        self.url   = url 
        self.f     = f   =  feedparser.parse(self.url)
        self.df    = df  =  pandas.DataFrame(self.f.entries).drop(columns=['title_detail', 'summary', 'summary_detail', 'published_parsed', 'links', 'link', 'id', 
                               'guidislink', 'authors', 'author', 'author_detail'])
    
    #{key: value for (key, value) in iterable}
    def tc_dict_list(self):
        return {nhc_atcf: [nhc_name    , nhc_type, nhc_center, nhc_movement, 
                        nhc_pressure, nhc_wind, published , nhc_datetime]         
             for (nhc_name    , nhc_atcf, nhc_type  , nhc_center  , nhc_movement,
                  nhc_pressure, nhc_wind, published , nhc_datetime) 
             in  zip(self.df['nhc_name']    , self.df['nhc_atcf']    , self.df['nhc_type'], self.df['nhc_center'], 
                     self.df['nhc_movement'], self.df['nhc_pressure'], self.df['nhc_wind'], self.df['published'],
                     self.df['nhc_datetime']) 
             if pandas.isnull(nhc_name) == False}, [nhc_atcf for nhc_atcf in self.df['nhc_atcf'] if pandas.isnull(nhc_atcf) == False]
    
    
    
    
    
    
'''
align_string.py

Align string with spaces between words to fit specified width

Author: Denis Barmenkov <denis.barmenkov@gmail.com>

Copyright: this code is free, but if you want to use it, 
           please keep this multiline comment along with function source. 
           Thank you.

2005-05-22 13:27 - first revision
2010-03-09 17:01 - added align_paragraph()
2010-03-09 17:56 - added check for paragraph's last line
__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/414870/'
'''
import re, textwrap

def items_len(l):
    return sum([ len(x) for x in l] )

lead_re = re.compile(r'(^\s+)(.*)$')

def align_string(s, width, last_paragraph_line=0):
    '''
    align string to specified width 
    '''
    # detect and save leading whitespace
    m = lead_re.match(s) 
    if m is None:
        left, right, w = '', s, width
    else:
        left, right, w = m.group(1), m.group(2), width - len(m.group(1))

    items = right.split()

    # add required space to each words, exclude last item
    for i in range(len(items) - 1):
        items[i] += ' '

    if not last_paragraph_line:
        # number of spaces to add
        left_count = w - items_len(items)
        while left_count > 0 and len(items) > 1:
            for i in range(len(items) - 1):
                items[i] += ' '
                left_count -= 1
                if left_count < 1:  
                    break

    res = left + ''.join(items)
    return res

def align_paragraph(paragraph, width, debug=0):
    '''
    align paragraph to specified width,
    returns list of paragraph lines
    '''
    lines = list()
    if type(paragraph) == type(lines):
        lines.extend(paragraph)
    elif type(paragraph) == type(''):
        lines.append(paragraph)
    elif type(paragraph) == type(tuple()):
        lines.extend(list(paragraph))
    else:
        raise TypeError('Unsopported paragraph type: %r' % type(paragraph))

    flatten_para = ' '.join(lines)

    splitted = textwrap.wrap(flatten_para, width) 
    if debug:
        print('textwrap:\n%s\n' % '\n'.join(splitted))

    wrapped = list()
    while len(splitted) > 0:
        line = splitted.pop(0)
        if len(splitted) == 0:
            last_paragraph_line = 1
        else:
            last_paragraph_line = 0
        aligned = align_string(line, width, last_paragraph_line)
        wrapped.append(aligned)

    if debug:
        print('textwrap & align_string:\n%s\n' % '\n'.join(wrapped))
    #wrapped = 'textwrap & align_string:\n%s\n' % '\n'.join(wrapped

    return '\n'.join(wrapped)

'''
    =====================
    Script output:
    =====================

    textwrap:
    Contributors whose recipes are
    used in the book will receive
    a complimentary copy of the
    Second Edition. A portion of
    all royalties will go to the
    non-profit Python Software
    Foundation. [Last words]

    textwrap & align_string:
    Contributors whose recipes are
    used  in the book will receive
    a  complimentary  copy  of the
    Second  Edition.  A portion of
    all  royalties  will go to the
    non-profit   Python   Software
    Foundation. [Last words]
'''