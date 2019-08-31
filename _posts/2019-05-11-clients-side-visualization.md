---
layout: post
title: "Visualization in Altair"
author: "tomrod"
use_math: true
tags: [coding, visualization, craft, software ]
---

## Context
Visualization is the art in analytics. Creating charts, figures, and tables is an essential part of deriving knowledge from data. So important is this aspect of analytics that corporations have entire groups focused on *reporting*, which is the creation and delivery of summary information derived from data.

This blog has previously used static images for visualization. Lifeless, unresponsive to query, it must serve all information in a single view. We can do better! 

For interactive visualizations there are two approaches: server-side and client-side. Client-side means an entire payload is delivered with all necessary data and instructions so that a client-side application (typically a browser) can create an interactive visualization.

## Altair
Several Python packages for this exist, such as [bokeh](https://bokeh.pydata.org/en/latest/). 