class LpSolutionGraphAnimatedData:
    def __init__(self, quiver_data, update_callback, lines, optimal_point, frames):
        self.quiver_data = quiver_data
        self.update_callback = update_callback
        self.lines = lines
        self.optimal_point = optimal_point
        self.frames = frames
