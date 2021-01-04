set CURRENT_DIR=%CD%
set WORK_DIR=%CURRENT_DIR%\deeplab
set DATASET_DIR=datasets
set PQR_FOLDER=PQR
set EXP_FOLDER=exp
set INIT_FOLDER=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\%EXP_FOLDER%\init_models
set TRAIN_LOGDIR=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\%EXP_FOLDER%\train
set VIS_LOGDIR=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\%EXP_FOLDER%\vis
set DATASET=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\tfrecord
python "%WORK_DIR%\vis.py" --logtostderr --vis_split="val" --model_variant="xception_65" --atrous_rates=6 --atrous_rates=12 --atrous_rates=18 --output_stride=16 --decoder_output_stride=4 --vis_crop_size="220,436" --dataset="road_dataset" --checkpoint_dir="%TRAIN_LOGDIR%" --vis_logdir="%VIS_LOGDIR%" --dataset_dir="%DATASET%" --max_number_of_iterations=1
