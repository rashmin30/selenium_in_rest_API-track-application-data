from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from time import *
from selenium.webdriver.common.by import By
import requests
from threading import Thread


# Create your views here.


class WebScraping(APIView):
    def get(self, request, format=None):
        app_details = []

        def craping(**i):
            print(i)
            driver = webdriver.Chrome()
            driver.get(
                f"https://play.google.com/store/apps/details?id={i['package_name']}")
            sleep(3)
            try:
                driver.find_element(
                    By.XPATH, "//*[@id='yDmH0d']/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button/i").click()
                sleep(1)
                version = driver.find_element(
                    By.XPATH, "//*[@id='yDmH0d']/div[4]/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div[2]")
                last_update_date = driver.find_element(
                    By.XPATH, "//*[@id='yDmH0d']/div[4]/div[2]/div/div/div/div/div[2]/div[3]/div[2]/div[2]")
                if version.text != i['app_version']:
                    app_details.append({
                        "package_name": i['package_name'],
                        "update_date": last_update_date.text,
                        "play_version": version.text,
                        "old_version": i['app_version'],
                        "app_url": driver.current_url
                    })
            except:
                app_details.append({
                    "package_name": i['package_name'],
                    "update_date": '',
                    "play_version": '',
                    "old_version": i['app_version'],
                    "app_url": driver.current_url
                })
            driver.quit()
        URL = 'https://developer.kartavyainfotech.com/api/dev/getfavapplistbydate'
        body = {
            "date": "Total"
        }
        header = {
            "app_key": "5N6Q8R9SBUCVDXFYGZH3K4M5P7Q8RATBUCWEXFYH2J3K5N6P7R9SATCVDW"
        }
        r = requests.post(url=URL, headers=header, data=body)
        if r.status_code == 200:
            data = r.json()
            x = []  
            for i in data['result']:
                sleep(0.5)
                t = Thread(target=craping, kwargs=i)
                t.start()
                x.append(t)
            for m in x:
                m.join()
            response = {
                "data": app_details,
                "status": 200
            }
        else:
            response = {
                "msg": "Please Enter Valid URL.",
                "status": r.status_code
            }
        return Response(response)
