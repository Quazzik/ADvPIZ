# АНАЛИЗ ДАННЫХ И ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ [in GameDev]
Отчет по лабораторной работе #1 выполнил(а):
- Коротков Юрий Артемович
- НМТ-213901
Отметка о выполнении заданий (заполняется студентом):

| Задание | Выполнение | Баллы |
| ------ | ------ | ------ |
| Задание 1 | * | 60 |
| Задание 2 | * | 20 |
| Задание 3 | * | 20 |

знак "*" - задание выполнено; знак "#" - задание не выполнено;

Работу проверили:
- к.т.н., доцент Денисов Д.В.
- к.э.н., доцент Панов М.А.
- ст. преп., Фадеев В.О.

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Структура отчета

- Данные о работе: название работы, фио, группа, выполненные задания.
- Цель работы.
- Задание 1.
- Код реализации выполнения задания. Визуализация результатов выполнения (если применимо).
- Задание 2.
- Код реализации выполнения задания. Визуализация результатов выполнения (если применимо).
- Задание 3.
- Код реализации выполнения задания. Визуализация результатов выполнения (если применимо).
- Выводы.

## Цель работы
Ознакомиться с основными операторами зыка Python на примере реализации линейной регрессии.

## Задание 1
### Написать программы Hello World на Python и Unity
При помощи инструмента Jupiter Notebook мной была написана примитивная однострочная программа, выводящая надпись "Hello World"
Скриншот результата выполнения программы:

![image](https://user-images.githubusercontent.com/113617617/190617739-89758ba0-321c-4ed2-9efa-9d5e084751ef.png)
Код программы:
```py

print('Hello World')

```

В юнити мной был создан 2D проект, в него добавлен скрипт HelloWorld.cs (код приведен ниже), который я прикрепил к камере.
```С#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HelloWorld : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("Hello World");
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

```

Скриншот результата запуска сцены:

![image](https://user-images.githubusercontent.com/113617617/190618721-09e41eb3-dafb-4810-a48b-d4806324fda5.png)


## Задание 2
### В разделе «Ход работы» пошагово выполнить каждый пункт с описанием и примером реализации задачи по теме лабораторной работы.

В ходе выполнения следующего задания я полностью разобрал код и даже модифицировал, но для начала я переписал его из методических указаний:
```py
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

x=[3,21,22,34,54,34,55,67,89,99]
x=np.array(x)
y=[2,22,24,65,79,82,55,130,150,199]
y=np.array(y)

plt.scatter(x,y)


def model (a,b,x):
    return a*x+b

def loss_function(a,b,x,y):
    num = len(x)
    prediction = model(a,b,x)
    return (0.5/num)*(np.square(prediction-y)).sum()

def optimize(a,b,x,y):
    num = len(x)
    prediction = model(a,b,x)
    da=(0.1/num)*((prediction-y)*x).sum()
    db=(0.1/num)*((prediction-y).sum())
    a=a-Lr*da
    b=b-Lr*db
    return a,b

def iterate(a,b,x,y,times):
    for i in range(times):
        a,b = optimize(a,b,x,y)
        return(a,b)
    
a=np.random.rand(1)
print(a)
b=np.random.rand(1)
print(b)
Lr = 0.0000001
a,b = iterate(a,b,x,y,100)
prediction = model(a,b,x)
loss = loss_function(a,b,x,y)
print(a,b,loss)
plt.scatter(x,y)
plt.plot(x,prediction)
```
При выполнении кода появляется вот такой график:

![image](https://user-images.githubusercontent.com/113617617/190675340-fb4bc766-7bc2-4f6e-8c5c-31efc33f6793.png)


## Изучить код на Python и ответить на вопросы:

 - Должна ли величина loss стремиться к нулю при изменении исходных данных? Ответьте на вопрос, приведите пример выполнения кода, который подтверждает ваш ответ.

Loss будет равен нулю если входной y всегда будет равен y[i]=a*x[i]+b
Для начала введу некоторое равенство: y[i]=a*x[i]+b=y(!). И так, если разность между y(1) и y[i] будет уменьшаться, то loss тоже будет уменьшаться (стремиться к нулю). Для доказательство это я изменил входные данные так, чтобы разница между ожидаемыми и входными значениями уменьшалась и в итоге была равна нулю. Так же для удобства я установил коэффиценты a и b = 1. Ниже представлен код:
```py
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

x=[1,2,3,4,5,6,7,8,9,10]
x=np.array(x)
y=[70,60,50,40,30,7,8,9,10,11]
y=np.array(y)

plt.scatter(x,y)


def model (a,b,x):
    return a*x+b

def loss_function(a,b,x,y):
    num = len(x)
    prediction = model(a,b,x)
    return (0.5/num)*(np.square(prediction-y)).sum()

def optimize(a,b,x,y):
    num = len(x)
    prediction = model(a,b,x)
    da=(0.1/num)*((prediction-y)*x).sum()
    db=(0.1/num)*((prediction-y).sum())
    a=a-Lr*da
    b=b-Lr*db
    return a,b

def iterate(a,b,x,y,times):
    for i in range(times):
        a,b = optimize(a,b,x,y)
        return(a,b)
    
a=1
print(a)
b=1
print(b)
Lr = 0.000001
a,b = iterate(a,b,x,y,100)
prediction = model(a,b,x)
loss = loss_function(a,b,x,y)
print(a,b,loss)
plt.scatter(x,y)
plt.plot(x,prediction)
```

В ходе выполнения программы генерируется следующий график:

![image](https://user-images.githubusercontent.com/113617617/190675565-eedf2c5e-5aac-4456-8024-407f25f43195.png)

### Какова роль параметра Lr? Ответьте на вопрос, приведите пример выполнения кода, который подтверждает ваш ответ. В качестве эксперимента можете изменить значение параметра.

в ходе выполнения программы считается сумма отклонений y от предполождительного если бы точки считались по функции, а не были заданы (da,db).
a и b получают значение разности самих себя с этими отклонениями, умноженными на коэффицент Lr
Lr - "сдерживающий" коэффицент, не прозволяющим a и b прийти к нулю и, соответственно обнулить функцию.

## Выводы

Абзац умных слов о том, что было сделано и что было узнано.

За время выполнения лабораторной работы я познакомился с Unity, установил всё необходимое для дальнейшей работы ПО, научился поздавать, писать и использовать скрипты в сценах Unity, освежил навыки работы в Python, освоил базовые навыки работы в Jupiter Notepad и в Anaconda в целом.

Отдельно все файлы с кодом можно найти перейдя по [ссылке](https://github.com/Quazzik/DA-in-GameDev-lab1/tree/main/code)

## Powered by

**BigDigital Team: Denisov | Fadeev | Panov**
