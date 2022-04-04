 #! /bin/bash

echo "Iniciando..."

if      [ "$(date +%H)" -ge 20 -a "$(date +%H)" -le 23 ]; then 
        a='A'; hr=00; stn="78486,78954,78526"; DATE="$(date +%d%m%y -d "+1 day")"; hr2=18
 elif   [ "$(date +%H)" -ge 00 -a "$(date +%H)" -le 07 ]; then 
  	    a='A'; hr=00; stn="78486,78954,78526"; DATE="$(date +%d%m%y)"; hr2=18
 elif   [ "$(date +%H)" -ge 08 -a "$(date +%H)" -le 13 ]; then 
  	    a='B'; hr=12; stn="78954,78486,78526"; DATE="$(date +%d%m%y)"; hr2=06
 elif   [ "$(date +%H)" -ge 14 -a "$(date +%H)" -le 19 ]; then
        a='C'; hr=12; stn="78954,78486,78526"; DATE="$(date +%d%m%y)"; hr2=12
fi

date
echo "Moviendose a la carpeta correspondiente..."

cd ~/Desktop/Carpeta_de_Analisis/"$(date +%Y)"/"$(date +%m)"/C"$a""$DATE"/

echo "Escribiendo en las imagenes tdqpf..."

for i in `ls -l | grep "14.crb_" | sed -r 's/\s+/,/g' | cut -d"," -f9`
do
	j=`echo "$i" | cut -d"_" -f3 | cut -d"." -f1` && k="${j:6:3}"  #Expansion Parameter
	convert "$i" -fill red -gravity South -pointsize 60 \
	-annotate +0+100 "$k HORAS" ~/Desktop/drag_folder/coopre/temp_files/temp_"$k".png   
	# convert -font helvetica -fill black -pointsize 60 -gravity center \
    # -draw "text 0,350 'TEXT TO BE DISPLAYED'" Screenshot_2019-05-29_08-42-51.png ex_2.png
done

echo "Generando GIF tdqpf.gif..."

convert -delay 350 -loop 0 ~/Desktop/drag_folder/coopre/temp_files/temp_* \
~/Desktop/drag_folder/coopre/tdqpf.gif
rm -rf ~/Desktop/drag_folder/coopre/temp_files/*

echo "tdqpf.gif creado con exito!"

echo "Escribiendo en las imagenes ecmwfqpf..."

for i in `ls -l | grep "14.1ECMWF" | sed -r 's/\s+/,/g' | cut -d"," -f9`
do
	j=`echo "$i" | cut -d"_" -f2` 
	convert "$i" -fill red -gravity South -pointsize 60 \
	-annotate +0+100 "$j HORAS" ~/Desktop/drag_folder/coopre/temp_files/temp_2_"$j".png  
done

echo "Generando GIF ecmwfqpf.gif..."

convert -delay 350 -loop 0 ~/Desktop/drag_folder/coopre/temp_files/temp_2_* \
~/Desktop/drag_folder/coopre/ecmwfqpf.gif
rm -rf ~/Desktop/drag_folder/coopre/temp_files/*

echo "ecmwfqpf.gif creado con exito!"



# echo "Moviendose a la carpeta correspondiente..."
# cd ~/Desktop/Carpeta_de_Analisis/"$(date +%Y)"/"$(date +%m)"/C"$a""$DATE"/iSAT/

# echo "Escribiendo en las imagenes  rcs..."

# for i in `ls -l | sed -r 's/\s+/,/g' | cut -d"," -f9`
# do
# 	j=`echo "$i" | cut -d"_" -f2 | cut -d"." -f1`
# 	convert "$i" -fill red -gravity South -pointsize 60 \
# 	-annotate +0+100 "$j" ~/Desktop/drag_folder/coopre/temp_files/temp_3_"$j".gif  
# done

# echo "Generando GIF rcs.gif..."

# convert -delay 5 -loop 0 ~/Desktop/drag_folder/coopre/temp_files/*.gif \
# ~/Desktop/drag_folder/coopre/rcs.gif

# rm -rf ~/Desktop/drag_folder/coopre/temp_files/*

# echo "rcs.gif creado con exito!"
date