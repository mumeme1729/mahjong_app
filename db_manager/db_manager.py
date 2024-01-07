import psycopg2

class DBManager:
    host = "localhost"  # データベースサーバーのホスト名またはIPアドレス
    dbname = "mahjong_db_container"  # データベース名
    user = "postgres"  # データベースのユーザー名
    password = "postgres"  # データベースのパスワード
    port = "5432"  # PostgreSQLのポート番号（デフォルトは5432
    
    def __init__(self):
        # データベース接続情報
        pass

    def connect(self):
        conn = psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            port=self.port
        )
        
        return conn


    def __get_games(self):
        try:
            connect = self.connect()
            cur = connect.cursor()
            # SQLクエリの実行
            cur.execute("SELECT * FROM games;")

            # 結果の取得
            rows = cur.fetchall()
            game_ids = []
            for row in rows:
                game_ids.append(row[0])
            
            return game_ids
        except Exception as e:
            raise e
        finally:
            connect.close()
    
    def update_score(self, score, gameresult_id):
        try:
            connect = self.connect()
            cur = connect.cursor()
            q = f"""
                UPDATE gameresults
                SET score = {score}
                WHERE id = '{gameresult_id}';
            """
            cur.execute(q)
            # cur.fetchall()
            connect.commit()
        except Exception as e:
            raise e
        finally:
            connect.close()

    def get_gameresults(self):
        try:
            game_ids = self.__get_games()
            connect = self.connect()
            cur = connect.cursor()
            for game_id in game_ids:
                q = f"""
                    SELECT * FROM gameresults
                    where game = '{game_id}';
                """
                cur.execute(q)
                rows = cur.fetchall()
                total = 0
                rank1_id = None
                for row in rows:
                    # print(row)
                    if not row[3] == 1:
                        total += row[4]
                    else:
                        rank1_id = row[0]
                
                rank1_score = -total
                # print(rank1_score)
                # print(rank1_id)
                # Db内のデータを更新する
                self.update_score(rank1_score, rank1_id)
        except Exception as e:
            raise e
        finally:
            connect.close()



if __name__ == '__main__':
    db_manager = DBManager()
    db_manager.get_gameresults()
    