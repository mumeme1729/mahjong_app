# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import database_exists, drop_database
# from db import Base

# @pytest.fixture(scope="function")
# def SessionLocal():
#     """
#     テスト用のDBを作成する。
#     関数毎に一時的にDatabaseを作成
#     そのDatabaseとのsessionをつくることができるSessionmakerインスタンスをテスト関数に渡す
#     各テストケースの終了時にDatabaseを削除
#     """
#     # DBの設定
#     TEST_SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/test_db"
#     engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL,encoding="utf-8",echo=True)

#     assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."

#     # Create test database and tables
#     Base.metadata.create_all(engine)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     # Run the tests
#     yield SessionLocal

#     # Drop the test database
#     drop_database(TEST_SQLALCHEMY_DATABASE_URL)