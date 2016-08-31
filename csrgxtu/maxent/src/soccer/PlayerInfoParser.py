#!/usr/bin/env python
# coding=utf-8
#
# Author: Archer Reilly
# Date: 15/Oct/2014
# File: PlayerInfoParser.py
# Description: parse the page you give, only work for stats.nba.com
# player info page.
# Website: http://csrgxtu.blog.com/
#
# Produced By CSRGXTU
from Parser import Parser

class PlayerInfoParser(Parser):
  
  def __init__(self, html):
    Parser.__init__(self, html)
  
  # getCurrentSeasonStats
  # get the current season stats data, like ["6.6", "6.8", "0.5", "10.1%"]
  #
  # @return recs in list format or None
  def getCurrentSeasonStats(self):
    xpathExp = ''
    recs = self.getTree().xpath(xpathExp);
    if len(recs) != 4:
      return None
    else:
      return recs
