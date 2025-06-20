#!/bin/bash

INPUT_DIR="data/input"
TOML_OUTPUT_DIR=".."
EXEC="./build/src/clue_alpaka/mainAlpaka"

for file in "$INPUT_DIR"/*_1000.csv; do
    echo "Running on: $file"
    
    $EXEC -i "$file" -d 25.0 -r 20.0 -o 5.0 -e 100000 -v -u GpuCuda
    
    if [ -f "$TOML_OUTPUT_DIR/clue.toml" ]; then
        base_name=$(basename "$file" .csv)
        mv "$TOML_OUTPUT_DIR/clue.toml" "$TOML_OUTPUT_DIR/${base_name}.toml"
        echo "Renamed clue.toml to ${base_name}.toml"
    else
        echo "Warning: clue.toml not found after processing $file"
    fi

    echo
done
