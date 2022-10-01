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
познакомиться с программными средствами для организции передачи данных между инструментами google, Python и Unity

## Задание 1
### Реализовать совместную работу и передачу данных в связке Python - Google-Sheets – Unity.
В ходе выполнения работы я создал проект в Google Cloud, где подключил API для работы с Google Sheets и создал сервисный аккаунт, через который данные отправляются в гугл-таблицу

![image](https://user-images.githubusercontent.com/113617617/193407736-d3742356-e63c-48c4-9f42-a9a84b56e507.png)

После настройки передачи данных в таблицу, был написан код на Python, который генерировал случайтые числа, которые являлись ценами, а так же рассчитывал инфляцию по этим ценам и загружал их в таблицу (код представлен ниже)

```py
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
```

После запуска программы таблица заполнилась 11-ю строками значений цен и инфляции:

![image](https://user-images.githubusercontent.com/113617617/193407826-b952264b-dd6e-4d07-b240-016e13e92dd0.png)

Далее я перешел в Юнити, создал там 3D поект, добавил на цену пустой объект и два пакета с библиотеками и звуками. После этого мной был создан скрипт, получающий из гугл-таблицы значения и анализирующий их, после чего по сценарию воспроизводящий звук в зависимости от значения инфляции и выводящий значение инфляции (код представлен ниже).

```С#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class NewBehaviourScript : MonoBehaviour
{
    public AudioClip goodSpeak;
    public AudioClip normalSpeak;
    public AudioClip badSpeak;
    private AudioSource selectAudio;
    private Dictionary<string,float> dataSet = new Dictionary<string, float>();
    private bool statusStart = false;
    private int i = 1;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GoogleSheets());
    }

    // Update is called once per frame
    void Update()
    {
        if (dataSet["Mon_" + i.ToString()] <= 10 & statusStart == false & i != dataSet.Count)
        {
            StartCoroutine(PlaySelectAudioGood());
            Debug.Log(dataSet["Mon_" + i.ToString()]);
        }

        if (dataSet["Mon_" + i.ToString()] > 10 & dataSet["Mon_" + i.ToString()] < 100 & statusStart == false & i != dataSet.Count)
        {
            StartCoroutine(PlaySelectAudioNormal());
            Debug.Log(dataSet["Mon_" + i.ToString()]);
        }

        if (dataSet["Mon_" + i.ToString()] >= 100 & statusStart == false & i != dataSet.Count)
        {
            StartCoroutine(PlaySelectAudioBad());
            Debug.Log(dataSet["Mon_" + i.ToString()]);
        }
    }

    IEnumerator GoogleSheets()
    {
        UnityWebRequest curentResp = UnityWebRequest.Get("https://sheets.googleapis.com/v4/spreadsheets/1aBabJK26hHyMOqQdhsGbuxNwiIThUYeoP_JVZQ4Jiic/values/Лист1?key=AIzaSyAKpwV3EMBmiL-9RyU2wuBfGatszeoaM_U");
        yield return curentResp.SendWebRequest();
        string rawResp = curentResp.downloadHandler.text;
        var rawJson = JSON.Parse(rawResp);
        foreach (var itemRawJson in rawJson["values"])
        {
            var parseJson = JSON.Parse(itemRawJson.ToString());
            var selectRow = parseJson[0].AsStringList;
            dataSet.Add(("Mon_" + selectRow[0]), float.Parse(selectRow[2]));
        }
    }

    IEnumerator PlaySelectAudioGood()
    {
        statusStart = true;
        selectAudio = GetComponent<AudioSource>();
        selectAudio.clip = goodSpeak;
        selectAudio.Play();
        yield return new WaitForSeconds(3);
        statusStart = false;
        i++;
    }
    IEnumerator PlaySelectAudioNormal()
    {
        statusStart = true;
        selectAudio = GetComponent<AudioSource>();
        selectAudio.clip = normalSpeak;
        selectAudio.Play();
        yield return new WaitForSeconds(3);
        statusStart = false;
        i++;
    }
    IEnumerator PlaySelectAudioBad()
    {
        statusStart = true;
        selectAudio = GetComponent<AudioSource>();
        selectAudio.clip = badSpeak;
        selectAudio.Play();
        yield return new WaitForSeconds(4);
        statusStart = false;
        i++;
    }
}
```

Пустой объект получил набор звуков и к нему был прикреплен напианный скрипт:

![image](https://user-images.githubusercontent.com/113617617/193408103-dfa8c9cf-a2d7-42c0-aaba-26eb7d21dcdc.png)

Скриншот результата запуска сцены:

![image](https://user-images.githubusercontent.com/113617617/193408135-8957ff56-be17-4064-8cc2-fc8757ddbad7.png)



## Задание 2
### Реализовать запись в Google-таблицу набора данных, полученных с помощью линейной регрессии из лабораторной работы № 1

В ходе выполнения этого задания мной был модифицирован код на Python, туда была добавлена функция линйной регрессии. Код представлен ниже:

```py
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
```

При выполнении код генерирует такой набор данных:

![image](https://user-images.githubusercontent.com/113617617/193408349-654d8206-c189-4098-b5a2-9f0d3da54c22.png)

## Задание 3
### Самостоятельно разработать сценарий воспроизведения звукового сопровождения в Unity в зависимости от изменения считанных данных в задании 2

В ходе выполнения этого задания я изменил источник данных на таблицу, в которую записываются значения из задания 2. А так же создал сценарий обработки данных (начал считать и анализировать изменение инфляции и уже в соответствии с этим изменением воспроизводил звуки), новый фрагмент кода представлен ниже:

```C#
 if (dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())] <= 5 & dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())] >= -5 & statusStart == false & i+1 != dataSet.Count)
        {
            StartCoroutine(PlaySelectAudioNormal());
            Debug.Log(dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())]);
        }

        if (dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())] > 5 & statusStart == false & i+1 != dataSet.Count)
        {
            StartCoroutine(PlaySelectAudioBad());
            Debug.Log(dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())]);
        }

        if (dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())] < -5 & statusStart == false & i+1 != dataSet.Count)
        {
            StartCoroutine(PlaySelectAudioGood());
            Debug.Log(dataSet["Mon_" + ((int)i+1).ToString()]-dataSet["Mon_"+(i.ToString())]);
        }
```
Результат запуска сцены:

![image](https://user-images.githubusercontent.com/113617617/193410191-de63920d-57cd-4f07-8c85-bdc7d3978e94.png)

## Выводы

В ходе выполнения этой работы я поздакомился с API для работы Python и C# с гугл-таблицами, научился генерировать данные в питоне и передаваь их в C#. Изучил ранее неизвестный мне парсер SimpleJSON для C#, научился создавать и настраивать гугл-таблицы, лучше изучил библиотеку numpy для питона. Так же я создал первый проект в Unity, состоящий не только из скрипта, выводящего одно сообщение при запуске, а обрабатывающий данные каждый условный тик и воспроизводящий звук в зависимости от результатов обработки

Отдельно все файлы с кодом можно найти перейдя по [ссылке](https://github.com/Quazzik/ADvPIZ/tree/lab2/code)

Таблицы:

1.[по основному коду из примера](https://docs.google.com/spreadsheets/d/1aBabJK26hHyMOqQdhsGbuxNwiIThUYeoP_JVZQ4Jiic/edit#gid=0)

2.[по модифицированному коду](https://docs.google.com/spreadsheets/d/1JATihckB993crmMbBS01OVTAWpzrDEePPzJD9LhBFbs/edit#gid=0)

## Powered by

**BigDigital Team: Denisov | Fadeev | Panov**
