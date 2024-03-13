# Changes
## Fixed int math (numbers)
Also, if operation is between registers or register and number
## Fixed stringf.FloatToString
## New macros **convto**
convto float *size* [x]
convto double *size* [x]
convto int *size* [x]

convto float rax
convto double eax
convto int (rax/eax)