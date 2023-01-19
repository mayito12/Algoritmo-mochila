class Individuo:
    def __init__(self, packages) -> None:
        self.packages = packages
        self.total_space = 0
        self.profit_ind = 0
        self.valid_range = 0

    def __repr__(self) -> str:
        return repr((self.packages, self.total_space, self.profit_ind, self.valid_range))
