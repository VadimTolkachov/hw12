class Test:
    
    lst = []
    def w_file(self):
        with open('test.txt', 'w') as fl:
            fl.write(str(self.lst))

    def r_file(self):
        with open('test.txt', 'r') as fl:
            result = fl.read()
        return result

    def add_lst(self, val):
        self.lst.append(val)

    def v(self):
        return self.lst
comand = Test()    
while True:
    
    inpt = input('>>>')

    if inpt.startswith('add'):
        tupl = inpt.split()
        #print(tupl[1])
        comand.add_lst(tupl[1])

    elif inpt.startswith('show'):
        tupl = inpt.split()
        print(comand.v())

    elif inpt.startswith('write'):
        tupl = inpt.split()
        print(comand.w_file())

    elif inpt.startswith('read'):
        tupl = inpt.split()
        print(comand.r_file())

