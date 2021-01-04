CURRENT_DIR=$(pwd)
WORK_DIR="./PQR"
PQR_ROOT="${WORK_DIR}/dataset"
SEG_FOLDER="${PQR_ROOT}/SegmentationClass"
SEMANTIC_SEG_FOLDER="${PQR_ROOT}/SegmentationClassRaw"
# Build TFRecords of the dataset.
OUTPUT_DIR="${WORK_DIR}/tfrecord"
mkdir -p "${OUTPUT_DIR}"
IMAGE_FOLDER="${PQR_ROOT}/JPEGImages"
LIST_FOLDER="${PQR_ROOT}/ImageSets"
echo "Converting PQR dataset..."
python ./build_new_pqr_data.py \
  --image_folder="${IMAGE_FOLDER}" \
  --semantic_segmentation_folder="${SEMANTIC_SEG_FOLDER}" \
  --list_folder="${LIST_FOLDER}" \
  --image_format="jpg" \
  --output_dir="${OUTPUT_DIR}"