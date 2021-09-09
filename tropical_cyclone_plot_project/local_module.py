import geopandas 
import requests
from   zipfile import ZipFile

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
                gdf_names[file_names[2]][idx]  = geopandas.read_file(
                f'zip://./nhc_latest/{file_names[2]}!{zip_file_name.namelist()[_[idx]]}')
        return gdf_names

    track_line_gdf        = 'none'
    cone_gdf              = 'none'
    points_gdf            = 'none'
    init_radii_gdf        = 'none'
    fcst_radii_gdf        = 'none'
    best_track_points_gdf = 'none'
    best_track_line_gdf   = 'none'
    best_track_radii_gdf  = 'none'
    best_track_swath_gdf  = 'none'
    gtwo_areas_gdf        = 'none'
    gtwo_lines_gdf        = 'none'
    gtwo_points_gdf       = 'none'
    wsp_34_gdf_points     = 'none'
    wsp_50_gdf_points     = 'none'
    wsp_64_gdf_points     = 'none'
    wsp_34_gdf_polygons   = 'none'
    wsp_50_gdf_polygons   = 'none'
    wsp_64_gdf_polygons   = 'none'

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
