class A:

    def __iter__(self): #1
        self.x = 0 #2
        return self #3

    def __next__(self): #4
        if self.x > 2:
            raise StopIteration #5
        else:
            self.x += 1
            return self.x #6


for i in A():
    print(i)
