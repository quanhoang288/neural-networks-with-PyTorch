from IPython import display
from matplotlib import pyplot as plt

def set_svg_display():
    display.set_matplotlib_formats('svg')

def set_figsize(figsize=(3.5, 2.5)):
    set_svg_display()
    plt.rcParams['figure.figsize'] = figsize

def set_axes(axes, xlabel, ylabel, xlim, ylim, xscale, yscale, legend):
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    if legend:
        axes.legend(legend)
    axes.grid()

class RealTimeVisualizer(object):
    def __init__(self, xlabel=None, ylabel=None, legend=None, xlim=None,
                 ylim=None, xscale='linear', yscale='linear', fmts=None,
                 figsize=(4.5, 3.5)):
        """Incrementally plot multiple lines."""
        self.legend = [] if legend is None else legend
        set_svg_display()

        self.fig, self.axes = plt.subplots(1, 1, figsize=figsize)
        self.xlabel, self.ylabel = xlabel, ylabel
        self.xlim, self.ylim = xlim, ylim
        self.xscale, self.yscale = xscale, yscale

        self.X, self.Y, self.fmts = None, None, fmts

    def config_axes(self):
        set_axes(self.axes, self.xlabel, self.ylabel, self.xlim, self.ylim,
                 self.xscale, self.yscale, self.legend)

    def add_point(self, x, y):
        """
        Plot points of multiple metrics (typically 3)
        :param x: epoch
        :param y: list or tuple of 3 metrics. `self.Y` is 3 lists of the 3 metrics. We plot them simultaneously.
        """
        if not hasattr(y, "__len__"):
            y = [y]
        n = len(y)
        if not hasattr(x, "__len__"):
            x = [x] * n

        if self.X is None:
            self.X = [[] for _ in range(n)]
        if self.Y is None:
            self.Y = [[] for _ in range(n)]
        if self.fmts is None:
            self.fmts = ['-'] * n

        # Append metrics which are not None to `self.Y`
        for i, (a, b) in enumerate(zip(x, y)):
            if a is not None and b is not None:
                self.X[i].append(a)
                self.Y[i].append(b)
        self.axes.cla()

        for x, y, fmt in zip(self.X, self.Y, self.fmts):
            self.axes.plot(x, y, fmt)

        self.config_axes()
        display.display(self.fig)
        display.clear_output(wait=True)