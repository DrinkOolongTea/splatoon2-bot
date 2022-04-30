import nonebot
from nonebot import get_driver
from tomlkit import boolean
from .config import Config
from .utils import SplatoonUtiles
from pathlib import Path
from PIL import Image, ImageFont
from typing import List
import os

global_config = get_driver().config
config = Config.parse_obj(global_config)


class SplatoonInfo:
    """
    @name：push_league_battle
    @author： DrinkOolongTea
    @remark： 喷喷2资讯获取类
    @param： 
    @return： 
    """
    def __init__(self):

        self.splatoon_utils = SplatoonUtiles()

    @staticmethod
    def clear_cookies():
        """
        @name：Sichongzou
        @author： DrinkOolongTea
        @remark： 清除换存放昂发
        @param： 
        @return： 
        """
        nonebot.logger.info("开始清除缓存")
        for cookies in config.cookies_list:
            if os.path.exists(cookies):
                nonebot.logger.info("clear %(cokies)s")
                os.remove(cookies)
            else: nonebot.logger.info("%(cokies)s is not found")
        nonebot.logger.success("清除缓存结束")
    
    @staticmethod
    def cookies_exists() -> boolean:
        """
        @name：Sichongzou
        @author： DrinkOolongTea
        @remark： 判断缓存是否存在
        @param： 
        @return： boolean
        """
        for cookies in config.cookies_list:
            if os.path.exists(cookies):
                nonebot.logger.info("cookies %(cokies)s is ok")
            else: return False
        return True
    

    def get_image_cookies(self):
        """
        @name：push_league_battle
        @author： DrinkOolongTea
        @remark： 获取所有模式缓存
        @param： 
        @return： 
        """
        nonebot.logger.info("开始获取缓存")
        # 判断图片缓存目录是否存在
        images_cookies_dir = config.image_cookies_path
        if not os.path.exists(images_cookies_dir):
            os.makedirs(images_cookies_dir)

        # 获取网页数据
        proxy_file = config.proxy_file
        if os.path.isfile(proxy_file) :
            proxy_ip = global_config.https_proxy
            proxy_port = global_config.proxy_port
            if proxy_ip != "" and self.splatoon_utils.telnet(proxy_ip, int(proxy_port)):
                proxy_https ={'http:':"https://" + proxy_ip + ":" + str(proxy_port) + "/"}
                self.selector = self.splatoon_utils.request_get(config.url, proxy=proxy_https)
            else: self.selector = self.splatoon_utils.request_get(config.url)
        else:
            nonebot.logger.info(proxy_file) 
            nonebot.logger.info("未找到配置文件") 
            self.selector = self.splatoon_utils.request_get(config.url)
        #字体时间等配置
        self.data_path = Path(config.resource_path)
        font_path: Path = Path(self.data_path) / "ypifounts"
        china_font_path: Path = Path(self.data_path) / "china"
        self.font = ImageFont.truetype(str(font_path), 16)
        self.china_font = ImageFont.truetype(str(china_font_path), 16, encoding="unic")
        tmp_time = self.splatoon_utils.battle_time()
        self.time_list: List = [
            str(tmp_time)+":00", str(tmp_time+2)+":00"
        ]

        #处理信息保存图片缓存
        self.splatoon_utils.save_bytes_file(config.salmon_run_cookies, self.get_salmon_run())
        self.splatoon_utils.save_bytes_file(config.regular_battle_cookies, self.get_regular_battle())
        self.splatoon_utils.save_bytes_file(config.ranked_battle_cookies, self.get_ranked_battle())
        self.splatoon_utils.save_bytes_file(config.league_battle_cookies, self.get_league_battle())


    def get_salmon_run(self) -> bytes:
        """
        @name：get_salmon_run
        @author： DrinkOolongTea
        @remark： 获取打工资讯
        @param： 
        @return： 图片base64str
        """
        salmon_run_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][4]//a/text()")

        salmon_run_time: List = [self.selector.xpath("//div[@id='salmon1']/text()")[0],
                                 self.selector.xpath("//div[@id='salmon2']/text()")[0]]

        # 处理获取到的时间
        for i in range(len(salmon_run_time)):
            tmp: List = salmon_run_time[i].split(" ")
            tmp[2] = self.splatoon_utils.change_time_zone(tmp[2])
            tmp[6] = self.splatoon_utils.change_time_zone(tmp[6])
            # 移除不需要元素
            tmp.pop(7)
            salmon_run_time[i] = ' '.join(tmp)

        background_path: Path = Path(self.data_path) / "salmon_run.png"
        background: Image = Image.open(str(background_path))

        # 移除不需要元素
        salmon_run_info.pop(0)
        salmon_run_info.pop(5)
        salmon_run_info.pop(10)

        img_box: List = [(364, 147), (578, 142), (669, 142), (578, 201), (669, 201), (364, 333), (578, 330), (669, 330),
                         (578, 388), (669, 388)]
        text_box: List = [(385, 122), (385, 307)]

        self.splatoon_utils.paste_img(config.resource_path,salmon_run_info, img_box, background)
        self.splatoon_utils.draw_text(salmon_run_time, text_box, background, "white", self.font)
        nonebot.logger.info("处理打工资讯结束")
        return self.splatoon_utils.img_base64_str(background, "png")


    def get_regular_battle(self) -> bytes:
        """
        @name：get_regular_battle
        @author： DrinkOolongTea
        @remark： 获取涂地资讯
        @param： 
        @return： 图片base64str
        """
        regular_battle_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][2]//a/text()")
        new_list: List = [regular_battle_info[2], regular_battle_info[3], regular_battle_info[5],
                          regular_battle_info[6]]
        regular_battle_info = new_list
        nonebot.logger.info(regular_battle_info)

        background_path: Path = Path(self.data_path) / "regular_battle.png"
        background: Image = Image.open(str(background_path))
        img_box: List = [(60, 150), (331, 150), (60, 349), (331, 349)]
        text_box: List = [(100, 119), (100, 313)]
        self.splatoon_utils.paste_img(config.resource_path,regular_battle_info, img_box, background)
        self.splatoon_utils.draw_text(self.time_list, text_box, background, "white", self.font)

        nonebot.logger.info("处理涂地资讯结束")
        return self.splatoon_utils.img_base64_str(background, "png")


    def get_ranked_battle(self) -> bytes:
        """
        @name：get_ranked_battle
        @author： DrinkOolongTea
        @remark： 获取单人真格资讯
        @param： 
        @return： 图片base64str
        """
        ranked_battle_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][2]//a/text()")
        mode_list: List = [ranked_battle_info[8], ranked_battle_info[11]]
        new_list: List = []
        for i in range(len(mode_list)):
            new_list.append(self.splatoon_utils.mode_dict(mode_list[i]))
        mode_list = new_list

        new_list: List = [ranked_battle_info[9], ranked_battle_info[10], ranked_battle_info[12],
                          ranked_battle_info[13]]
        ranked_battle_info = new_list

        nonebot.logger.info(ranked_battle_info)

        background_path: Path = Path(self.data_path) / "ranked_battle.png"
        background: Image = Image.open(str(background_path))
        img_box: List = [(60, 150), (331, 150), (60, 349), (331, 349)]
        time_text_box: List = [(50, 119), (50, 313)]
        mode_text_box: List = [(100, 120), (100, 314)]

        self.splatoon_utils.paste_img(config.resource_path, ranked_battle_info, img_box, background)
        self.splatoon_utils.draw_text(self.time_list, time_text_box, background, "white", self.font)
        self.splatoon_utils.draw_text(mode_list, mode_text_box, background, "white", self.china_font)

        nonebot.logger.info("处理单排资讯结束")
        return self.splatoon_utils.img_base64_str(background, "png")


    def get_league_battle(self) -> bytes:
        """
        @name：get_League_Battle
        @author： DrinkOolongTea
        @remark： 获取多人真格资讯
        @param： 
        @return： 图片base64str
        """
        league_battle_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][2]//a/text()")
        mode_list: List = [league_battle_info[15], league_battle_info[18]]
        new_list: List = []
        for i in range(len(mode_list)):
            new_list.append(self.splatoon_utils.mode_dict(mode_list[i]))
        mode_list = new_list

        new_list: List = [league_battle_info[16], league_battle_info[17], league_battle_info[19],
                          league_battle_info[20]]

        league_battle_info = new_list

        nonebot.logger.info(league_battle_info)

        background_path: Path = Path(self.data_path) / "league_battle.png"
        background: Image = Image.open(str(background_path))
        img_box: List = [(60, 150), (331, 150), (60, 349), (331, 349)]
        time_text_box: List = [(50, 119), (50, 313)]
        mode_text_box: List = [(100, 120), (100, 314)]

        self.splatoon_utils.paste_img(config.resource_path, league_battle_info, img_box, background)
        self.splatoon_utils.draw_text(self.time_list, time_text_box, background, "white", self.font)
        self.splatoon_utils.draw_text(mode_list, mode_text_box, background, "white", self.china_font)

        nonebot.logger.info("处理组排资讯结束")
        return self.splatoon_utils.img_base64_str(background, "png")


    def push_salmon_run(self):
        """
        @name：push_league_battle
        @author： DrinkOolongTea
        @remark： 推送打工资讯
        @param： 
        @return： 
        """
        return self.splatoon_utils.read_bytes_file(config.salmon_run_cookies)
    

    def push_regular_battle(self):
        """
        @name：push_league_battle
        @author： DrinkOolongTea
        @remark： 推送凃地资讯
        @param： 
        @return： 
        """
        return self.splatoon_utils.read_bytes_file(config.regular_battle_cookies)


    def push_ranked_battle(self):
        """
        @name：push_league_battle
        @author： DrinkOolongTea
        @remark： 推送单排资讯
        @param： 
        @return： 
        """ 
        return self.splatoon_utils.read_bytes_file(config.ranked_battle_cookies)
    

    def push_league_battle(self):
        """
        @name：push_league_battle
        @author： DrinkOolongTea
        @remark： 推送组排资讯
        @param： 
        @return： 
        """
        return self.splatoon_utils.read_bytes_file(config.league_battle_cookies)

    