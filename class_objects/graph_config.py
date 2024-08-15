import matplotlib.pyplot as plt

class GraphConfig:
    def __init__(self):
        self.reparams = {
            'axes.spines.bottom' : True,
            'axes.spines.left' : False,
            'axes.spines.right' : False,
            'axes.spines.top' : False,

            'axes.axisbelow' : True,
            'axes.linewidth' : 2,
            'axes.ymargin' : 0,
            # -- Grid

            # Enable both major and minor grid lines globally
            'axes.grid' : True,
            'axes.grid.axis' : 'y',
            'grid.color' : 'grey',
            'grid.linewidth' : 0.5,
            'grid.linestyle' : '--',

            'axes.grid.which' : 'both',   # Apply grid lines to both major and minor ticks
            'grid.alpha' : 0.5,           # Transparency of grid lines

            # Enable minor ticks globally
            'xtick.minor.visible' : True, # Show x-axis minor ticks
            'ytick.minor.visible' : True, # Show y-axis minor ticks

            # Configure minor tick parameters
            # plt.'xtick.minor.bottom'] : False # Disable minor ticks at the bottom
            # plt.'ytick.minor.left'] : False   # Disable minor ticks on the left

            # You can also set other properties like color, width, size if needed
            # For example, setting the color and width of the grid lines
            'grid.color' : 'grey',        # Color of grid lines

            # -- Ticks and tick labels --
            'axes.edgecolor' : 'grey',
            'xtick.color' : 'grey',
            'ytick.color' : 'grey',
            'xtick.major.width' : 2,
            'ytick.major.width' : 0,
            'xtick.major.size' : 5,
            'ytick.major.size' : 0,

            # -- Fonts --
            'font.size' : 16,
            #'font.family' : 'LiberationMono-Regular' #'serif'
            "font.family": "Calibri", 
            "font.weight": "light",
            'text.color' : 'grey',
            'axes.labelcolor' : 'grey',

            # -- Figure size --
            'figure.dpi' : 100,
            'figure.figsize' : (8, 4),
            
            'legend.facecolor' :'white',
            'legend.framealpha'  : 1,
            #........................................
            #OTHER
            #........................................
            # -- Saving Options --
            'savefig.bbox' : 'tight',
            'savefig.dpi' : 500,
            'savefig.transparent' : True
        }
        
        self.color_palette = {
            # Add your color palette here
        }
        self.fonts = {
            # Add your font settings here
        }
        self.markers = {
            # Add your marker styles here
        }
        self.line_styles = {
            # Add your line styles here
        }
        self.tech_type_desired_order = [
            'COAL',
            'COGENERATION',
            'COMBINED_CYCLE',
            'HYDRO',
            'DUAL_FUEL',
            'SIMPLE_CYCLE',
            'GAS_FIRED_STEAM', 
            'OTHER',
            'SOLAR', 
            'WIND', 
            'UNKNOWN',
            'ENERGY_STORAGE', 
            'TIE_LINE'
            ]
        self.tech_type_list_plus_BTF = [
        
        ]
        self.graph_types = {
            'time_series': self.plot_time_series,
            'stacked_area': self.plot_stacked_area,
            'column': self.plot_column
        }

    def apply_config(self):
        plt.rcParams.update(self.reparams)
        print("Graph configuration applied")

    def plot_time_series(self, df, x, y, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        for series in self.series_order:
            plt.plot(df[x], df[series], label=series, marker=self.markers.get(series, ''), linestyle=self.line_styles.get(series, '-'))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    def plot_stacked_area(self, df, x, y_columns, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        plt.stackplot(df[x], [df[col] for col in y_columns], labels=y_columns, colors=[self.color_palette.get(col, 'blue') for col in y_columns])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    def plot_column(self, df, x, y_columns, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        bar_width = 0.35
        for i, col in enumerate(y_columns):
            plt.bar(df[x] + i * bar_width, df[col], bar_width, label=col, color=self.color_palette.get(col, 'blue'))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    def plot_graph(self, graph_type, df, **kwargs):
        if graph_type in self.graph_types:
            self.graph_types[graph_type](df, **kwargs)
        else:
            print(f"Graph type '{graph_type}' is not supported.")
