#!/usr/bin/env python3

import os


def build_latex_pdf(fname, outdir):
    try:
        code = os.system('pdflatex --version  >/dev/null 2>&1')
        if code != 0:
            print('PdfLatex is not installed')
        os.system('pdflatex -output-directory=%s %s  >/dev/null 2>&1' % (outdir, fname))
        os.remove('%s.log' % fname[:-4])
        os.remove('%s.aux' % fname[:-4])
    except:
        print('Error building latex: %s' % fname)


def write_table(fname,
                dat,
                index_list,
                fmt,
			    lcol,
                pdfwidth=200,
                pdfheight=55,
                hoffset=-45,
                voffset=-40):

    num_cols = len(dat.columns)
    # write header info
    txt = ('\\documentclass{article}\n'
           '\\setlength{\\pdfpagewidth}{%dmm}\n'
           '\\setlength{\\pdfpageheight}{%dmm}\n'
           '\\addtolength{\\hoffset}{%dmm}\n'
           '\\addtolength{\\voffset}{%dmm}\n'
           '\\begin{document}\n'
           '\\begin{table}[ht]\n'
           '\\centering\n'
           '\\begin{tabular}{l%s}\n'
           '\\hline\n' % (pdfwidth,
                          pdfheight,
                          hoffset,
                          voffset, 'r'*num_cols))

    txt += '%s & %s \\\\ \\hline\n' % (lcol, '&'.join(dat.columns))

    for u in index_list:
        if u in dat.index:
            data = dat.loc[u].values
            fmt_data = [fmt[i] % data[i] for i in range(0, len(data))]
            txt += '%s & %s \\\\ \n' % (u, '&'.join(fmt_data))
    txt += ('\\hline\n'
            '\\end{tabular}\n'
            '\\end{table}\n'
            '\\end{document}\n')

    with open(fname, 'w') as f:
        f.write(txt)

    return fname





def build():
    pass
