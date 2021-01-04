set CURRENT_DIR=%CD%
set WORK_DIR=%CURRENT_DIR%\deeplab
set DATASET_DIR=datasets
set PQR_FOLDER=PQR
set EXP_FOLDER=exp
set INIT_FOLDER=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\%EXP_FOLDER%\init_models
set TRAIN_LOGDIR=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\%EXP_FOLDER%\train
set DATASET=%WORK_DIR%\%DATASET_DIR%\%PQR_FOLDER%\tfrecord
set /A NUM_ITERATIONS=30000
python "%WORK_DIR%\train.py" --logtostderr --train_split="train" --model_variant="xception_65" --atrous_rates=6 --atrous_rates=12 --atrous_rates=18 --output_stride=16 --decoder_output_stride=4 --train_crop_size="220,436" --train_batch_size=2 --dataset="road_dataset" --training_number_of_steps="%NUM_ITERATIONS%" --fine_tune_batch_norm=false --tf_initial_checkpoint="%INIT_FOLDER%/model.ckpt" --train_logdir="%TRAIN_LOGDIR%" --dataset_dir="%DATASET%" --initialize_last_layer=false --save_summaries_images=true
