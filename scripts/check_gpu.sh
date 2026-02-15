#!/bin/bash

# GPU availability checker script

echo "🔍 Checking GPU availability..."

# Check NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA drivers installed"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""
    
    # Check CUDA
    if python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())" 2>/dev/null; then
        python3 -c "import torch; print('✅ PyTorch CUDA available:', torch.cuda.is_available())"
        python3 -c "import torch; print('   Device count:', torch.cuda.device_count())"
        python3 -c "import torch; print('   Device name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
    else
        echo "⚠️  PyTorch not installed or CUDA not available"
    fi
else
    echo "❌ nvidia-smi not found - GPU may not be available"
    echo "   Inference will run on CPU (much slower)"
fi

echo ""
echo "✅ GPU check complete!"
