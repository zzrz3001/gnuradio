#!/usr/bin/env python
#
# Copyright 2005,2006,2007,2009 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gru, modulation_utils
from gnuradio import usrp
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

import random, time, struct, sys

# from current dir
import usrp_transmit_path
import packet_utils2

#import os 
#print os.getpid()
#raw_input('Attach and press enter')

def recode(s):
    bloop = ""
    
    #read every 8 bits, starting from index 2
    for j in range (0,len(s),8) :# = 3, j < 258, j += 8):
        res = 0;
        for i in range(0,8):
            res = 2*res + (1 if s[i+j] == '1' else 0)
            #print str[i+j]," "
            #if (s[i+j] == '1'):
            #    print "true\n", res
            #else: print "\n"
        
        bloop += chr(res);
    print bloop + "\n"
    return bloop


class my_top_block(gr.top_block):
    def __init__(self, modulator, options):
        gr.top_block.__init__(self)

        self.txpath = usrp_transmit_path.usrp_transmit_path(modulator, options)

        self.connect(self.txpath)

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

def main():

    def send_pkt(payload=None, eof=False):
        return tb.txpath.send_pkt(payload, eof)

    def rx_callback(ok, payload):
        print "ok = %r, payload = '%s'" % (ok, payload)

    mods = modulation_utils.type_1_mods()
    print "mods: ",mods

    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(),
                      default='dbpsk', #'dbpsk', need to add SNR stuff from gmsk
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(mods.keys()),))

    parser.add_option("-s", "--size", type="eng_float", default=1500,
                      help="set packet size [default=%default]")
    parser.add_option("-M", "--megabytes", type="eng_float", default=1.0,
                      help="set megabytes to transmit [default=%default]")
    parser.add_option("","--discontinuous", action="store_true", default=False,
                      help="enable discontinous transmission (bursts of 5 packets)")
    parser.add_option("","--from-file", default=None,
                      help="use file for packet contents")

    usrp_transmit_path.add_options(parser, expert_grp)

    for mod in mods.values():
        mod.add_options(expert_grp)

    (options, args) = parser.parse_args ()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    if options.tx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.from_file is not None:
        source_file = open(options.from_file, 'r')

    # build the graph
    tb = my_top_block(mods[options.modulation], options)

    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:
        print "Warning: failed to enable realtime scheduling"

    tb.start()                       # start flow graph
        
    # generate and send packets
    #nbytes = int(1e6 * options.megabytes)
    nbytes = 100
    n = 0
    pktno = 0
    pkt_size = int(options.size)
    

    f = open('/home/georgios_colleen/gnuradio/gnuradio-examples/python/digital/sent.txt', 'a')

    filedone=False
    while pktno < nbytes: #why are we limiting to 100 pkts being sent???
        print("---------------------pktno = %i, nbytes = %i--------------------"%(pktno,nbytes))
        if options.from_file is None:
            data = (pkt_size - 2) * chr(pktno & 0xff) 
        elif not(filedone):
            fromfile = source_file.read(pkt_size - 2)
            print("fromfile = %s\n"%fromfile)
            if fromfile == '':
                filedone = True
                continue
            data = fromfile#recode(fromfile)
            f.write(fromfile+"\n")
        elif len(packet_utils2.coded) > 0:
            print("CALLING WITH NO PAYLOAD")
            send_pkt(None)
            continue
        else: break #we really, truly have nothing left to send
            
        #struct.pack(fmt, v1, v2, ...)
        #Return a string containing the values v1, v2, ...
        payload = struct.pack('!H', pktno & 0xffff) + data
        print type(data)#struct.pack('!H', pktno & 0xffff)#payload
        
        send_pkt(payload)
        print("returned from send_pkt")
        n += len(payload)
        sys.stderr.write('.')
        if options.discontinuous and pktno % 10 == 9:
            time.sleep(1)
        pktno += 1

    time.sleep(3)
    print("About to send EOF")
    send_pkt(eof=True)
    
    tb.wait()                       # wait for it to finish

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
