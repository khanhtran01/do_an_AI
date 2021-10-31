# a = [2,4,5,6,7]
# a.pop()
# print(a)

class point():
    def __init__(self,x,y,p) -> None:
        self.x = x
        self.y = y
        self.p = p
    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y




# if __name__ == '__main__':

v1 = [point(1,2,3), point(2,3,4)]
x = point (2,3,0)
print(v1.index(x))


