import gspread
import numpy as np

gc = gspread.service_account(filename='lab2-364110-a302ae311266.json')
sh = gc.open("lab2z2test")

x = [3, 21, 22, 34, 54, 34, 55, 67, 89, 99]
x = np.array(x)
y = [2, 22, 24, 65, 79, 82, 55, 130, 150, 199]
y = np.array(y)


def model(a, b, x):
    return a * x + b


def optimize(a, b, x, y):
    num = len(x)
    prediction = model(a, b, x)
    da = (0.1 / num) * ((prediction - y) * x).sum()
    db = (0.1 / num) * ((prediction - y).sum())
    a = a - Lr * da
    b = b - Lr * db
    return a, b


def iterate(a, b, x, y, times):
    for i in range(times):
        a, b = optimize(a, b, x, y)
        return (a, b)


a = np.random.rand(10)

b = np.random.rand(10)

Lr = 0.005
a, b = iterate(a, b, x, y, 100)
prediction = model(a, b, x)

price = np.array(a+b)*100

mon = list(range(1, 10))
i = 0
while i <= len(mon):
    i += 1
    if i == 0:
        continue
    else:
        tempInf = ((price[i - 1] - price[i - 2]) / price[i - 2]) * 100
        tempInf = str(tempInf)
        tempInf = tempInf.replace('.', ',')
        sh.sheet1.update(('A' + str(i)), str(i))
        sh.sheet1.update(('B' + str(i)), str(round(price[i - 1])))
        sh.sheet1.update(('C' + str(i)), str(tempInf))
        print(tempInf)