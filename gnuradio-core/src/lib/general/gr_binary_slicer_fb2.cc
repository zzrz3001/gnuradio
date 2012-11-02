/* -*- c++ -*- */
/*
 * Copyright 2006,2010 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gr_binary_slicer_fb2.h>
#include <gr_io_signature.h>
#include <stdexcept>
#include <iostream>

using namespace std;

static float error [222];
static int bits [222];
static float SNR = 0;

gr_binary_slicer_fb2_sptr
gr_make_binary_slicer_fb2 ()
{
  return gnuradio::get_initial_sptr(new gr_binary_slicer_fb2 ());
}

gr_binary_slicer_fb2::gr_binary_slicer_fb2 ()
  : gr_sync_block ("binary_slicer_fb2",
		   gr_make_io_signature (1, 1, sizeof (float)),
		   gr_make_io_signature (1, 1, sizeof (unsigned char)))
{
}


int
insert(int x){
  int p_sig = x*x;
  for (int i = 0; i < 221; i++){
    bits[i+1] = bits[i];
    p_sig += bits[i+1]*bits[i+1];
  }
  bits[0] = x;
  return p_sig;
}

float
insert(float x){
  float p_noise = x*x;
  for (int i = 0; i < 221; i++){
    error[i+1] = error[i];
    p_noise += error[i+1]*error[i+1];
  }
  error[0] = x;
  return p_noise;
}


static inline int
slice(float x)
{

  // 0 = -1, 1 = 1? 0 value is a bit suspect...
  //assuming a repeating code.
  //should SNR still analyze bitwise?
  //cout << "rcvd bit: " <<  x << "\n";
  int decision = x < 0 ? 0 : 1;
  float error = x < 0 ? (1+x ): (1-x);
  SNR = (float)insert(1)/insert(error);
  return decision;
}

int
gr_binary_slicer_fb2::work (int noutput_items,
			   gr_vector_const_void_star &input_items,
			   gr_vector_void_star &output_items)
{
  const float *in = (const float *) input_items[0];
  unsigned char *out = (unsigned char *) output_items[0];


  for (int i = 0; i < noutput_items; i++){
    out[i] = slice(in[i]);
  }
  
  return noutput_items;
}

float 
gr_binary_slicer_fb2::snr(void){
  return SNR;
}
