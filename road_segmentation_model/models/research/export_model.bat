set CURRENT_DIR=%CD%
set WORK_DIR=%CURRENT_DIR%\deeplab
set CHECKPOINT_DIR=%WORK_DIR%\datasets\PQR\exp\train\model.ckpt-30000
set EXPORT_PATH=%WORK_DIR%\datasets\PQR\exp\final_model\frozen_inference_graph.pb
python "%WORK_DIR%\export_model.py" --logtostderr --vis_split="val" --checkpoint_path="%CHECKPOINT_DIR%" --export_path="%EXPORT_PATH%" --num_classes=2 --vis_crop_size=220 --vis_crop_size=436 --model_variant="xception_65" --atrous_rates=6 --atrous_rates=12 --atrous_rates=18 --output_stride=16 --decoder_output_stride=4 --add_flipped_images=False --save_inference_graph=True --quantize_delay_step=-1 --dataset="road_dataset"