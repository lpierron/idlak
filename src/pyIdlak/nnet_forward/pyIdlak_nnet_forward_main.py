#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Cereproc Ltd. (author: Skaiste Butkute)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
# WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.
# See the Apache 2 License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import argparse
import textwrap
from nnet_forward import nnet_forward as nnet_fwd


def tobool(prop):
    if prop and prop.lower() == "true":
        prop = True
    else:
        prop = False
    return prop


def main():
    descrp = '''\
Perform forward pass through Neural Network
Usage: pyIdlak-nnet-forward-main.py [options] <nnet1-in> <feature-rspecifier> \
<feature-wspecifier>
e.g.: pyIdlak-nnet-forward-main.py final.nnet ark:input.ark ark:output.ark
'''
    formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=descrp,
                                     formatter_class=formatter)
    parser.add_argument('--class-frame-counts', help='Vector with frame-' +
                        'counts of pdfs to compute log-priors. (priors are ' +
                        'typically subtracted from log-posteriors or ' +
                        'pre-softmax activations)', default='')
    parser.add_argument('--prior-scale', help='Scaling factor to be ' +
                        'applied on pdf-log-priors', default=1.0, type=float)
    parser.add_argument('--prior-floor', help='Flooring constatnt for prior ' +
                        'probability (i.e. label rel. frequency)',
                        default=1e-10, type=float)
    parser.add_argument('--feature-transform', help='Feature transform in ' +
                        'front of main network (in nnet format)', default='')
    parser.add_argument('--reverse-transform', help='Feature transform ' +
                        'applied in reverse on output')
    parser.add_argument('--no-softmax', help='Removes the last component ' +
                        'with Softmax, if found. The pre-softmax activations' +
                        ' are the output of the network. Decoding them ' +
                        'leads to the same lattices as if we had used ' +
                        "'log-posteriors'. in reverse on output")
    parser.add_argument('--apply-log', help='Transform NN output by log()')
    parser.add_argument('--use-gpu', help='only has effect if compiled with ' +
                        ' CUDA', choices=['no', 'yes', 'optional'],
                        default='no')
    parser.add_argument('nnet1_in', nargs=1)
    parser.add_argument('feature_rspecifier', nargs=1)
    parser.add_argument('feature_wspecifier', nargs=1)
    args = parser.parse_args()

    nnet_fwd(args.nnet1_in[0], args.feature_rspecifier[0],
             args.feature_wspecifier[0], args.class_frame_counts,
             args.prior_scale, args.prior_floor, args.feature_transform,
             tobool(args.reverse_transform), tobool(args.no_softmax),
             tobool(args.apply_log), args.use_gpu)


if __name__ == '__main__':
    main()
