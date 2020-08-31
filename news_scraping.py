# data_gathering
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
import pandas as pd
import numpy as np
import csv
import math
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import psycopg2 
import uuid
import schedule
import os


# options.add_argument('--headless')
#       options.add_argument('--disable-gpu')
#       options.add_argument('--no-sandbox')
#       options.add_argument('--remote-debugging-port=9222')
#       options.add_argument('--proxy-server='+proxy)

# import ScrapingTools as syn

csv_titles=[]
# conn = psycopg2.connect('Driver={SQL Server};'
#                       'Server=HQ_042;'
#                       'Database=news;'
#                       'Trusted_Connection=yes;')
conn = psycopg2.connect(
	host="host",
	database="database",user="user",
	password="password"
	)

class News:
	def __init__(self,max):
		self.max=max
	# SELECT MATCH FOR THE DAY
	def techcrunch(max=5):
		url="https://techcrunch.com/"
		chromeOptions = webdriver.ChromeOptions()
		# , 'disk-cache-size': 4096 dnt use for dynamic pages
		# HEROKU
		chromeOptions.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
		chromeOptions.add_argument("--headless")
		chromeOptions.add_argument("--no-sandbox")
		chromeOptions.add_argument("--disable-dev-sh-usage")
		driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chromeOptions)
		# prefs = {'profile.managed_default_content_settings.images':2}
		# chromeOptions.add_experimental_option("prefs", prefs)
		# chromeOptions.add_argument('ignore-certificate-errors')		
		# driver=webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/chromedriver/chromedriver.exe",options=chromeOptions)
		driver.get(url)
		i_loop=2
		try:
			login_element = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME, "post-block__title__link")))
		except:
			pass
		# soup=BeautifulSoup(driver.page_source,"lxml")
		cursor = conn.cursor()
		# cursor.execute('''
		#             INSERT INTO news (Id,website,link, image, title,description,news_date)
		#             VALUES
		#             ('{Id}','{website}','{link}', '{image}', '{title}','{description}','{news_date}')
		#             ''')
		
		for j in range(max):
			try:
				i=j+1
				link=driver.find_element_by_xpath("//*[@id='tc-main-content']/div[2]/div/div/div/article["+str(i)+"]/header/h2/a").get_attribute('href')
				try:
					image=driver.find_element_by_xpath("//*[@id='tc-main-content']/div[2]/div/div/div/article["+str(i)+"]/footer/figure/picture/img").get_attribute('src')
				except:
					image=""
				title=driver.find_element_by_xpath("//*[@id='tc-main-content']/div[2]/div/div/div/article["+str(i)+"]/header/h2/a").text
				description=driver.find_element_by_xpath("//*[@id='tc-main-content']/div[2]/div/div/div/article["+str(i)+"]/div/p").text
				news_date=driver.find_element_by_xpath("//*[@id='tc-main-content']/div[2]/div/div/div/article["+str(i)+"]/header/div/div/div/time").get_attribute('datetime')
				website="techcrunch"
				Id=uuid.uuid4()
				sql="select * from news where link='"+str(link).replace("//","///")+"' or link='"+str(link)+"'"
				cursor.execute(sql)
				records = len(cursor.fetchall())
				print("techcrunch"+str(records))
				if records>0:
					continue
				sql='''
					INSERT INTO news (Id,website,link, image, title,description,news_date,topic,date,lastUpdate)
					VALUES
					('{}','{}','{}', '{}', '{}','{}','{}','','{}','{}')
					'''
				cursor.execute(sql.format(str(Id), str(website), str(link).replace("'",'"'),str(image).replace("'",'"'),str(title).replace("'",'"'),str(description).replace("'",'"'),str(news_date),str(datetime.now()),str(datetime.now())))
			except er:
				print(er)			
				continue
			# print(Id, website, link,image,title,description,news_date )
			


		conn.commit()

	def washingtonpost_covid(max=5):
		today=datetime.now().strftime("%Y/%m/%d") #"2020/08/11" "+ today+"
		url="https://www.washingtonpost.com/nation/"+today+"/coronavirus-covid-live-updates-us/"	
		chromeOptions = webdriver.ChromeOptions()
		# , 'disk-cache-size': 4096 dnt use for dynamic pages
		# HEROKU
		chromeOptions.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
		chromeOptions.add_argument("--headless")
		chromeOptions.add_argument("--no-sandbox")
		chromeOptions.add_argument("--disable-dev-sh-usage")
		driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chromeOptions)
		# prefs = {'profile.managed_default_content_settings.images':2}
		# chromeOptions.add_experimental_option("prefs", prefs)
		# chromeOptions.add_argument('ignore-certificate-errors')

		# driver=webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/chromedriver/chromedriver.exe",options=chromeOptions)
		driver.get(url)
		i_loop=2
		
		try:
			login_element = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME, "inline-story b bt pt-xs bc-gray-light")))
		except Exception as er:
			print(str(er))
		cursor = conn.cursor()
		for dt in BeautifulSoup(driver.page_source,"lxml").find_all(class_="inline-story b bt pt-xs bc-gray-light"):
			# //*[@id="link-VTBD5J5B6VF35NTM6H2NDIAUBE"]/div[2]/section/div[1]/figure/div/img
			try:			
				inline_id=str(dt.get("id"))			
				if inline_id is None:
					print("continue")
					continue			
				time.sleep(5)
				title=driver.find_element_by_xpath("//*[@id='"+inline_id+"']/h2").text		
				try:
					image=driver.find_element_by_xpath("//*[@id='"+inline_id+"']/div[2]/section/div[1]/figure/div/img").get_attribute('src')			
				except:
					image=""
				description=driver.find_element_by_xpath("//*[@id='"+inline_id+"']/div[2]/section/div[2]/p").text
				link=url+"#"+inline_id
				news_date=today+"  "+driver.find_element_by_xpath("//*[@id='"+inline_id+"']/div[1]/div").text
				website="washingtonpost"
				Id=uuid.uuid4()
				sql="select * from news where link='"+str(link).replace("//","///")+"' or link='"+str(link)+"'"
				cursor.execute(sql)
				records = len(cursor.fetchall())
				print("washingtonpost"+str(records))
				if records>0:
					continue
				sql='''
					INSERT INTO news (Id,website,link, image, title,description,news_date,topic,date,lastUpdate)
					VALUES
					('{}','{}','{}', '{}', '{}','{}','{}','','{}','{}')
					'''
				cursor.execute(sql.format(str(Id), str(website), str(link).replace("'",'"'),str(image).replace("'",'"'),str(title).replace("'",'"'),str(description).replace("'",'"'),str(news_date),str(datetime.now()),str(datetime.now())))
			except Exception as er:
				print("error: " +str(er))
				continue
		conn.commit()

	def cnn(max=5):
		url="https://edition.cnn.com/"
		chromeOptions = webdriver.ChromeOptions()
		# HEROKU
		chromeOptions.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
		chromeOptions.add_argument("--headless")
		chromeOptions.add_argument("--no-sandbox")
		chromeOptions.add_argument("--disable-dev-sh-usage")
		# , 'disk-cache-size': 4096 dnt use for dynamic pages
		# prefs = {'profile.managed_default_content_settings.images':2}
		# chromeOptions.add_experimental_option("prefs", prefs)
		# chromeOptions.add_argument('ignore-certificate-errors')
		
		# driver=webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/chromedriver/chromedriver.exe",options=chromeOptions)
		driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chromeOptions)
		driver.get(url)		
		i_loop=2
		try:
			login_element = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME, "cn__title column zn__column--idx-5")))
		except:
			pass
		cursor = conn.cursor()
		# soup=BeautifulSoup(driver.page_source,"lxml")
		i=0
		for j in range(max):
			try:
				if i>0:
					driver.get(url)
				i_loop=2
				try:
					login_element = WebDriverWait(driver, 10).until(
							EC.presence_of_element_located((By.CLASS_NAME, "cn__title column zn__column--idx-5")))
				except:
					pass
				i=j+1
				if i>0:
					time.sleep(15)
				else:
					time.sleep(5)
				if i==1:
					link=driver.find_element_by_xpath("//*[@id='intl_homepage1-zone-1']/div[2]/div/div[3]/ul/li["+str(i)+"]/article/div/div[2]/h3/a").get_attribute('href')
					image=driver.find_element_by_xpath("//*[@id='intl_homepage1-zone-1']/div[2]/div/div[3]/ul/li[1]/article/div/div[1]/a/img").get_attribute('src')
				else:
					link=driver.find_element_by_xpath("//*[@id='intl_homepage1-zone-1']/div[2]/div/div[3]/ul/li["+str(i)+"]/article/div/div/h3/a").get_attribute('href')
					image=""
				
				title=driver.find_element_by_xpath("//*[@id='intl_homepage1-zone-1']/div[2]/div/div[3]/ul/li["+str(i)+"]/article/div/div/h3/a/span[1]").text
				website="cnn"
				Id=uuid.uuid4()				
				driver.get(link)
				try:
					login_element = WebDriverWait(driver, 10).until(
							EC.presence_of_element_located((By.CLASS_NAME, "pg-headline")))
					description=driver.find_element_by_xpath("//*[@id='body-text']/div[1]/div[1]/p").text
					try:
						news_date=driver.find_element_by_xpath("/html/body/div[6]/article/div[1]/div[2]/div[1]/p[3]").text
					except:
						news_date=datetime.now()
																					
				except Exception as re:
					print(i)
					print("errrr")
					print(re)
					continue
				sql="select * from news where link='"+str(link).replace("//","///")+"' or link='"+str(link)+"'"
				cursor.execute(sql)
				records = len(cursor.fetchall())
				print("cnn"+str(records))

				if records>0:
					continue
				
				sql='''
					INSERT INTO news (Id,website,link, image, title,description,news_date,topic,date,lastUpdate)
					VALUES
					('{}','{}','{}', '{}', '{}','{}','{}','','{}','{}')
					'''
				params = (Id, website, link,image,title,description,news_date )
				# print(sql.format(str(Id), str(website), str(link),str(image).replace("'",'"'),str(title).replace("'",'"'),str(description).replace("'",'"'),str(news_date )))
				cursor.execute(sql.format(str(Id), str(website), str(link).replace("'",'"'),str(image).replace("'",'"'),str(title).replace("'",'"'),str(description).replace("'",'"'),str(news_date),str(datetime.now()),str(datetime.now())))
			except Exception as er:
				print(i)
				print("ffffff")
				print(er)			
				continue
		conn.commit()


def main():
	News.cnn()
	News.washingtonpost_covid()	
	News.techcrunch()		


# if __name__=="__main__":
	
# Task scheduling 
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
  
if __name__=="__main__":
	schedule.every(5).hours.do(main)
	# Loop so that the scheduling task 
	# keeps on running all time. 
	while True: 
	
		# Checks whether a scheduled task  
		# is pending to run or not 
		schedule.run_pending() 
		time.sleep(30) 

# News.cnn()