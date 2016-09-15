'''
Author: geronm@mit.edu

This is a script to grab fields from LCM channels and write them to ascii files.

'''
import sys
import time
import random

import lcm

USAGE = \
'''
USAGE: lcm_writer output_file(!) channel_name lcmtype_path msg_field_expr [package]

Example:
  lcm_writer my_output.asc EST_ROBOT_STATE drc.robot_state_t msg.pose.translation
  lcm_writer my_output.asc LCM_SPEWER drc.position_3d_t msg.translation.x drc
'''

args = sys.argv
if len(args) < 1+4 or len(args) > 1+5:
  print(USAGE)
  sys.exit(1)
elif len(args) == 1+5:
  exec 'import ' + sys.argv[5]


out_filename = sys.argv[1]
listen_channel = sys.argv[2]
lcmtype_str = sys.argv[3]
field_expr_str = sys.argv[4]


lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')

out_file = open(out_filename,'w')

print 'LCM Writer Setup Success.  Writing to file ' + out_filename + '...'

PRINT_LIMIT_SECONDS = 0.1
last_time = time.time()

try:
    def handler(channel, data):
        global last_time
        cur_time = time.time()

        if cur_time - last_time > PRINT_LIMIT_SECONDS:
            print('Received..')
            last_time = time.time()
        
        msg = eval(lcmtype_str + '.decode(data)')
        field = eval(field_expr_str)
        out_file.write(str(field) + '\n')


    lc.subscribe(listen_channel, handler)
    while(True):
        lc.handle()
except KeyboardInterrupt:
    out_file.close()
    print 'KeyboardInterrupt detected.  Writer Terminated'    

