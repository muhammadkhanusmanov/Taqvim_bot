import json
from get_request import get_data
#Create Like counting class
class DB:
    def __init__(self, db_path):
        #Initialize the database
        #Open the database file if it exists, otherwise create a new database file
        self.db_path = db_path
        try:
            with open(db_path, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}
            #Save the database to the database file
            with open(db_path, 'w') as f:
                json.dump(self.db, f, indent=4)
    def starting(self,chat_id):
        if not (chat_id in self.db['users'].keys()):
            self.db['users'][str(chat_id)]={'lang':'uz','obuna':False,'img':'','video':'','oxirgi_amal':'','page':0,'data':{},'con':1}
        return None
    def obuna(self,data:bool,chat_id):
        self.db['users'][str(chat_id)]['obuna']=data
        return None
    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f, indent=4)
    def til(self,chat_id):
        return self.db['users'][str(chat_id)]['lang']
    def kanal(self):
        return self.db['admin']['obuna']
    def get_til(self,chat_id,lang):
        self.db['users'][str(chat_id)]['lang']=lang
        return None
    def eslatma(self,chat_id):
        return self.db['users'][str(chat_id)]['eslatma']
    def admins(self):
        return self.db['admin']['admins']
    def get_amal(self,chat_id):
        return self.db['users'][str(chat_id)]['oxirgi_amal']
    def add_amal(self,chat_id,amal):
        self.db['users'][str(chat_id)]['oxirgi_amal']=amal
        return None
    def get_city(self):
        return self.db['data_city']
    def user(self):
        return self.db['users']
    def get_page(self,chat_id):
        return self.db['users'][str(chat_id)]['page']
    def add_page(self,chat_id,n):
        self.db['users'][str(chat_id)]['page']=n
        return None
    def add_data(self,chat_id,data):
        self.db['users'][str(chat_id)]['data']=data
        return None
    def get_d(self,chat_id,date,lang,lat):
        data=self.db['users'][str(chat_id)]['data']
        if data.get(lang+lat,False):
            if data[lang+lat].get(date,False):
                tz=self.db['users'][str(chat_id)]['data'][lang+lat]['tz']
                ans=self.db['users'][str(chat_id)]['data'][lang+lat][date]
                return ans,tz
            else:
                data=get_data(date,lang,lat)
                self.add_data(chat_id,data)
                self.save()
                return self.get_d(chat_id,date,lang,lat)
        else:
            data=get_data(date,lang,lat)
            self.add_data(chat_id,data)
            self.save()
            return self.get_d(chat_id,date,lang,lat)
    def get_admins(self):
        return self.db['admin']['admins']
    def add_admin(self,user_name):
        self.db['admin']['admins'].append(user_name)
        return None
    def get_members(self):
        return len(self.db['users'])
    def add_kanal(self,name):
        self.db['admin']['obuna']='https://t.me/'+name
        return None
    def add_img(self,chat_id,img):
        self.db['users'][str(chat_id)]['img']=img
        return None
    def add_video(self,chat_id,video):
        self.db['users'][str(chat_id)]['video']=video
        return None
    def get_imgs(self,chat_id):
        return self.db['users'][str(chat_id)]['img']
    def get_video(self,chat_id):
        return self.db['users'][str(chat_id)]['video']             

