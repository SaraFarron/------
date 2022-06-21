## Диплом
Исследование алгоритма вычисления ионосферной поправки для системы Galileo.

## Добавить в диплом
Фазовые измерения точнее, но есть проблема что не понятно сколько длин волн уложится
фаза - насколько сигнал завхватили корреляторов и насколько он сигнал

## Комбинации


1


2
С09, csv - 04, l1
```
    t, nqa = t[1700:], nqa[1700:]
    x, y = x[35:], y[35:]
```

3
C10, csv - 04, l1
```
    t, nqa = t[:-2000], nqa[:-2000]
    x, y = x[:-370], y[:-370]
```

4
E01, csv - 04, l1
```
    t, nqa = t[1400:-1100], nqa[1400:-1100]
    x, y = x[:-350], y[:-350]
```

## Таска

Сделать измерения за неделю, считаем разницу между неквиком и иземернием и считаем матожидание и сигму

Маспроизводство PPPH
Брать только спутники из галилео

## Ссылки

[cord converter](https://tool-online.com/en/coordinate-converter.php)

[link from prof](https://vk.com/away.php?utf=1&to=http%3A%2F%2Fgdc.cddis.eosdis.nasa.gov%3A21%2Fpub%2Fgps%2Fdata%2Fdaily%2F2021%2F001%2F21l%2FABPO00MDG_R_20210010000_01D_EN.rnx.gz)

[check cords](https://www.gps-coordinates.net/)

[sp3 description](http://www.epncb.oma.be/ftp/data/format/sp3c.txt)

[юзать l типы файлов версии 3](https://cddis.nasa.gov/archive/gnss/data/daily/2021/001/21l/)

[web nequick](https://t-ict4d.ictp.it/nequick2/nequick-2-web-model)

[Нормальное описание формата ринекса для галилео](https://www.gsc-europa.eu/gsc-products/galileo-rinex-navigation-parameters)

[для ринекс 2](https://files.igs.org/pub/data/format/)

[ссылка с датой (нужна регистрация)](https://cddis.nasa.gov/archive/gnss/data/daily/)

[предположительно atx для всего](https://www.ngs.noaa.gov/ANTCAL/LoadFile?file=ngs14.atx)

[конвертер кордов](https://www.ngs.noaa.gov/TOOLS/XYZ/xyz.shtml)

## Алгоритм измерений
Взять корды и ионосферные коэфы из ринекса -> Перевод в blh -> NeQuick -> Перевод в задержку -> Графики
Взять корды из sp3 -> провернуть в PPPH -> Перевод в blh -> NeQuick -> Перевод в задержку -> Графики
Взять псевдодальности из о файла -> взять сдвиг из dcb -> Посчитать задержку -> Графики

## 
