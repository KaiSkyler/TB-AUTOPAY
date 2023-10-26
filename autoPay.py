import os  # 创建文件夹, 文件是否存在
import time  # time 计时
import pickle  # 保存和读取cookie实现免登陆的一个工具
import json
from time import sleep
from selenium import webdriver  # 操作浏览器的工具
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaoBaoPay:
    # 初始化加载
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.current_url = ''
        self.payPassword = '123456'
        self.loginBtn = ''
        self.cartBtn = ''
        self.checkBtn = ''
        self.checkOrderBtn = ''
        self.createOrderBtn = ''
        self.passwordInput = ''
        self.payMoneyBtn = ''
        self.payIframe = ''
        self.loginUrl = 'https://login.taobao.com/member/login.jhtml'  # 根据实际情况修改
        self.loginTarget = 'i.iconfont.icon-qrcode'  # 根据实际情况修改
        self.cartTarget = 'J_MiniCart'  # 根据实际情况修改
        self.selectAllTarget = 'J_SelectAll1'  # 根据实际情况填写
        self.checkOrderTarget = 'J_Go'  # 根据实际情况填写
        self.createOrderTarget = 'go-btn' # 根据实际情况填写
        self.inputPasswordTarget = 'payPassword_rsainput' # 根据实际情况填写
        self.payTarget = 'validateButton' # 根据实际情况填写
        self.payIframeTarget = 'iframe___1Em0z' # 根据实际情况填写

    def autoLogin(self):
        self.driver.get(self.loginUrl)
        while True:
            print('正在登录中请稍等.............')
            try:
              self.loginBtn = self.driver.find_element(By.CSS_SELECTOR, self.loginTarget)
            except Exception as e:
              print(e)
            if self.loginBtn:
                break
        
        sleep(1)
        self.loginBtn.click()
        sleep(5)

        while True:
            #print(f'当前地址：{self.driver.current_url}')
            print('请扫描二维码登录淘宝账号，如已扫描耐心等待登录成功即可.............')
            try:
                self.current_url = self.driver.current_url
            except Exception as e:
              print(e)
            if self.current_url != 'https://login.taobao.com/member/login.jhtml':
                break
          
        sleep(1)
        self.searchCart()

    def searchCart(self):
        
        while True:
            print('正在进入购物车请稍等.............')
            try:
                self.cartBtn = self.driver.find_element(By.ID, self.cartTarget)
            except Exception as e:
               print(e)
            if self.cartBtn:
                break
        
        sleep(1)
        self.cartBtn.click()
        sleep(5)
        self.searchShopItem()

    def searchShopItem(self):
    
        while True:
            print('正在确认支付商品请稍等.............')
            try:
                self.checkBtn = self.driver.find_element(By.ID, self.selectAllTarget)
            except Exception as e:
              print(e)
            if self.checkBtn:
                break
        
        sleep(1)
        self.checkBtn.click()
        sleep(5)

        while True:
            print('正在进行商品结算请稍等.............')
            try:
                self.checkOrderBtn = self.driver.find_element(By.ID, self.checkOrderTarget)
            except Exception as e:
              print(e)
            if self.checkOrderBtn:
                break
    
        sleep(1)
        self.checkOrderBtn.click()
        sleep(5)
        
        self.toAutoPay()

    def toAutoPay(self):
        
        while True:
            print('正在提交支付订单请稍等.............')
            try:
                self.createOrderBtn = self.driver.find_element(By.CLASS_NAME, self.createOrderTarget)
            except Exception as e:
              print(e)
            if self.createOrderBtn:
                break
        
        sleep(1)
        self.createOrderBtn.click()
        sleep(5)

        self.inputPassword()
    
    def inputPassword(self):

        while True:
            print('正在进行输入支付密码操作请稍等.............')
            try:
                # 等待iframe加载完成
                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, self.payIframeTarget))
                )
                sleep(3)
                # 等待元素加载完成
                self.passwordInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, self.inputPasswordTarget))
                )
                sleep(3)
            except Exception as e:
              print(e)
            if self.passwordInput:
                break
        
        sleep(1)
        self.passwordInput.send_keys(self.payPassword)
        sleep(5)

        self.confirmPay()
    
    def confirmPay(self):

        while True:
            print('正在进行提交支付操作请稍等.............')
            try:
                # 等待元素加载完成
                self.payMoneyBtn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, self.payTarget))
                )
            except Exception as e:
              print(e)
            if self.payMoneyBtn:
                break

        sleep(1)
        self.payMoneyBtn.click()
        # 切换回主文档
        self.driver.switch_to.default_content()
        print('已成功提交支付请稍等，若支付密码错误则无法进行下一步.............')
        sleep(1000)


    def finish(self):
        self.driver.quit()

if __name__ == '__main__':
    con = TaoBaoPay()
    try:
        con.autoLogin()  # 自动登录
    except Exception as e:
        print(e)
        con.finish()
