# Swaiter

​	项目名字取自：Selenium+waiter

​	作为一个爬虫人，在使用selenium进行爬虫时，时长会遇到由于网络等原因导致无法及时获取一些元素，从而导致程序报错。此时聪明的小伙伴就会说了：加个`time.sleep()`不就好了。事实上这个方法确实可以解决绝大部分问题，但其也有一个比较尴尬的问题：到底要“睡”多久合适？长了耽误爬取效率，短了又怕没有作用，所以这个库就是为了解决上述问题而存在的。

## 安装

库的安装十分简单直接使用以下面的命令就可以安装成功了：

```bash
pip install Swaiter
```

## 使用

使用方法主要分为两种：直接使用基础组件进行开发、继承并添加自己的检索函数

### 使用基础组件

这里给一个简单的使用基础组件的例子：

```python
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from waiter import Waiter

if __name__ == '__main__':
    # 获取selenium中驱动配置项（可省略）
    driver_opt = Options()
    url = "https://www.baidu.com/"
    # 获取selenium中的driver对象
    chrome_driver = Chrome(options=driver_opt)
    chrome_driver.get(url=url)
    # 利用获取到的driver对象创建Waiter对象
    w = Waiter(chrome_driver)
    # 传入xpath路径以及查询参数，检索input对象，并向其中填入查询参数
    w.input_send_waiter(xpath="//input[@id='kw']", query="python")
    # 利用xpath找到点击对象，模拟点击
    w.click_waiter(xpath="//input[@id='su']")
    # 在新的页面找到第一个链接，并获取其中的href属性值
    result = w.elements_text_waiter(xpath="//h3/a[@tabindex=0]", attribute="href")
    print(result)
```

​	上述例子中，使用了3个基础的搜索函数，向这样的搜索函数，本库一共提供了5个，应该可以满足简单的模拟需求，当然如果你有一些特别的搜索需求，也可以尝试使用第二种方式。

### 继承并开发自己的检索函数

```python
from waiter import Waiter
from selenium.webdriver.common.by import By

class MyWaiter(Waiter):
    def __init__(self, driver, interval, is_track, is_log):
        super().__init__(driver=driver, interval=interval, is_track=is_track, is_log=is_log)

    def _textarea_send(self, xpath, **kwargs):
        self.driver.find_element(By.XPATH, xpath).send(kwargs)

    def textarea_send(self, xpath, **kwargs):
        self.wait(func="_textarea_send", xpath=xpath, interval=5, **kwargs)
```

## 环境

> window10、window11
>
> python>=3.8
>
> selenium>=4.9.0
>
> loguru>=0.7.0

## 版本

#### 2023.5.16

**Version-1.0.3**

完成基础功能

​	[1.0.3](https://pypi.org/project/Swaiter/1.0.3/)

