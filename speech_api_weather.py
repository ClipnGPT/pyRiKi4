#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import codecs

import subprocess

import requests
import json



# weather 天気予報
import speech_api_weather_key as weather_key



class WeatherAPI:

    def __init__(self, ):
        self.timeOut   = 10

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def getWeather(self, api, key, city, ):
        weather  = ''
        temp_max = ''
        temp_min = ''
        humidity = ''

        # openweathermap
        if (api == 'openweathermap'):
                url  = 'http://api.openweathermap.org/data/2.5/weather'
                params = {
                    'q': city.replace(' ', ''),
                    'units': 'metric',
                    'lang': 'ja',
                    'mode': 'json',
                    'appid':  key,
                    }
                try:
                    res = requests.post(url, params=params, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = res.json()
                        #print(res_json)
                        weather  = str(res_json['weather'][0]['description'])
                        temp_max = str(res_json['main']['temp_max'])
                        temp_min = str(res_json['main']['temp_min'])
                        humidity = str(res_json['main']['humidity'])
                except Exception as e:
                    pass

        return weather, temp_max, temp_min, humidity



if __name__ == '__main__':

        #tenkiAPI = weather_api.WeatherAPI()
        tenkiAPI = WeatherAPI()

        city = '三木市'

        api = 'openweathermap'
        key = weather_key.getkey(api)
        weather, temp_max, temp_min, humidity = \
            tenkiAPI.getWeather(api, key, city, )

        print(city + '、今日の天気は、「' + weather + '」です。')
        print('最高気温は、' + temp_max + '℃。')
        print('最低気温は、' + temp_min + '℃。')
        print('湿度は、' + humidity + '%です。')



