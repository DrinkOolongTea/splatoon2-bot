from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher import Matcher
from .utils import SplatoonInfo
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

__splatoon2_tools_version__ = "v0.1.2"

salmon_run = on_command('打工', aliases={'工'})
regular_battle = on_command('凃地', aliases={'凃地'})
ranked_battle = on_command('单排', aliases={'单排'})
league_battle = on_command('组排', aliases={'组排'})

@regular_battle.handle()
async def _handle(matcher: Matcher):
    await salmon_run.finish(MessageSegment.image(SplatoonInfo().get_regular_battle()))


@ranked_battle.handle()
async def _handle(matcher: Matcher):
    await salmon_run.finish(MessageSegment.image(SplatoonInfo().get_ranked_battle()))


@league_battle.handle()
async def _handle(matcher: Matcher):
    await salmon_run.finish(MessageSegment.image(SplatoonInfo().get_League_Battle()))


@salmon_run.handle()
async def _handle(matcher: Matcher):
    await salmon_run.finish(MessageSegment.image(SplatoonInfo().get_salmon_run()))
