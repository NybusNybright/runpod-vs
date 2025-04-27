#!/bin/bash

bash -c '
echo "🔧 Starting setup sequence..."

SCRIPT_DIR=/workspace/setup/scripts/

bash $SCRIPT_DIR//install_packages.sh
bash $SCRIPT_DIR/setup_comfy.sh
bash $SCRIPT_DIR/setup_sd_webui.sh
# bash $SCRIPT_DIR/setup_symlinks.sh
bash $SCRIPT_DIR/launch_services.sh

echo "✅ Setup complete!"
'
