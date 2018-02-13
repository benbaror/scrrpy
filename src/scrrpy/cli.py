"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mscrrpy` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``scrrpy.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``scrrpy.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import click

from .drr import DRR


@click.command()
@click.argument('name')
@click.argument('sma', type=click.FLOAT)
@click.argument('l_max', type=click.INT)
@click.option('--gamma', default=1.75)
@click.option('--mstar', default=1.0)
@click.option('--mbh', default=4e6)
@click.option('--rh', default=2.0)
@click.option('--threads', default=1)
@click.option('--neval', default=1e4)
@click.option('--plot', is_flag=True)
@click.option('--no_pbar', is_flag=True)
def main(name, sma, l_max, gamma, mstar, mbh, rh, threads, neval, plot,
         no_pbar):
    drr = DRR(sma, gamma=gamma, mbh_mass=mbh, star_mass=mstar, rh=rh)

    d_rr, d_err = drr(l_max, threads=threads, tol=0.0, neval=neval, progress_bar=~no_pbar)
    drr.save(name + '.hdf5')
    if plot:
        import matplotlib.pyplot as plt
        plt.errorbar(drr.j, d_rr, d_err, fmt='o')
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig(name + '.eps')
