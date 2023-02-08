#!/usr/bin/env python3 

import os
import pytz
import math
import numpy
import pandas
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import cm

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class PlotObject(object):
    def __init__(self, x, y,
                 dataframe=None,
                 label='',
                 color='b',
                 linestyle='-'):
        self.x = x
        self.y = y
        self.label = label
        self.linestyle = linestyle
        self.color = color
        self.dataframe = dataframe

    @property
    def df(self):
        if self.dataframe is None:
            _df = pandas.DataFrame(self.y, index=self.x, columns=[self.label])
            _df.index = pandas.to_datetime(_df.index)
            return _df
        return self.dataframe


def line(plotObjs_ax1,
         filename,
         axis_dict={},
         figure_dict={},
         rcParams={},
         **kwargs):
    """
    Creates a figure give plot objects
    plotObjs: list of plot object instances
    filename: output name for figure *.png
    **kwargs: matplotlib plt args, e.g. xlabel, ylabel, title, etc
    """

    print('--> making figure...')

    # set global plot attributes
    if rcParams != {}:
        plt.rcParams.update(rcParams)

    # create figure of these data
    fig, ax = plt.subplots()
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)

    annotate = figure_dict.pop('annotate_series', False)
    annotate_legend = figure_dict.pop('annotate_legend', False)
    for pobj in plotObjs_ax1:
        label = pobj.label

        if annotate_legend:
            label = f'{label} ({pobj.y.max()})'

        ax.plot(pobj.x, pobj.y,
                color=pobj.color,
                linestyle=pobj.linestyle,
                label=label)

        # annotate the last point
        if annotate:
            ax.text(pobj.x[-1] + timedelta(days=5), # x-loc
                    pobj.y[-1], # y-loc
                    int(round(pobj.y[-1], 0)), # text value
                    bbox=dict(boxstyle='square,pad=0.5',
                              fc='none', # foreground color
                              ec='none', # edge color
                              ))

    # turn on the grid
    if figure_dict.pop('grid', False):
        ax.grid()

    # add a legend
    if figure_dict.pop('legend', False):
        plt.legend()

    # add monthly minor ticks
    months = mdates.MonthLocator()
    ax.xaxis.set_minor_locator(months)

    # set plot attributes
    for k, v in axis_dict.items():
        # eval if string is a tuple
        if '(' in v:
            v = eval(v)
        getattr(ax, 'set_'+k)(v)

    for k, v in figure_dict.items():
        getattr(plt, k)(v)


#    for k, v in text_dict.items():
#        getattr(ax, k)(v)

    # save the figure and the data
    plt.savefig(filename)
    print(f'--> figure saved to: {filename}')



def bar(plotObjs_ax1,
        filename,
        width=10,
        axis_dict={},
        figure_dict={},
        rcParams={},
        **kwargs):

#        title='',
#              agg='1M', width=.5, annotate=False,
#              **kwargs):

    print('--> making figure...')
    
    # set global plot attributes
    if rcParams != {}:
        plt.rcParams.update(rcParams)

    # create figure of these data
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)

    annotate = figure_dict.pop('annotate_series', False)
    for pobj in plotObjs_ax1:
        ax.bar(pobj.x,
               pobj.y,
               width=float(width),
               color=pobj.color)

        if annotate:
            for p in ax.patches:
                height = p.get_height()
                if height > 0:
                    ax.annotate("%d" % height,
                                (p.get_x() + p.get_width() / 2.,
                                 height),
                                ha='center',
                                va='center',
                                xytext=(0, 10),
                                textcoords='offset points')

    # add monthly minor ticks
    months = mdates.MonthLocator()
    ax.xaxis.set_minor_locator(months)

    # set plot attributes
    for k, v in axis_dict.items():
        # eval if string is a tuple
        if '(' in v:
            v = eval(v)
        getattr(ax, 'set_'+k)(v)

    for k, v in figure_dict.items():
        getattr(plt, k)(v)

    # save the figure and the data
    plt.savefig(filename)
    print(f'--> figure saved to: {filename}')


def pie(plotObjs_ax1,
        filename,
        axis_dict={},
        figure_dict={},
        rcParams={},
        **kwargs):

    print('--> making figure...')

    # set global plot attributes
    if rcParams != {}:
        plt.rcParams.update(rcParams)

    # create figure of these data
    fig, ax = plt.subplots()

    # remove figure configs from the figure_dict to avoid issues when
    # setting valid attributes later on
    legend = figure_dict.pop('legend', False)
    label_threshold = figure_dict.pop('label_threshold', 0)
    for pobj in plotObjs_ax1:
        # place annotations on pie slices
        if not legend:
            plt.subplots_adjust(left=0.1, right=0.5, bottom=.02)

            #df = pobj.df[pobj.label].sort_values(ascending=False).reindex()
            df = pobj.df[pobj.label]
            wedges = []
            labels = []

            while len(df) > 0:
                # select high value
                max_val = df.max()
                idx = df[df.values == max_val].index[0]
                df.drop(idx, inplace=True)
                wedges.append(max_val)
                if max_val < label_threshold:
                    labels.append(None)
                else:
                    labels.append(idx)

                if len(df) == 0:
                    break

                # select low value
                min_val = df.min()
                idx = df[df.values == min_val].index[0]
                df.drop(idx, inplace=True)
                wedges.append(min_val)
                if min_val < label_threshold:
                    labels.append(None)
                else:
                    labels.append(idx)

            wedges, texts = ax.pie(wedges, wedgeprops=dict(width=0.5),
                                   startangle=-50)


            bbox_props = dict(boxstyle="square,pad=0.1",
                              fc="w",
                              ec="none",
                              lw=0.72,
                              pad=10)
            kw = dict(arrowprops=dict(arrowstyle="-"),
                 bbox=bbox_props, zorder=0, va="center")

            for i, p in enumerate(wedges):
                if labels[i] is None:
                    continue
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = numpy.sin(numpy.deg2rad(ang))
                x = numpy.cos(numpy.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(numpy.sign(x))]
                connectionstyle = "angle,angleA=0,angleB={}".format(ang)
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                ax.annotate(labels[i], xy=(x, y), xytext=(1.35*numpy.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

        # remove all annotations except within legend
        else:
            for col in pobj.df.columns:
                pobj.df[col].plot(kind='pie', ax=ax, labels=None)
                ax.legend(
                          labels=pobj.df.index,
                          bbox_to_anchor=(1.25, 0),
                          ncol=2)

    plt.tight_layout()

    # set plot attributes
    for k, v in axis_dict.items():
        # eval if string is a tuple
        if '(' in v:
            v = eval(v)
        getattr(ax, 'set_'+k)(v)

    for k, v in figure_dict.items():
        getattr(plt, k)(v)

    # save the figure and the data
    plt.savefig(filename)
    print(f'--> figure saved to: {filename}')

def table(plotObjs_ax1,
          filename,
          axis_dict={},
          figure_dict={},
          rcParams={},
          **kwargs):

    print('--> making figure...')

    # set global plot attributes
    if rcParams != {}:
        plt.rcParams.update(rcParams)

    # create figure of these data
    fig, ax = plt.subplots()
   
    # right now this only supports a single plot object
    # TODO: align this functionality with the other plot
    # functions.
    plotObj = plotObjs_ax1[0]

    # get the data that will be populated in the table
    df = plotObj.df

    # set column widths
    column_widths = [.1] * len(df.columns)

    # build the table object
    table = ax.table(rowLabels=df.index, cellText=df.values,
                     colLabels=df.columns, colWidths=column_widths,
                     loc='center')
    # set font size
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1, 4)

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    print('--> saving figure as %s' % filename)

    plt.tight_layout()

    # set plot attributes
    for k, v in axis_dict.items():
        # eval if string is a tuple
        if '(' in v:
            v = eval(v)
        getattr(ax, 'set_'+k)(v)

    for k, v in figure_dict.items():
        getattr(plt, k)(v)

    # save the figure and the data
    plt.savefig(filename)
    print(f'--> figure saved to: {filename}')


def table_html(plotObjs_ax1,
               filename,
               axis_dict={},
               figure_dict={},
               rcParams={},
               **kwargs):


    print('--> making html table...')

    df = plotObjs_ax1[0].df
    html = df.to_html()

    with open(filename, 'w') as f:
        f.write(html)

    print(f'--> table saved to: {filename}')
