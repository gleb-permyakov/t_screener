from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import statistics

import t

def make_nano(nano):
    nano = int(nano / 10000000)
    if int(nano / 10) == 0:
        return f"0{nano}"
    return f"{nano}"


def make_chart_candles (figi1, figi2, interval):

    from_data = "2026-02-24T16:30:00Z"
    to_data = "2026-03-24T23:00:00Z"

    # Получение исторических данных о свечках
    candles_unsorted = t.get_candles(figi1, from_data, to_data, interval)
    candles = []
    closes_arr_BTC = []

    for i in candles_unsorted:        
        candles.append( [float(f"{i["open"]["units"]}.{make_nano(i["open"]["nano"])}"), 
                         float(f"{i["close"]["units"]}.{make_nano(i["close"]["nano"])}"), 
                         float(f"{i["high"]["units"]}.{make_nano(i["high"]["nano"])}"), 
                         float(f"{i["low"]["units"]}.{make_nano(i["low"]["nano"])}"),
                         i["time"]] ) # открытие, закрытие, хай, лой свечи, время
        closes_arr_BTC.append( float(f"{i["close"]["units"]}.{make_nano(i["close"]["nano"])}")) 

    # Переносим массив точек
    line_BTC = np.array(closes_arr_BTC)
    # Среднее значение
    mean_BTC = np.mean(line_BTC)

    # параметры графика
    w = 2000
    h = 1400
    padding_btm = 120
    paddig_top = 300
    padding_rght = 400

    # параметры свечи
    space_candle = (w - padding_rght) / len(candles)
    width_candle = int(space_candle * 0.8)

    # координаты курсора
    p_x = width_candle / 2
    p_y = 0

    img = Image.new('RGB', (w, h), color = (255, 255, 255))

    # Создаем объект для рисования на изображении
    draw = ImageDraw.Draw(img)

    minmax = [100000000.0, -100000000.0]
    for i in candles:
        minmax[0] = min(minmax[0], float(i[3]))
        minmax[1] = max(minmax[1], float(i[2]))

    # Посчитаем сколько в процентах амплитуда графика биткоина
    amplituda_BTC = 1 - minmax[0]/minmax[1]

    # масштаб для отображения высоты свечи ( px / $ )
    scale = (h - padding_btm - paddig_top) / (minmax[1] - minmax[0])

    # тени свечей
    for i in candles:
        # сколько пикселей прошла цена
        delta_px = (float(i[2]) - float(i[3])) * scale
        # цвет свечи (синий)
        color = (11, 0, 58)
        # где курсор у лоя
        p_y = (h - padding_btm) - (float(i[3]) - minmax[0]) * scale 
        # Рисуем линию от точки лоя до точки хая
        draw.line([(p_x, p_y), (p_x, p_y - delta_px)], fill=color, width=2)
        # Сдвигаемся вправо на ширину свечи
        p_x += space_candle

    # новые стартовые значения курсора
    p_x = 0
    p_y = 0
    delta_px = 0

    # тела свечей
    for i in candles:
        # сколько пикселей прошло тело цены
        delta_px = (float(i[1]) - float(i[0])) * scale
        # цвет свечи
        color = (11, 0, 58)
        # где курсор у границы открытия тела
        p_y = (h - padding_btm) - (float(i[0]) - minmax[0]) * scale 
        # Рисуем тело свечи
        if delta_px >= 0: xy = [(p_x, p_y - delta_px), (p_x + width_candle, p_y)]
        else: xy = [(p_x, p_y), (p_x + width_candle, p_y - delta_px)]
        draw.rectangle(xy, fill=color, width=2)
        # Сдвигаемся вправо на ширину свечи
        p_x += space_candle

    y_end1 = p_y - delta_px

    draw.line([(p_x, y_end1), (p_x + 50, y_end1)], fill=(11, 0, 58), width=4)









    # рисуем монету рядом с битком
    candles_unsorted = t.get_candles(figi2, from_data, to_data, interval)
    # candles сохраняем тот, он нам нужен - там есть временные отметки тех свечек, которые мы записываем
    # но сами значения свечек надо подтереть
    for i in candles:
        i[0] = 0
        i[1] = 0
        i[2] = 0
        i[3] = 0
    closes_arr = []

    for i in candles_unsorted:        
        closes_arr.append( float(f"{i["close"]["units"]}.{make_nano(i["close"]["nano"])}")) 
    
    # Переносим массив точек
    line_COIN = np.array(closes_arr)
    # Среднее значение
    mean_COIN = np.mean(line_COIN)
    # Вот мы нашли коэффициент масштабирования, для того чтобы численно приравнять прайс монеты к прайсу битка
    scale_price = mean_BTC / mean_COIN

    # Масштабируем значение монетки в числах
    for i in candles_unsorted:      
        for j in candles:
            if j[4] == i["time"]:
                j[0] = float(f"{i["open"]["units"]}.{make_nano(i["open"]["nano"])}") * scale_price
                j[1] = float(f"{i["close"]["units"]}.{make_nano(i["close"]["nano"])}") * scale_price
                j[2] = float(f"{i["high"]["units"]}.{make_nano(i["high"]["nano"])}") * scale_price
                j[3] = float(f"{i["low"]["units"]}.{make_nano(i["low"]["nano"])}") * scale_price
        # candles.append( [float(f"{i["open"]["units"]}.{make_nano(i["open"]["nano"])}") * scale_price, 
        #                  float(f"{i["close"]["units"]}.{make_nano(i["close"]["nano"])}") * scale_price, 
        #                  float(f"{i["high"]["units"]}.{make_nano(i["high"]["nano"])}") * scale_price, 
        #                  float(f"{i["low"]["units"]}.{make_nano(i["low"]["nano"])}") * scale_price] ) # открытие, закрытие, хай, лой свечи
        

    # for i in candles:
    #     print(i, "\n")

    minmax = [100000000.0, -100000000.0]
    for i in candles:
        if i[0] != 0:
            minmax[0] = min(minmax[0], float(i[3]))
            minmax[1] = max(minmax[1], float(i[2]))

    # Посчитаем сколько в процентах амплитуда графика коина
    amplituda_COIN = 1 - minmax[0]/minmax[1]
        
    # Численно выравниваем значения монетки, чтобы они были похожи с битком
    # (то есть значения в долларах по коину подгоняем под значения в долларах по битку, использую их соотношение в росте/падении)
    # это надо как-то принимать либо вручную, либо еще как-то, пока пусть будет вручную
    koeff = amplituda_COIN/amplituda_BTC 
    for i in candles:
        if i[0] != 0:
            for value in range(4):
                i[value] = mean_BTC + (i[value] - mean_BTC) / koeff
       

    # Теперь можно найти отклонения значений на графике монеты от значений на графике битка 
    difference = []
    for i in range(len(candles)):
        if (candles[i][1] != 0):
            difference.append(closes_arr_BTC[i] - candles[i][1])
    
    optimal_shift = statistics.median(difference)


    # координаты курсора
    p_x = width_candle / 2
    p_y = 0

    # пересчитываем minmax с новыми значениями
    minmax = [100000000.0, -100000000.0]
    for i in candles:
        if i[0] != 0:
            minmax[0] = min(minmax[0], float(i[3]))
            minmax[1] = max(minmax[1], float(i[2]))
    
    # масштаб для отображения высоты свечи ( px / $ )
    # scale = (h - padding_btm - paddig_top) / (minmax[1] - minmax[0]) # уже не надо, т.к. масштабируемся битку

    # тени свечей
    for i in candles:
        # сколько пикселей прошла цена
        delta_px = (float(i[2]) - float(i[3])) * scale
        # смещение в пикселях относительно битка
        shift_px = optimal_shift * scale
        # цвет свечи (зеленый)
        color = (0, 56, 8)
        # где курсор у лоя
        p_y = (h - padding_btm) - (float(i[3]) - minmax[0]) * scale - shift_px
        # Рисуем линию от точки лоя до точки хая
        draw.line([(p_x, p_y), (p_x, p_y - delta_px)], fill=color, width=2)
        # Сдвигаемся вправо на ширину свечи
        p_x += space_candle

    # новые стартовые значения курсора
    p_x = 0
    p_y = 0
    delta_px = 0

    # тела свечей
    for i in candles:
        # сколько пикселей прошло тело цены
        delta_px = (float(i[1]) - float(i[0])) * scale
        # смещение в пикселях относительно битка
        shift_px = optimal_shift * scale
        # цвет свечи
        color = (0, 56, 8)
        # где курсор у границы открытия тела
        p_y = (h - padding_btm) - (float(i[0]) - minmax[0]) * scale - shift_px
        # Рисуем тело свечи
        if delta_px >= 0: xy = [(p_x, p_y - delta_px), (p_x + width_candle, p_y)]
        else: xy = [(p_x, p_y), (p_x + width_candle, p_y - delta_px)]
        draw.rectangle(xy, fill=color, width=2)
        # Сдвигаемся вправо на ширину свечи
        p_x += space_candle

    y_end2 = p_y - delta_px

    draw.line([(p_x, y_end2), (p_x + 50, y_end2)], fill=(0, 56, 8), width=4)

    print(shift_px)


    # Сохраняем изображение
    img_path = "./img.jpg"
    img.save(img_path)

    # return [round(float(koeff), 2), round(closes_arr_BTC[0], 2), round(candles[0][1], 2), (max(y_end2, y_end1) - min(y_end2, y_end1))/scale]
    # коэфф, последняя цена биток, последняя цена альта, разница в баксах делить на масштаб = разница в пикселях

    # Показываем изображение
    img.show()
