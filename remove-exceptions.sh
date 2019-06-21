#!/bin/bash
filename=$1

for i in 14 26 28 30 39 55 79 85 90 101 120 179 181 199 202 206 218 260 263 287 296 299 300 307 313 329 364 372 375 378 391 397 418 445 453 454 474 525 562 585 606 623 640 643 673 682 269
do
  printf -v patientID "%04d" $i
  echo $patientID
  sed -i "/^$patientID/d" $filename
done
