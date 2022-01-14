import logging
import yaml
from datetime import datetime
from pytz import timezone


def customTime(*args):
    """
    ログの出力時間を日本標準時に変更する
    """
    return datetime.now(timezone('Asia/Tokyo')).timetuple()

def set_logger(logger_name:str,folder:str = 'api',file_name:str ='app')-> logging.Logger:
    """
    loggerを作成する
    
    Parameters
    
    ----------

    logger_name : str
        loggerに設定する名前
    """

    # 設定ファイルを読み込む
    with open('settings.yaml', 'r') as yml:
        settings = yaml.safe_load(yml)

    #ログファイルを作成
    dt = datetime.now()
    date_format = dt.strftime(settings['fastapi']['logging']['log_filename'])
    filename =f'{file_name}_{date_format}'

    #loggerの作成
    logger = logging.getLogger(logger_name)
    logger.setLevel(settings['fastapi']['logging']['level'])

    #ハンドラーの設定
    file_handler = logging.FileHandler(f'../../logs/{folder}/{filename}.log',mode='a',encoding='utf-8')
    file_handler.setLevel(settings['fastapi']['logging']['level'])
    
    #ログ出力時のフォーマット設定
    formatter = logging.Formatter(settings['fastapi']['logging']['format'],datefmt=settings['fastapi']['logging']['datefmt'])
    formatter.converter = customTime
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger