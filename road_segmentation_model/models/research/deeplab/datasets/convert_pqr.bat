set CURRENT_DIR=%CD%
set WORK_DIR=%CURRENT_DIR%\PQR
set PQR_ROOT=%WORK_DIR%\dataset
set SEMANTIC_SEG_FOLDER=%PQR_ROOT%\SegmentationClass
set OUTPUT_DIR=%WORK_DIR%\tfrecord
set IMAGE_FOLDER=%PQR_ROOT%\JPEGImages
set LIST_FOLDER=%PQR_ROOT%\ImageSets
echo "Converting PQR dataset..."
python ./build_voc2012_data.py --image_folder="%IMAGE_FOLDER%" --semantic_segmentation_folder="%SEMANTIC_SEG_FOLDER%" --list_folder="%LIST_FOLDER%" --image_format="png" --output_dir="%OUTPUT_DIR%"