set pagination off
break inventory_total
run
printf "BREAKPOINT_HIT\n"
print inv->count
backtrace
quit
