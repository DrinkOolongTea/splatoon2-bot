import os
from pydantic import BaseSettings


class Config(BaseSettings):
    # 获取配置图片路径
    resource_path: str = os.path.join(os.path.dirname(__file__), "resource")

    # 配置文件路径
    proxy_file = os.getcwd() + "/splatoon2_tools_config.ini"

    # 图片缓存路径
    image_cookies_path = os.getcwd() + "/splatonn2_tools_cookies"

    # 图片缓存名称

    salmon_run_cookies = image_cookies_path + "/salmon_run_cookies"
    regular_battle_cookies = image_cookies_path + "/regular_battle_cookies"
    ranked_battle_cookies = image_cookies_path + "/ranked_battle_cookies"
    league_battle_cookies = image_cookies_path + "/league_battle_cookies"

    cookies_list = [salmon_run_cookies, regular_battle_cookies,
                    ranked_battle_cookies, league_battle_cookies]

    # url
    url = 'https://splatoonwiki.org/wiki/Main_Page'

    class Config:
        extra = "ignore"
