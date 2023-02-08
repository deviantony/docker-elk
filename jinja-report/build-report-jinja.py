#!/usr/bin/env python3


import os
import sys
import yaml
#import shutil
import jinja2
import argparse
#from datetime import datetime
import series_models as models
from subprocess import Popen, PIPE

import doi
import plot
import users
import activity
import resources
import utilities
import organizations
import users_pie as userpie


class modules():
    module_map = {'user': users,
                  'resource': resources,
                  'organization': organizations,
                  'userpie': userpie,
                  'doi': doi,
                  'activity': activity}

    def lookup(self, type):
        return self.module_map.get(type, None)


def read_config(yaml_path):
    """
    reads yaml configuration file and returns build arguments
    """
    with open(yaml_path, "r") as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)

    # todo: insert error checking
    return yaml_data


def output_exists(cmd):
    fname = None
    wrk = ''
    for c in cmd:
        if '--filename' in c:
            fname = c.split('=')[-1]
        if '--working-dir' in c:
            wrk = c.split('=')[-1]

    if fname is not None:
        if os.path.exists(os.path.join(wrk, fname)):
            return True
    return False


def run(command):
    if output_exists(command):
        print('.. skipping bc output already exists')
        return

    cmd = [sys.executable] + command

    p = Popen(cmd, stderr=PIPE)
    while True:

        out = p.stderr.read(1).decode('utf-8', errors='ignore')
        if out == '' and p.poll() is not None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()


if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('yaml_data',
                   help='yaml configuration file')
    p.add_argument('--re-build', action='store_true', default=False,
                   help='rebuild from cache')
    args = p.parse_args()

    with open(args.yaml_data, 'r') as f:
        dat = yaml.load(f, Loader=yaml.FullLoader)

    # parse report parameters
    report_params = dat.get('report')

    # check that the input and output directories exist
    indir = os.path.join(report_params.get('input_directory'), 'data')
#    if not os.path.exists(indir):
#        print('Could not located the input directory, so I will create it '
#              f'and collect data.')
    run(['collect_data.py',
         '-s',
         '-d',
         indir,
         '--de-identify'])
    outdir = os.path.abspath(report_params['output_directory'])
    if not os.path.exists(outdir):
        print('Could not find output directory so I\'m making one: '
              f'{outdir}')
        os.makedirs(outdir)
        os.makedirs(f'{outdir}/data')
        os.makedirs(f'{outdir}/figures')

    # copy styles
    


    # loop through metrics args and parse them
    metrics = {}
    for k, v in dat.get('metrics', {}).items():
        mtype = v.pop('metric_type', None)
        if mtype is None:
            # no metric type was given, skip
            continue

        # instantiate figure
        fig_config = v.pop('figure_configuration', None)
        if fig_config is not None:
            figure = getattr(models, 'Figure')(**fig_config)
            v['figure'] = figure

        # instantiate mtype class
        _class = getattr(models, mtype)
        v['input_directory'] = indir

        metrics[k] = _class(**v)

    # loop through parsed metrics and generate figures
    mods = modules()
    data = []
    idx = 0
    for metric_name, metric_data in metrics.items():
        idx += 1
        print('\n' + '-'*50)
        print(f'Creating Figure {idx}: {metric_name}')
        print('-'*50)
        series = metric_data.get_series()
        figure_data = metric_data.figure

        # set the default figure name if it's not provided
        # in the config.yaml
        if metric_data.filename == '':
            metric_data.filename = f'{metric_name}.png'

        outpath = os.path.join(outdir, 'figures', metric_data.filename)

        plot_data = {}

        if not args.re_build:
            # generate the figure
            module = mods.lookup(metric_data.__class__.__name__)
            plots = []

            # loop through each series that will be plotted to the figure,
            # compute the data that will be displayed and create line
            # objects that will be plotted later
            for series_type, series_data in series.items():
                method = getattr(module, series_type)
                pltobj = method(**series_data)

                # some functions return a list of plot objects.
                # for these, just extend the plots list
                if type(pltobj) == list:
                    plots.extend(pltobj)
                else:
                    # if a single plot is returned (most common case),
                    # just append it to the plots list
                    plots.append(pltobj)

            # generate plot figures for each metric.
            method = getattr(plot, series_data['figure'].type)
            method(plots, outpath,
                   rcParams=metric_data.figure.rcParams,
                   axis_dict=metric_data.figure.axis,
                   figure_dict=metric_data.figure.figure)

        # initialize a dictionary of data that will be passed to the template
        template_dict = {'caption': metric_data.figure.caption,
                         'title': metric_data.figure.title,
                         'img_path': os.path.basename(outpath),
                         'img_data': None,
                         'type': 'img'}

        # set figure type if defined in config.yaml. This is necessary
        # to distinguish between raw html and images.
        if metric_data.return_type:
            template_dict['type'] = metric_data.return_type

        # save the plot data for the series in the figure
        # if indicated in the yaml configuration
        if metric_data.save_data:
            dat_path = os.path.join(outdir, 'data', f'{metric_name}.csv')

            # only save the data if the plots were created, i.e. the
            # re-build flag was not passed
            if not args.re_build:
                # save all series dataframes to the plot_data dict
                # and pass this dict to the utility function
                plot_data[dat_path] = [p.df for p in plots]

                # save plot data
                utilities.save_data_to_csv(plot_data)

            # save path to data file in the template dict so it will be
            # rendered in the report doc.
            template_dict['img_data'] = f'{metric_name}.csv'

        # append metadata for this figure that will be used to render 
        # the report later.
        data.append(template_dict)

    print('Building report html')
    Loader = jinja2.FileSystemLoader(['./templates',
                                      f'{outdir}/figures'])
    env = jinja2.Environment(loader=Loader)
    template = env.get_template('template.html')
    rpt_path = os.path.join(outdir, 'report.html')

    with open(rpt_path, 'w') as f:
        f.write(template.render(report_data=report_params, dat=data))

    print('\nReport Build Complete')
    print(f'--> report saved to {rpt_path}\n')
