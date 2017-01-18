#!/bin/bash

# This bash script converts *dot* generated files into *png* files with the
# same name
names=(big small super_imposed)

for name in ${names[@]}; do
    dot -Tpng -o "${name}.png" "${name}.dot"
done
