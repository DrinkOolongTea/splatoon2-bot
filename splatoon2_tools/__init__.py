from lib2to3.pgen2 import driver
from nonebot import get_driver, on_command
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher import Matcher
from .core import SplatoonInfo
from .config import Config
from nonebot import require
from nonebot import get_bots
from nonebot.permission import SUPERUSER
from .utils import SplatoonUtiles
import threading

# 初始化
global_config = get_driver().config
config = Config.parse_obj(global_config)
driver = get_driver()

__splatoon2_tools_version__ = "v1.3.0"

splatoon2 = SplatoonInfo()
splatoon2_utiles = SplatoonUtiles()

@driver.on_startup
async def start():
    get_cookies()

if global_config.group_id_list is not None:
    group_id_list=global_config.group_id_list
else: group_id_list=[]

if global_config.bot_qq is not None:
    bot_qq=str(global_config.bot_qq)
else: bot_qq = ""

salmon_run = on_command('打工', aliases={'工'})
regular_battle = on_command('涂地', aliases={'涂地'})
ranked_battle = on_command('单排', aliases={'单排'})
league_battle = on_command('组排', aliases={'组排'})
scheduler = require("nonebot_plugin_apscheduler").scheduler
admin_open= on_command('开启自动推送', permission=SUPERUSER)
admin_close= on_command('关闭自动推送', permission=SUPERUSER)
update = on_command('更新地图数据', permission=SUPERUSER)

# 响应回复板块头
@regular_battle.handle()
async def _handle( matcher: Matcher):
    nonebot.logger.info("推送涂地资讯")
    await salmon_run.finish(MessageSegment.image(splatoon2.push_regular_battle()))


@ranked_battle.handle()
async def _handle(matcher: Matcher):
    nonebot.logger.info("推送单排资讯")
    await salmon_run.finish(MessageSegment.image(splatoon2.push_ranked_battle()))


@league_battle.handle()
async def _handle(matcher: Matcher):
    nonebot.logger.info("推送组排资讯")
    await salmon_run.finish(MessageSegment.image(splatoon2.push_league_battle()))


@salmon_run.handle()
async def _handle(matcher: Matcher):
    nonebot.logger.info("推送打工资讯")
    await salmon_run.finish(MessageSegment.image(splatoon2.push_salmon_run()))


@update.handle()
async def _handle(matcher: Matcher):
    get_cookies()
    

# 响应回复板块尾

# 定时任务头
async def cron_get_cookies():
    splatoon2.clear_cookies()
    get_cookies()


async def cron_push():
    if splatoon2.cookies_exists():
        forward_msg=news_list()
        bot=get_bots()[bot_qq]
        if group_id_list is not None:
            for group_id in group_id_list:
                try:
                    nonebot.logger.info(group_id)
                    await bot.send_group_forward_msg(group_id=group_id,messages=forward_msg)
                except:
                    nonebot.logger.error("推送群消息出现错误")
    else: await admin_open.finish(MessageSegment.text("无数据，请联系管理员"))


@admin_open.handle()
async def _handle(matcher: Matcher):
    scheduler.add_job(cron_push, "cron", hour="*/2", minute = 3, id="cron_get_cookies")
    scheduler.add_job(cron_push, "cron", hour="*/2", minute = 5, id="cron_push")
    await admin_open.finish(MessageSegment.text("已打开自动推送"))


@admin_close.handle()
async def _handle(matcher: Matcher):
    if scheduler.get_job("cron_get_cookies") and scheduler.get_job("cron_push") is None:
        await admin_close.finish(MessageSegment.text("没有开启自动推送哦"))
    scheduler.remove_job("cron_get_cookies")
    scheduler.remove_job("cron_push")
    await admin_close.finish(MessageSegment.text("已关闭自动推送"))

# 定时任务尾

# 自定义方法头

def news_list():
    """
    @name: news_list
    @author： Sichongzou
    @remark： 组装群发消息
    @param： 
    @return： 组装好的群发消息
    """
    forward_msg=[]
    #forward_msg.append(to_json("这里是Splatoon2定时推送姬,以下是未来时间段的地图信息！"))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoon2.push_league_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoon2.push_ranked_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoon2.push_regular_battle()))))
    forward_msg.append(to_json(Message(MessageSegment.image(splatoon2.push_salmon_run()))))

    return forward_msg


def to_json(msg: Message):
    """
    @name：cron_push
    @author： Sichongzou
    @remark： 转群转发
    @param： 消息列
    @return： none
    """
    if global_config.bot_qq_name is not None:
        name = global_config.bot_qq_name
    else:
        name = "splatoon2推送机器人"
    return {"type": "node", "data": {"name": name, "uin": bot_qq, "content": msg}}


def get_cookies():
    """
    @name：Sichongzou
    @author： DrinkOolongTea
    @remark： 并发获取缓存
    @param： 
    @return：
    """
    nonebot.logger.info("获取splatoon2缓存")
    t = threading.Thread(target=splatoon2.get_image_cookies)
    t.start()
    nonebot.logger.info("获取splatoon2缓存结束")

# 自定义方法尾
