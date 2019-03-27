import time

test = []


class DataValidateModule:
    def is_real(self):
        while True:
            test.append(1)
            time.sleep(50)
            print(test)
            print('yse')


class testThd:
    def is_false(self):
        while True:
            test.append(2)
            print(test)
            print('no')
