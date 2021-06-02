#!/bin/bash

aws s3 sync s3://hcp-openaccess/HCP_1200/$1/T1w ~/scratch/HCP/stage_0/$1/T1w
