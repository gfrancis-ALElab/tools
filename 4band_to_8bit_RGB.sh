img=20200818_mosaic

# gdal_contrast_stretch -percentile-range 0.01 0.99 ${img}.tif ${img}_8bit.tif
gdal_translate -scale -ot byte ${img}.tif ${img}_8bit.tif

gdal_translate -b 3 -b 2 -b 1  ${img}_8bit.tif ${img}_8bit_rgb.tif

rm ${img}_8bit.tif
