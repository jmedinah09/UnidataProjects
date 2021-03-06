#! /bin/bash

echo "Setting up parameters..."
if      [ "$(date +%H)" -ge 20 -a "$(date +%H)" -le 23 ]; then 
        a='A'; hr=00; hr2=18
 elif   [ "$(date +%H)" -ge 00 -a "$(date +%H)" -le 07 ]; then 
  	a='A'; hr=00; hr2=18
 elif   [ "$(date +%H)" -ge 08 -a "$(date +%H)" -le 13 ]; then 
  	a='B'; hr=12; hr2=06
 elif   [ "$(date +%H)" -ge 14 -a "$(date +%H)" -le 19 ]; then
        a='C'; hr=12; hr2=12
fi

echo "Setting up directories (If exist, removing files)..."
caDir=~/Desktop/CCarpeta_de_Analisis/"$(date -u +%Y)"/"$(date -u +%m)"/C"$a""$(date -u +%d%m%y)"/iSAT
#caDir=/mnt/e/Pronostico/Carpeta_de_Analisis/"$(date +%Y)"/"$(date +%m)"/C"$a""$(date -u +%d%m%y)"/iSAT
mkdir -p "$caDir" && cd "$caDir"/../ && find . -maxdepth 1 -type f ! -name "1.*_latest.gif" -exec rm -rf {} +  

echo "Downloading from NHC - TAFB..."
 curl --retry 36 --retry-delay 300 -s \
      -O "https://www.nhc.noaa.gov/tafb_latest/{USA,WATL,CAR}_latest.gif" \
      -O "https://www.nhc.noaa.gov/tafb_latest/atlsfc{24,48,72}_latestBW.gif" \
      -O "https://www.nhc.noaa.gov/tafb_latest/atl{sea,24,36,48,72}_latestBW.gif"  
          rename -f 's/^/1.1.h-'$(date +%H)'./g' USA_latest.gif
          rename -f 's/^/1.2.h-'$(date +%H)'./g' WATL_latest.gif
          rename -f 's/^/1.3.h-'$(date +%H)'./g' CAR_latest.gif
          rename 's/^/2./g'   atlsfc*_latestBW.gif
          rename 's/^/3./g'   atl*_latestBW.gif
          rename 's/3.atlsea_latestBW.gif/2.atlsea_latestBW.gif/g' 3.atlsea_latestBW.gif  

echo "Downloading soundings from WY..."
 curl --retry 36 --retry-delay 300 -s \
      -O "http://weather.uwyo.edu/upperair/images/"$(date +%Y%m%d)""$hr".{78486,78954,78526}.skewt.parc.gif" 
          rename 's/^/4./g' $(date +%Y%m%d)*.skewt.parc.gif    

echo "Downloading wind derived products from SSEC..."
curl --retry 36 --retry-delay 300 -s \
       -O "http://tropic.ssec.wisc.edu/real-time/mtpw2/webAnims/tpw_nrl_colors/natl/mimictpw_natl_latest.gif" \
       -O "http://tropic.ssec.wisc.edu/real-time/sal/g16split/g16split.jpg" \
       -O "http://tropic.ssec.wisc.edu/real-time/atlantic/winds/wg8{wvir,ir,shr,sht,midshr,dvg,conv,vor,vor1,vor2,vor3}.GIF"
           rename 's/^/5./g' mimictpw_natl_latest.gif
           rename 's/^/6./g' g16split.jpg
           rename 's/^/7./g' wg8*.GIF 
           rename 's/7.wg8wvir.GIF/7.awg8wvir.GIF/g' 7.wg8wvir.GIF
           rename 's/7.wg8ir.GIF/7.awg8ir.GIF/g'     7.wg8ir.GIF

echo "Downloading global model outputs..."
curl --retry 36 --retry-delay 300 -s \
      -O "https://www.wpc.ncep.noaa.gov/mike/gfs/crb_p24i_gfs12f[024-120:12].gif" \
      -O "https://services.meteored.com/img/models/ecmwf/ECMWF_[006-120:6]_AMC1_SFC_es-ES_es.png" \
      -O "https://mag.ncep.noaa.gov/data/gfs/"$hr2"/atlantic/250_wnd_ht/gfs_atlantic_[000-120:24]_250_wnd_ht.gif" \
      -O "https://mag.ncep.noaa.gov/data/gfs/"$hr2"/atlantic/500_rh_ht/gfs_atlantic_[000-120:24]_500_rh_ht.gif" \
      -O "https://mag.ncep.noaa.gov/data/gfs/"$hr2"/atlantic/500_vort_ht/gfs_atlantic_[000-120:24]_500_vort_ht.gif" \
      -O "https://mag.ncep.noaa.gov/data/gfs/"$hr2"/atlantic/700_rh_ht/gfs_atlantic_[000-120:24]_700_rh_ht.gif" \
      -O "https://mag.ncep.noaa.gov/data/gfs/"$hr2"/atlantic/850_pw_ht/gfs_atlantic_[000-120:24]_850_pw_ht.gif" \
      -O "https://mag.ncep.noaa.gov/data/gfs/"$hr2"/atlantic/850_vort_ht/gfs_atlantic_[000-120:24]_850_vort_ht.gif"
          rename 's/^/8./g'  *_250*.gif
          rename 's/^/9./g'  *_500_rh_ht.gif
          rename 's/^/10./g' *_500_vort_ht.gif
          rename 's/^/11./g' *_700*.gif
          rename 's/^/12./g' *_850_pw_ht.gif
          rename 's/^/13./g' *_850_vort_ht.gif
          rename 's/^/14./g' *_p24i_gfs12f*.gif  
          rename 's/^/14.1/g' ECMWF*

hr3=18;
if      [ "$(date +%H)" -ge 2 -a "$(date +%H)" -le 23 ]; then 
        hr3=06;
fi
echo "Downloading HIRES output from NCEP ..."
curl --retry 36 --retry-delay 300 -s \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp24h_PR_f24_PRMEANV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp24h_PR_f24_PRAVRGV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp24h_PR_f24_PRPMMNV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp24h_PR_f24_PRLPMMV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp48h_PR_f48_PRMEANV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp48h_PR_f48_PRAVRGV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp48h_PR_f48_PRPMMNV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hrefv3/"$hr3"_exp/href_apcp48h_PR_f48_PRLPMMV3.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hiresw/pr"$hr3"/hiresw_apcp48h_PR_f48_PRARWOPS.gif"  \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hiresw/pr"$hr3"/hiresw_apcp48h_PR_f48_PRARWMEM2.gif" \
      -O "https://www.emc.ncep.noaa.gov/mmb/mpyle/hiresw/pr"$hr3"/hiresw_apcp48h_PR_f48_PRFV3.gif" 
             rename 's/^/15.1/g'  *href_apcp24h_PR_f24*.gif
             rename 's/^/15.2/g'  *href_apcp48h_PR_f48*.gif
             rename 's/^/15.2/g'  *hiresw*.gif
cd iSAT/ 
if      [ "$(date +%H)" -ge 20 -a "$(date +%H)" -le 22 ]; then 
        echo "WARNING: For satellite images update after 11:00 p.m."
else
        DATE2="$(date -u +%Y%m%d)"
        link="https://rammb.cira.colostate.edu/ramsdis/online/images/rmtc/"
        echo "Downloading satellite observation from RAMDIS..."
        curl --retry 36 --retry-delay 300 -s \
                -O ""$link"rmtcsasec4vis04/rmtcsasec4vis04_"$DATE2"["$(date -u +%H -d "-3 hour")"-"$(date -u +%H -d "-1 hour")"][00-50:10]20.gif" \
                -O ""$link"rmtcsasec4ir404/rmtcsasec4ir404_"$DATE2"["$(date -u +%H -d "-3 hour")"-"$(date -u +%H -d "-1 hour")"][00-50:10]20.gif" \
                -O ""$link"rmtcsasec4ir304/rmtcsasec4ir304_"$DATE2"["$(date -u +%H -d "-3 hour")"-"$(date -u +%H -d "-1 hour")"][00-50:10]20.gif" \
                -O ""$link"rmtcsasec4ir204/rmtcsasec4ir204_"$DATE2"["$(date -u +%H -d "-3 hour")"-"$(date -u +%H -d "-1 hour")"][00-50:10]20.gif" 
fi

echo "Files in the current folder have been updated successfully!"





