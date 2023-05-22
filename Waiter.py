import time
from loguru import logger
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class Waiter(object):
    def __init__(self, driver, interval=1, is_track=False, is_log=True):
        """
        @param driver: selenium driver
        @param interval: 单次等待时长间隔
        @param is_track: 在发生除NoSuchElementException以外的异常时是否抛出
        @param is_log: 是否打印log
        """
        self.driver = driver
        self.interval = interval
        self.is_track = is_track
        self.is_log = is_log

    def update_driver(self, driver):
        """
        用于如果需要手动显式更新url时使用
        @param driver: 更新后的 driver
        @return:
        """
        self.driver = driver

    def _loger(self, message, level="info"):
        if self.is_log:
            getattr(logger, level)(message)

    def _select_input_waiter(self, xpath: str, way="value", **kwargs):
        """
        通过xpath和way选定selector，并将kwargs得到的值填入其中。
        :param xpath:
        :param way: 有三种方法选择：value，index，text，默认为value
        :param kwargs:
        :return:
        """
        assert len(kwargs.values()) == 1, "select param takes 1 positional arguments but more or less were given"
        selector = Select(self.driver.find_element(By.XPATH, xpath))
        opt_value = next(iter(kwargs.values()))
        if way == "value":
            selector.select_by_value(opt_value)
        elif way == "index":
            selector.select_by_index(opt_value)
        else:
            selector.select_by_visible_text(opt_value)

    def _select_option_waiter(self, xpath, opt_type="all") -> list:
        value_list = []
        selector = Select(self.driver.find_element(By.XPATH, xpath))
        if opt_type == "first":
            value_list.append(selector.first_selected_option.text)
        else:
            if opt_type == "all":
                value_list.append(selector.first_selected_option.text)
                options = selector.options
            elif opt_type == "select_all":
                options = selector.all_selected_options
            for option in options:
                value_list.append(option.text)
        return value_list

    def _username_input_waiter(self, xpath: str, **kwargs):
        self._input_send_waiter(xpath, **kwargs)

    def _password_input_waiter(self, xpath: str, **kwargs):
        self._input_send_waiter(xpath, **kwargs)

    def _input_send_waiter(self, xpath: str, **kwargs):
        assert len(kwargs.values()) == 1, "input param takes 1 positional arguments but more or less were given"
        input_element = self.driver.find_element(By.XPATH, xpath)
        input_element.send_keys(next(iter(kwargs.values())))
        time.sleep(2)

    def _element_text_waiter(self, xpath: str, **kwargs) -> str:
        if not kwargs.get("attribute"):
            return self.driver.find_element(By.XPATH, xpath).text
        else:
            return self.driver.find_element(By.XPATH, xpath).get_attribute(kwargs.get("attribute"))

    def _click_waiter(self, xpath: str):
        self.driver.find_element(By.XPATH, xpath).click()

    def username_input_waiter(self, xpath: str, **kwargs):
        self.wait(func="_username_input_waiter", xpath=xpath, **kwargs)

    def input_send_waiter(self, xpath: str, **kwargs):
        self.wait(func="_input_send_waiter", xpath=xpath, **kwargs)

    def password_input_waiter(self, xpath: str, **kwargs):
        self.wait(func="_password_input_waiter", xpath=xpath, **kwargs)

    def click_waiter(self, xpath: str):
        self.wait(func="_click_waiter", xpath=xpath)

    def select_input_waiter(self, xpath: str, way="value", **kwargs):
        self.wait(func="_select_input_waiter", xpath=xpath, way=way, **kwargs)

    def select_option_waiter(self, xpath, opt_type="all"):
        option_list = self._get_value(func="_select_option_waiter", xpath=xpath, opt_type=opt_type)
        return option_list

    def elements_text_waiter(self, xpath: str, attribute=None) -> str:
        """
        循环等待搜索函数获取结果
        @param attribute: 根据attribute是否为空，选择是获取属性还是获取text
        @param xpath:
        @return:
        """
        element_text = self.wait(func="_element_text_waiter", xpath=xpath, attribute=attribute)
        return element_text

    def _get_value(self, xpath: str, func, **kwargs):
        while True:
            result = self.wait(func=func, xpath=xpath, **kwargs)
            if result:
                return result
            time.sleep(1)

    def wait(self, func: str, xpath, interval=None, **kwargs):
        """
        等待函数，通过函数的名称找到相应的搜索函数并循环等待，直到被搜索元素加载完成。
        用户可以通过继承该父类，写出自己的搜索函数，并交由该等待函数进行维护。
        @param func:
        @param xpath: 通过xpath寻找元素
        @param interval: 用于设置独立的等待时间
        @param kwargs: 元素加载成功后的输入，如：input需要输入的参数
        @return:
        """
        try:
            if callable(getattr(self, func)):
                if kwargs:
                    self._loger(message=kwargs)
                    return getattr(self, func)(xpath, **kwargs)
                else:
                    return getattr(self, func)(xpath)
        except NoSuchElementException as e:
            self._loger(level="warning", message="页面还未加载完毕")
            if interval:
                time.sleep(interval)
            else:
                time.sleep(self.interval)
            self.wait(func=func, xpath=xpath, interval=interval, **kwargs)
        except Exception as e:
            self._loger(level="error", message=e.args)
            if self.is_track:
                raise e
