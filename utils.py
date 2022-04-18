import base64
import nonebot
import datetime
import requests
from io import BytesIO
from nonebot import get_driver
from .config import Config
from pathlib import Path
from lxml import etree
from PIL import Image, ImageDraw, ImageFont
from typing import List

global_config = get_driver().config
config = Config.parse_obj(global_config)


class SplatoonInfo:
    def __init__(self):
        url = 'https://splatoonwiki.org/wiki/Main_Page'
        req = requests.get(url)
        html = req.text
        self.selector = etree.HTML(html)
        self.data_path = Path(config.resource_path)
        print(self.data_path)
        font_path: Path = Path(self.data_path) / "ypifounts"
        china_font_path: Path = Path(self.data_path) / "china"
        self.font = ImageFont.truetype(str(font_path), 16)
        self.china_font = ImageFont.truetype(str(china_font_path), 16, encoding="unic")
        time = self.battle_time()
        self.time_list: List = [
            str(time)+":00", str(time+2)+":00"
        ]

    @staticmethod
    def change_time_zone(time: str) -> str:
        time: str = datetime.datetime.strptime(time, "%H:%M")
        time: str = (time + datetime.timedelta(hours=8)).strftime('%H:%M')
        return time

    def paste_img(self, info: List, box: List, background_img: Image):
        for i in range(len(info)):
            img = Image.open(Path(self.data_path / Path((info[i]).replace(" ", "_") + ".png"))).convert(
                    'RGBA')
            r, g, b, a = img.split()
            background_img.paste(img, box[i], mask=a)

    @staticmethod
    def battle_time() -> int:
        curr_time = datetime.datetime.now()
        time_str = curr_time.strftime("%H")
        if int(time_str) % 2 > 0:
            return int(time_str) - 1
        else:
            return int(time_str)

    @staticmethod
    def draw_text(info: List, box: List, background_img: Image, color: str, font: ImageFont):
        draw = ImageDraw.Draw(background_img)
        for i in range(len(info)):
            draw.text(box[i], str(info[i]), fill=color, font=font)

    @staticmethod
    def img_base64_str(image: Image, img_format: str) -> str:
        buf = BytesIO()
        image.save(buf, img_format)
        base64_str: str = "base64://" + base64.b64encode(buf.getbuffer()).decode()
        return base64_str

    @staticmethod
    def mode_dict(context: str) -> str:
        d = {"Rainmaker": "鱼", "Splat Zones": "占地", "Clam Blitz": "蛤蜊", "Tower Control": "塔"}
        return d[context]

    def get_salmon_run(self) -> str:
        salmon_run_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][4]//a/text()")

        salmon_run_time: List = [self.selector.xpath("//div[@id='salmon1']/text()")[0],
                                 self.selector.xpath("//div[@id='salmon2']/text()")[0]]

        nonebot.logger.info(salmon_run_info)

        # 处理获取到的时间
        for i in range(len(salmon_run_time)):
            tmp: List = salmon_run_time[i].split(" ")
            tmp[2] = self.change_time_zone(tmp[2])
            tmp[6] = self.change_time_zone(tmp[6])
            # 移除不需要元素
            tmp.pop(7)
            salmon_run_time[i] = ' '.join(tmp)
        nonebot.logger.info(salmon_run_time)

        background_path: Path = Path(self.data_path) / "salmon_run.png"
        background: Image = Image.open(str(background_path))

        # 移除不需要元素
        salmon_run_info.pop(0)
        salmon_run_info.pop(5)
        salmon_run_info.pop(10)

        img_box: List = [(364, 147), (578, 142), (669, 142), (578, 201), (669, 201), (364, 333), (578, 330), (669, 330),
                         (578, 388), (669, 388)]
        text_box: List = [(385, 122), (385, 307)]

        self.paste_img(salmon_run_info, img_box, background)
        self.draw_text(salmon_run_time, text_box, background, "white", self.font)

        return self.img_base64_str(background, "png")

    def get_regular_battle(self) -> str:
        regular_battle_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][2]//a/text()")
        new_list: List = [regular_battle_info[2], regular_battle_info[3], regular_battle_info[5],
                          regular_battle_info[6]]
        regular_battle_info = new_list
        now_time = self.battle_time()
        nonebot.logger.info(regular_battle_info)

        background_path: Path = Path(self.data_path) / "regular_battle.png"
        background: Image = Image.open(str(background_path))
        img_box: List = [(60, 150), (331, 150), (60, 349), (331, 349)]
        text_box: List = [(100, 119), (100, 313)]
        self.paste_img(regular_battle_info, img_box, background)
        self.draw_text(self.time_list, text_box, background, "white", self.font)

        return self.img_base64_str(background, "png")

    def get_ranked_battle(self) -> str:
        ranked_battle_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][2]//a/text()")
        mode_list: List = [ranked_battle_info[8], ranked_battle_info[11]]
        ranked_battle_time: List = ["now", "next"]
        new_list: List = []
        for i in range(len(mode_list)):
            new_list.append(self.mode_dict(mode_list[i]))
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

        self.paste_img(ranked_battle_info, img_box, background)
        self.draw_text(self.time_list, time_text_box, background, "white", self.font)
        self.draw_text(mode_list, mode_text_box, background, "white", self.china_font)

        return self.img_base64_str(background, "png")

    def get_League_Battle(self):
        league_battle_info: List = self.selector.xpath("//div[@class='bubbleboxbg'][2]//a/text()")
        mode_list: List = [league_battle_info[15], league_battle_info[18]]
        league_battle_time: List = ["now", "next"]
        new_list: List = []
        for i in range(len(mode_list)):
            new_list.append(self.mode_dict(mode_list[i]))
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

        self.paste_img(league_battle_info, img_box, background)
        self.draw_text(self.time_list, time_text_box, background, "white", self.font)
        self.draw_text(mode_list, mode_text_box, background, "white", self.china_font)

        return self.img_base64_str(background, "png")









