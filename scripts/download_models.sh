#!/bin/bash

# Script to download required models for inference service

set -e

MODELS_DIR="./inference_service/models"
mkdir -p "$MODELS_DIR"

echo "Downloading Stable Diffusion Inpainting model..."
python -c "
from huggingface_hub import snapshot_download
import os

models_dir = os.path.join(os.getcwd(), 'inference_service', 'models')
os.makedirs(models_dir, exist_ok=True)

# Download Stable Diffusion Inpainting
print('Downloading Stable Diffusion Inpainting...')
snapshot_download(
    repo_id='runwayml/stable-diffusion-inpainting',
    local_dir=os.path.join(models_dir, 'sd-inpainting'),
    local_dir_use_symlinks=False
)

# Download ControlNet
print('Downloading ControlNet...')
snapshot_download(
    repo_id='lllyasviel/sd-controlnet-canny',
    local_dir=os.path.join(models_dir, 'controlnet-canny'),
    local_dir_use_symlinks=False
)

print('Models downloaded successfully!')
"

echo "Downloading Whisper model..."
python -c "
import whisper
model = whisper.load_model('base')
print('Whisper model loaded and cached.')
"

echo "All models downloaded successfully!"
