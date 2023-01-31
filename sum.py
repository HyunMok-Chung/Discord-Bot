import requests
import json

api_key = "API 키"

print("!소환사: 플레이어 검색")
selectnum = input("명령어를 입력해주세요 : ")

if selectnum == "!소환사": #명령어
    name = input("소환사의 닉네임을 입력해주세요: ")
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name
    res = requests.get(URL, headers={"X-Riot-Token": api_key})
    if res.status_code == 200: #코드가 200일때
        
        resobj = json.loads(res.text)
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        rankinfo = json.loads(res.text)
        print("소환사 이름: "+name)
        for i in rankinfo:
            if i["queueType"] == "RANKED_SOLO_5x5": #솔랭
                
                print("Solo Rank:")
                print(f'tier: {i["tier"]} {i["rank"]}')
                print(f'win : {i["wins"]}games, lose : {i["losses"]}games')
            else: # 자랭
                
                print("Free Rank :")
                print(f'tier : {i["tier"]} {i["rank"]}')
                print(f'win : {i["wins"]}games, lose: {i["losses"]}games')
    else:
        # 코드가 200이 아닐때(즉 찾는 닉네임이 없을때)
        selectnum("No Data")
        
        ##test branch