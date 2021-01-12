# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 04:44:15 2020

@author: Adithya
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_h_cost(board):
  h = 0
  for i in range(len(board)):
    #Check every column we haven't already checked
    for j in range(i + 1,len(board)):
      #Queens are in the same row
      if board[i] == board[j]:
        h += 1
      #Get the difference between the current column
      #and the check column
      offset = j - i
      #To be a diagonal, the check column value has to be 
      #equal to the current column value +/- the offset
      if board[i] == board[j] - offset or board[i] == board[j] + offset:
          h += 1
     
  return h


print(get_h_cost([0,2,4,1,3]))