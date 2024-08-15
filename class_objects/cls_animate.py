
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animation:
    def __init__(self, data: pd.DataFrame, column: str, title: str):
        self.data = data
        self.column = column
        self.title = title
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_title(self.title)
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel(self.column)

    def init_animation(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        x = self.data.index[:i]
        y = self.data[self.column][:i]
        self.line.set_data(x, y)
        return self.line,

    def start_animation(self, save_path=None):
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init_animation,
                                       frames=len(self.data), interval=50, blit=True)
        if save_path:
            anim.save(save_path, writer='imagemagick')
        else:
            plt.show()
