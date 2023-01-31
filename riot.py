#라이엇 api

#todo
# 1. 각자 데이터 출력하게끔 메소드 생성 및 주석 작성
# 2. 키 분리
# 3. 모듈화 후 디스코드 봇에서 사용

#Riot API
#userID 입력했을때 id,accountid,puuid 뱉음
#api에서 encryptedID를 요구할 땐 id를 입력하면 됨

import requests
import json
class RiotData:
    def __init__(self,userID): #set
        with open('key.json') as json_file:
            json_data = json.load(json_file)
        self.userID = userID
        self.api_key = json_data['Riot_Key'] #로컬에 있는 json 파일의 value로 키 세팅
        self.url = "https://kr.api.riotgames.com"
        self.DataDragon = "http://ddragon.leagueoflegends.com/cdn/11.6.1/data/ko_KR"
    
    def getEncryptedId(self): #암호화된 id 리턴
        url = self.url+"/lol/summoner/v4/summoners/by-name/"+self.userID+"?api_key="+self.api_key
        res = requests.get(url)
        return res.json().get('id')
    
    def getAccountID(self): #Account id 리턴
        url = self.url+"/lol/summoner/v4/summoners/by-name/"+self.userID+"?api_key="+self.api_key
        res = requests.get(url)
        return res.json().get('accountId')
    
    def getUserData(self): #유저 정보
        url = self.url+"/lol/summoner/v4/summoners/by-name/"+self.userID+"?api_key="+self.api_key
        res = requests.get(url)
        sum_Lev = res.json().get('summonerLevel') #유저 레벨
        sum_ID = res.json().get('id')  #전적검색 위한 소환사ID
        print("소환사 레벨 : ", sum_Lev)
        print("summonerID : ", sum_ID)

        url_League = self.url + "/lol/league/v4/entries/by-summoner/" + sum_ID + "?api_key=" + self.api_key
        res_League = requests.get(url_League)
        que_List = res_League.json()  #소환사 티어, 승률, json파일 파싱
        
        for que_Data in que_List:
            que_Type = que_Data.get('queueType')
            if(que_Type == "RANKED_SOLO_5x5"):
                print("솔로랭크 정보입니다.")  #솔랭 전적 출력
                print("티어 : ", que_Data.get('tier'), que_Data.get('rank'), que_Data.get('leaguePoints'), "포인트")
                #티어, 랭크, 리그포인트 출력
                win = int(que_Data.get('wins'))
                lose = int(que_Data.get('losses'))
                print("승률 : ", round((win/(lose+win))*100, 1), "%")  #승률 출력
            elif(que_Type == "RANKED_FLEX_SR"):
                print("자유랭크 정보입니다.")  #자랭 전적 출력
                print("티어 : ", que_Data.get('tier'), que_Data.get('rank'), que_Data.get('leaguePoints'), "포인트")
                #티어, 랭크, 리그포인트 출력
                win = int(que_Data.get('wins'))
                lose = int(que_Data.get('losses'))
                print("승률 : ", round((win/(lose+win))*100, 1), "%")  #승률 출력
            else:
                print("자료가 없습니다.")

    def getChampRotation(self,*champ): #챔프 로테이션
        if not champ: #인자 안 들어올 때
            url = self.url + "/lol/platform/v3/champion-rotations"+"?api_key="+self.api_key
            res = requests.get(url)
            rotation_list = res.json().get('freeChampionIds') #type = list
            print("챔피언 리스트 배열 : ",rotation_list,"\n")
        
            url = self.DataDragon + "/champion.json"
            res = requests.get(url)
            champ_data = res.json().get('data')
            sum_rotation = []
            for champ_name , chame_des in champ_data.items():
                for rotation in rotation_list:
                    if champ_data.get(champ_name).get('key') == str(rotation):
                        sum_rotation.append(champ_data.get(champ_name).get('name'))
            return sum_rotation
        else: #인자 들어올 떄
            url = self.DataDragon + "/champion.json"
            res = requests.get(url)
            champ_data = res.json().get('data')
            for champ_name , chame_des in champ_data.items():
                #print(champ_data.get(champ_name).get('key'))
                if champ_data.get(champ_name).get('key') == str(champ[0]):
                    return champ_data.get(champ_name).get('name')
        #return champ_data
        
    def getCurrentGame(self): #인게임 출력 #챔프선택 단계일때 예외처리해야함
        url = self.url+"/lol/spectator/v4/active-games/by-summoner/"+ self.getEncryptedId() +"?api_key="+self.api_key
        res = requests.get(url)
        participants = res.json().get('participants') #type = list
        for user in participants:
            print(user.get('summonerName')," ",self.getChampRotation(user.get('championId')))

#userID = input("userID : ")
#test = RiotData(userID)
#print(" ",test.getCurrentGame())
#test.getUserData()
#test.getChampRotation()