import json
from main import app
from db import get_db
from datetime import datetime
from starlette.testclient import TestClient



client = TestClient(app)

def test_put_log_history():
    dt = datetime.now()
    
    # OKパターン
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 200

#device_id
def test_put_log_history_device_id_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_id not found"


def test_put_log_history_device_id_long():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e380178f495735a00000000000100114e380178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_id is oversized"


#meter_id
def test_put_log_history_meter_id_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="meter_id not found"
    

def test_put_log_history_meter_id_long():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A00000000000001202123AZ000015AB3A00000000000001202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="meter_id is oversized"


#device_type
def test_put_log_history_device_type_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_type not found"
    

def test_put_log_history_device_type_long():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LFLFLFLFLFLFLFLFLFLFLFLFLFLFLF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_type is oversized"


#device_type
def test_put_log_history_event_category_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="event_category not found"
    

def test_put_log_history_event_category_long():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログログログログログログログログログログログログログログログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="event_category is oversized"


#event_info
def test_put_log_history_event_info_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="event_info not found"
    

def test_put_log_history_event_info_long():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信NILM送信NILM送信NILM送信NILM送信NILM送信NILM送信NILM送信NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="event_info is oversized"


#log_detail
def test_put_log_history_log_detail_long():
    dt = datetime.now()
    s=""
    for i in range(1024):
        s+= "A"
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": s,
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="log_detail is oversized"


#device_mac
def test_put_log_history_device_mac_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_mac not found"
    

def test_put_log_history_device_mac_format1():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01:02:03:04:05:06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_mac is Improper format"

def test_put_log_history_device_mac_format2():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05333-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_mac is Improper format"


def test_put_log_history_device_mac_format3():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_mac is Improper format"


def test_put_log_history_device_mac_long():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06-01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="device_mac is oversized"


#group_node
def test_put_log_history_group_node_none():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="group_node not found"
    

def test_put_log_history_group_node_format1():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1.1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="group_node is Improper format"

def test_put_log_history_group_node_format2():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1,r",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="group_node is Improper format"


def test_put_log_history_group_node_format3():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="group_node is Improper format"


def test_put_log_history_group_node_format4():
    dt = datetime.now()
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": ",1",
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="group_node is Improper format"


def test_put_log_history_group_node_long():
    dt = datetime.now()
    s=""
    for i in range(1024):
        s+= "1,1"
        if i !=1023:
            s+=","
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": s,
              "option1": "",
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="group_node is oversized"


#option1
def test_put_log_history_option1_long():
    dt = datetime.now()
    s=""
    for i in range(1024):
        s+= "A"
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": s,
              "oprion2":"",
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="option1 is oversized"


#option2
def test_put_log_history_option2_long():
    dt = datetime.now()
    s=""
    for i in range(1024):
        s+= "A"
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "option2": s,
              "option3": "",   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="option2 is oversized"


#option3
def test_put_log_history_option3_long():
    dt = datetime.now()
    s=""
    for i in range(1024):
        s+= "A"
    response = client.put(
        "/log_history/put", 
        json={
              "occur_date": str(dt),
              "device_id": "0178f495735a00000000000100114e38",
              "meter_id" : "1202123AZ000015AB3A0000000000000",
              "device_type": "LF",
              "event_category":"ログ",
              "event_info": "NILM送信",
              "log_detail": "",
              "device_mac": "01-02-03-04-05-06",
              "group_node": "1,1",
              "option1": "",
              "oprion2":"",
              "option3": s,   
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] =="option3 is oversized"

## get ##

def test_get_log_history():
    response = client.get("/log_history/get")
    assert response.status_code == 200


def test_get_log_history_id():
    response = client.get("/log_history/get/id/1")
    assert response.status_code == 200

def test_get_log_history_id_not_found():
    response = client.get("/log_history/get/id/999999000")
    assert response.status_code == 404


def test_get_log_history_device_id():
    response = client.get("/log_history/get/device_id/0178f495735a00000000000100114e38")
    assert response.status_code == 200


def test_get_log_history_device_id_not_found():
    response = client.get("/log_history/get/device_id/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    assert response.status_code == 404


def test_get_log_history_meter_id():
    response = client.get("/log_history/get/meter_id/1202123AZ000015AB3A0000000000000")
    assert response.status_code == 200


def test_get_log_history_meter_id_not_found():
    response = client.get("/log_history/get/meter_id/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    assert response.status_code == 404


def test_get_log_history_device_type():
    response = client.get("/log_history/get/device_type/LF")
    assert response.status_code == 200


def test_get_log_history_device_type_not_found():
    response = client.get("/log_history/get/meter_id/xx")
    assert response.status_code == 404


def test_get_log_history_event_category():
    response = client.get("/log_history/get/event_category/ログ")
    assert response.status_code == 200


def test_get_log_history_event_category_not_found():
    response = client.get("/log_history/get/event_category/xx")
    assert response.status_code == 404


def test_get_log_history_event_info():
    response = client.get("/log_history/get/event_info/NILM送信")
    assert response.status_code == 200


def test_get_log_history_event_info_not_found():
    response = client.get("/log_history/get/event_info/xx")
    assert response.status_code == 404

def test_get_log_history_device_mac():
    response = client.get("/log_history/get/device_mac/01-02-03-04-05-06")
    assert response.status_code == 200


def test_get_log_history_device_mac_not_found():
    response = client.get("/log_history/get/device_mac/01-01-01-01-01-01")
    assert response.status_code == 404


def test_get_log_history_group_node():
    response = client.get("/log_history/get/group_node/1,1")
    assert response.status_code == 200


def test_get_log_history_group_node_not_found():
    response = client.get("/log_history/get/group_node/99,99")
    assert response.status_code == 404