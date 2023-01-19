class Package: 
    def __init__(self,name, space, cost, price, profit) -> None:
        self.name = name
        self.space = space
        self.cost = cost
        self.price = price
        self.profit = profit

    def __repr__(self):
        return repr((self.name, self.space, self.cost, self.price, self.profit))