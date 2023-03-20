#!/usr/bin/env python3


import sys
import shutil
from os import remove, makedirs
from os.path import abspath, join, exists
from subprocess import Popen, PIPE
from datetime import datetime
from pylatex import Document, Figure, Command
from pylatex.utils import NoEscape


# OUTPUT FIGURE NAMES
users_all_30 = 'hs-users-all-30.png'
users_all_180 = 'hs-users-all-180.png'
users_active_180 = 'hs-users-active-180.png'
users_types = 'hs_user_types.png'
users_specified = 'hs_users_specified.png'
downloads_unknown = 'hs_downloads_unknown.png'
downloads_known = 'hs_downloads_known.png'
org_all = 'hs_all_organizations.png'
org_cuahsi = 'hs_us_int_cuahsi_organizations.png'
git_open_closed = 'opened-closed.png'
git_open = 'open.png'
resource_size_total = 'hs-res-size-total.png'
resource_size_by_type = 'hs-res-size-by-type.png'
all_actions_table = 'hs-all-actions-table.png'
hs_resource_dois = 'hs-resource-dois.png'


def generate_figures(wrkdir, figdir):

    try:

        # collect data
        print('Collecting data')
        run(['collect_data.py', '-s', '-d',
              wrkdir, '--de-identify'])

        #########
        # USERS #
        #########
        print('\nGenerating %s' % users_all_30, flush=True)
        run(['users.py',
             '--working-dir=%s' % wrkdir,
             '--active-range=30',
             '--filename=%s/%s' % (figdir, users_all_30),
             '--figure-title=',
             '--step=10',
             '-tan'])

        print('\nGenerating %s' % users_all_180, flush=True)
        run(['users.py',
             '--working-dir=%s' % wrkdir,
             '--active-range=180',
             '--filename=%s/%s' % (figdir, users_all_180),
             '--figure-title=',
             '--step=10',
             '-tan'])

        print('\nGenerating %s' % users_active_180, flush=True)
        run(['users.py',
             '--working-dir=%s' % wrkdir,
             '--active-range=180',
             '--filename=%s/%s' % (figdir, users_active_180),
             '--figure-title=',
             '--step=10',
             '-anr'])

        print('\nGenerating %s' % users_types, flush=True)
        run(['users-pie.py',
             '--working-dir=%s' % wrkdir,
             '--filename=%s/%s' % (figdir, users_types),
             '--exclude=Other,Unspecified',
             '--figure-title=',
             '-p'])

        print('\nGenerating %s' % users_specified, flush=True)
        run(['users-pie.py',
             '--working-dir=%s' % wrkdir,
             '--filename=%s/%s' % (figdir, users_specified),
             '--figure-title=',
             '-c'])

        #############
        # DOWNLOADS #
        #############
        print('\nGenerating %s' % downloads_unknown, flush=True)
        run(['activity-pie.py',
             '--working-dir=%s' % wrkdir,
             '--filename=%s/%s' % (figdir, downloads_unknown),
             '--figure-title=',
             '-u'])

        print('\nGenerating %s' % downloads_known, flush=True)
        run(['activity-pie.py',
             '--working-dir=%s' % wrkdir,
             '--filename=%s/%s' % (figdir, downloads_known),
             '--figure-title=',
             '-k'])

        #################
        # ORGANIZATIONS #
        #################
        print('\nGenerating %s' % org_all, flush=True)
        run(['organizations.py',
             '--working-dir=%s' % wrkdir,
             '--agg=1D',
             '--filename=%s/%s' % (figdir, org_all),
             '--title=',
             '-a'])

        print('\nGenerating %s' % org_cuahsi, flush=True)
        run(['organizations.py',
             '--working-dir=%s' % wrkdir,
             '--agg=1D',
             '--filename=%s/%s' % (figdir, org_cuahsi),
             '--title=',
             '-uic'])

        ###########
        # ACTIONS #
        ###########
        print('\nGenerating %s' % all_actions_table, flush=True)
        run(['activity.py',
             '--working-dir=%s' % wrkdir,
             '--agg=Q',
             '--filename=%s/%s' % (figdir, all_actions_table),
             '-t'])

        #############
        # RESOURCES #
        #############
        print('\nGenerating %s' % resource_size_total, flush=True)
        run(['resources.py',
             '--working-dir=%s' % wrkdir,
             '--aggregation=1M',
             '--st=01-01-2014',
             '--filename=%s/%s' % (figdir, resource_size_total),
             '--figure-title=Cumulative Resource Size all Types (Monthly Avg)',
             '-t'])

        print('\nGenerating %s' % resource_size_by_type, flush=True)
        run(['resources.py',
             '--working-dir=%s' % wrkdir,
             '--aggregation=1M',
             '--st=01-01-2014',
             '--filename=%s/%s' % (figdir, resource_size_by_type),
             '--figure-title=Cumulative Resource Size by Type (Monthly Avg)',
             '-u'])

        ##################
        # RESOURCES DOIs #
        ##################

        print('\nGenerating %s' % hs_resource_dois, flush=True)
        run(['doi.py',
             '--working-dir=%s' % wrkdir,
             '--agg=1M',
             '--filename=%s/%s' % (figdir, hs_resource_dois),
             '--title=Number of DOIs Issued per Month',
             '--bar-width=10',
             '--annotate'
             ])

    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)


def output_exists(cmd):
    fname = None
    wrk = ''
    for c in cmd:
        if '--filename' in c:
            fname = c.split('=')[-1]
        if '--working-dir' in c:
            wrk = c.split('=')[-1]

    if fname is not None:
        if exists(join(wrk, fname)):
            return True
    return False


def run(command):
    if output_exists(command):
        print('.. skipping bc output already exists')
        return

    cmd = [sys.executable] + command

    p = Popen(cmd, stderr=PIPE)
    while True:
        out = p.stderr.read(1).decode('utf-8')
        if out == '' and p.poll() is not None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()


def create_report(wrkdir, figdir='.', report_fn='hs-metrics-report'):

    # Create document and title
    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "0.25in",
    }
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(NoEscape(r'\usepackage[section]{placeins}'))

    doc.preamble.append(NoEscape(r'\title{HydroShare Usage Metrics Report' +
                                 r'\\ \normalsize Autogenerated report ' +
                                 r'\\ \normalsize Tony Castronova ' +
                                 '<acastronova@cuahsi.org> }'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    # clean old report files
    report_tex = join(report_fn, 'tex')
    report_pdf = join(report_fn, 'pdf')
    if exists(report_tex):
        remove(report_tex)
    if exists(report_pdf):
        remove(report_pdf)

    caption = """
    This document contains figures and statistics about
    HydroShare users, their activity, and their distribution
    among domains in the community. The figures contained in
    in this document are intended to be used to understand
    the general adoption and use of the HydroShare platform.
    All data used to generate these figures are available
    in the public HydroShare metrics ElasticSearch database
    which can be found at: http://usagemetrics.hydroshare.org.
    """
    doc.append(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, users_all_30)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        (1) Total cumulative HydroShare accounts through time
        based on the date each account was created, (2) active accounts
        are defined as those that have logged into HydroShare within the
        last 30 days, and (3) new accounts defined as those
        that were created within the active range (i.e.
        the portion of active users that created an account within the
        last 30 days).
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, users_all_180)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        (1) Total cumulative HydroShare accounts
        through time based on the date each account is created,
        (2) active accounts defined as users that have logged into
        HydroShare within the last 180 days, and (3) new accounts
        defined as HydroShare accounts that were created within
        the active range (i.e. the portion of active users that
        created an account within the last 180 days).
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, users_active_180)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        (1) Active accounts defined as users that
        have logged into HydroShare within the last 180 days, (2)
        new accounts defined as HydroShare accounts that were
        created within the active range (i.e. the portion of
        active users that created an account within the last
        180 days), and (3) returning users defined as the
        portion of active users that created their account
        outside the active range.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, users_specified)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The distribution of HydroShare users that
        have defined a "user type" in their profile versus users
        that have not. User type was made a required component of
        the user profile in 2018.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, users_types)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The distribution of HydroShare users based on
        how they have defined "user type" type in their profile.
        Organization types come are defined by a controlled list, users
        that have not completed this attribute of their profile are not
        shown.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, org_all)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        Cumulative number of unique, user-specified,
        organizations represented in HydroShare. Values are
        plotted by the account creation date of the user account that
        defined the organization. In the event that an organization has
        been defined multiple times, it is associated with the first
        account that referenced it.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, org_cuahsi)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        Cumulative total of unique, user-specified,
        organizations divided into (1) US universities, (2) CUAHSI
        member institutions, and (3) international universities. Values are
        plotted by the account creation date of the user account that
        defined the organization. In the event that an organization has
        been defined multiple times, it is associated with the first
        account that referenced it.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, downloads_unknown)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        Total HydroShare resource downloads divided
        into two groups: HydroShare users and anonymous users.
        Anonymous downloads are currently possible for any public
        or published resource.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, downloads_known)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The distribution of user types for all
        downloads by known HydroShare users, i.e. the user types
        for the "HydroShare Users" subset in Figure 8. Note
        "Unspecified" is currently an option for HydroShare users
        but largely represents users that have not completed their
        profile (typically we classify these as inactive users).
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, resource_size_total)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The cumulative storage of all HydroShare resources
        plotted by the date in which the resource was created.
        These data are aggregated monthly and then summed cumulatively.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, resource_size_by_type)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The cumulative storage each resource type in
        HydroShare, plotted by the date in which they were created. These
        data are aggregated monthly and then summed cumulatively.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as fig:
        fig.add_image(abspath(join(figdir, hs_resource_dois)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The total number of digital object identifiers (DOIs)
        issued to HydroShare resources per month.
        """
        fig.add_caption(caption.replace('\n', ''))

    with doc.create(Figure(position='!htb')) as tab:
        tab.add_image(abspath(join(figdir, all_actions_table)),
                      width=NoEscape(r'\linewidth'))
        caption = """
        The total number of actions performed by HydroShare
        users aggregated quarterly. A session is a unique identity
        created by Django for storing user-specific data and they
        expire every <insert value> minutes. A login action is recorded
        every time a user account is successfully authenticated.
        Delete, create, and download actions are recorded
        whenever a user invokes one of these methods on a
        resource. App Launch is an action that is recorded
        whenever a user invokes the "Open With" functionality on a
        resource landing page.
        """
        tab.add_caption(caption.replace('\n', ''))

    # create the report
    print('Generating LaTeX Document')
    doc.generate_pdf(join(wrkdir, report_fn), clean_tex=False)
    doc.dumps()


if __name__ == '__main__':

    wrkdir = datetime.strftime(datetime.today(), '%m.%d.%Y')
    report_dir = join(wrkdir, 'tex')
    data_dir = join(wrkdir, 'data')
    report_fn = f'%s-hydroshare-metrics' % \
                datetime.strftime(datetime.today(), '%Y.%m.%d')

    fig_dir = join(wrkdir, 'fig')
    if not exists(fig_dir):
        makedirs(fig_dir)

    if not exists(report_dir):
        makedirs(report_dir)

    generate_figures(data_dir, '../fig')

    create_report(report_dir, fig_dir, report_fn=report_fn)

    pdf = f'%s.pdf' % report_fn
    shutil.move(join(report_dir, pdf),
                join(wrkdir, pdf))
