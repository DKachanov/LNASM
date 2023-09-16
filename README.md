# Project LNASM
## About LNASM
LNASM project provides simple macros for NASM.

## LNASM syntax
LNASM syntax is described in "base syntax.txt".
You can also look for examples in examples/*.lnasm

## Translate to NASM code
To translate to NASM you need to execute this command:

"python3 *path_to_LNASM*/main.py --name *your_file* --outfile *outfile_name*"

### Auto compile NASM code to elf64

If you want compile NASM code append to the command "--translateToElf64Program True"
(NASM and ld must be installed)
