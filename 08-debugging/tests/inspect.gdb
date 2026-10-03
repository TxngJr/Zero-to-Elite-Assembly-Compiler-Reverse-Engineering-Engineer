set pagination off
break compute_total
run
printf "COMPUTE_TOTAL_BREAK\n"
backtrace
info registers
quit
