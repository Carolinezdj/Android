# -*- coding: utf-8 -*-
import sys
import os
import unittest
from time import sleep
from appium import webdriver

class HelloWorld(unittest.TestCase):
    def test_addContact(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['appPackage'] = 'com.android.contacts'
        desired_caps['appActivity'] = '.activities.PeopleActivity'
        desired_caps['deviceName'] = '052abd630a670a6a'

        #初始化appium连接
        driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        #查找创建新联系人按钮
        createContactButton = None
        try:
            #如果手机没有联系人，则通过create_contact_button来创建。 此处通过控件id来查找
            createContactButton = driver.find_element_by_id("com.android.contacts:id/create_contact_button")
        except:
            #如果手机已经有其他联系人,则通过底部的添加联系人菜单来添加
            createContactButton = driver.find_element_by_id("com.android.contacts:id/menu_add_contact")
        #点击创建按钮
        createContactButton.click()

        #稍等下，手机响应需要一点时间
        sleep(2)
        #查看dialog的显示是否显示
        try:
            dialog = driver.find_element_by_id("android:id/content")
            #找到“本地保存”按钮并点击
            saveLocal = driver.find_element_by_id("com.android.contacts:id/left_button")
            saveLocal.click()
            sleep(2)
        except:
            #如果找不到dialog或者button,就会跳转到这里
            print("no dialog found")
        #点击姓名，并输入。此处是通过控件的文本来找到
        name = driver.find_element_by_name(u"姓名")
        name.click()
        name.send_keys("appiumTest")
        #点击电话输入框，并输入。注意此处是通过找到一组控件，并操作第n个控件，n从0开始。
        telephoneControls = driver.find_elements_by_name(u"电话")
        telephoneControls[1].click()
        telephoneControls[1].send_keys("01012345678")
        #保存一个屏幕截图
        driver.save_screenshot("afterinput.png")
        #点击完成按钮
        completeButton = driver.find_element_by_id("com.android.contacts:id/icon")
        completeButton.click()
        sleep(2)
        #验证联系的信息是否与输入一样
        barTitle = driver.find_element_by_id("android:id/action_bar_title")
        self.assertEqual(barTitle.text, "appiumTest")
        contactDatas = driver.find_elements_by_id("com.android.contacts:id/data")
        self.assertEqual(contactDatas[0].text, "010 1234 5678")
        #最后保存一个截图用于人工查看
        driver.save_screenshot("newContact.png")
        driver.close()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HelloWorld)
    unittest.TextTestRunner(verbosity=2).run(suite)