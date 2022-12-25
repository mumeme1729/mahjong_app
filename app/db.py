# -*- coding: utf-8 -*-
import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session



# 設定ファイルを読み込む
with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)


user_name = settings['db']['DB_USER']
password = settings['db']['DB_PASSWORD']
host = settings['db']['DB_HOST']
database_name = settings['db']['DB_NAME']
port = settings['db']['DB_PORT']

DATABASE = 'postgresql://%s:%s@%s:%s/%s' % (
    user_name,
    password,
    host,
    port,
    database_name,
)

# DBとの接続
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False,
    # timezoneの指定をしないと取り出す時すべてutc表示になる
    connect_args={"options": "-c timezone=Asia/Tokyo"}
)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するか
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

# modelで使用する
Base = declarative_base()
# DB接続用のセッションクラス、インスタンスが作成されると接続する
Base.query = session.query_property()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()