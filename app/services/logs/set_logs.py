import logging
import logging.handlers
import yaml
from datetime import datetime,time
from pytz import timezone


def customTime(*args):
    """
    ログの出力時間を日本標準時に変更する
    """
    return datetime.now(timezone('Asia/Tokyo')).timetuple()

def set_logger(logger:logging.Logger, folder:str = 'api', file_name:str ='app', log_level = "INFO")-> logging.Logger:
    """
    loggerにハンドラーを設定する
    
    Parameters
    
    ----------

    logger_name : str
        loggerに設定する名前
    """

    # 設定ファイルを読み込む
    with open('settings.yaml', 'r') as yml:
        settings = yaml.safe_load(yml)

    #ログファイルを作成
    # dt = datetime.now()
    # date_format = dt.strftime(settings['fastapi']['logging']['log_filename'])
    filename =f'{file_name}'
    logger.setLevel(log_level)
    #ハンドラーの設定
    file_handler = logging.handlers.TimedRotatingFileHandler(f'../../logs/{folder}/{filename}',encoding='utf-8', 
            when=settings['fastapi']['logging']['when'],
            backupCount=settings['fastapi']['logging']['backupCount'],
            atTime=time(2, 0, 0)
            )
    file_handler.setLevel(log_level)
    
    #ログ出力時のフォーマット設定
    formatter = logging.Formatter(settings['fastapi']['logging']['format'],datefmt=settings['fastapi']['logging']['datefmt'])
    formatter.converter = customTime
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
