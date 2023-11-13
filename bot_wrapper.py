from user_info import UserInfo
from known_user_manager import KnownUserManager
from mex_manager import MexManager
from telegram import Message

class BotWrapper:
    def __init__(self, known_user_file:str, bot_mex_file:str) -> None:
        self.known_user_manager = KnownUserManager(known_user_file)
        self.mex_manager = MexManager(bot_mex_file)

    def is_known_user(self, user_id:int) -> UserInfo:
        return self.known_user_manager.is_known_user(user_id)

    def add_user(self, new_user:UserInfo) -> UserInfo:
        return self.known_user_manager.add_user(UserInfo)

    def return_mex(self, code:str, user:UserInfo, text_message:Message) -> str:
        return self.mex_manager.return_mex(code, user, text_message)