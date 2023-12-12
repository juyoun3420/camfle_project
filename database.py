import pyrebase
import json
import array

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )

            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()
            
    def insert_item(self, name, data, img_path):
        item_info ={
            "price": data['price'],
            "okprice": data['okprice'],
            "seller": data['seller'],
            "addr": data['addr'],
            "category": data['category'],
            "status": data['status'],
            "level": data['level'],
            "sold": False,
            "buyer": "",
            "img_path": img_path,
            "click_count": 0
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'],
            "pw": pw
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        
        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                
                if value['id'] == id_string:
                    return False
                return True
            
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            
            if value['id'] == id_ and value['pw'] == pw_:
                return True
            
        return False
        
    def get_items(self):
        items=self.db.child("item").get().val()
        
        if items is not None:
            return items
        else :
            return {}
    
    def get_top_three_items(self):
        items=self.get_items()
        sorted_items = sorted(items.items(), key=lambda x:x[1].get('click_count', 0), reverse=True)
        top_three_items = dict(sorted_items[:3])
        
        return top_three_items
    
    def add_click(self, name):
        item = self.get_item_byname(name)
        click_count = item.get('click_count', 0)
        click_count += 1

        item_ref = self.db.child("item").child(name)
        item_ref.update({"click_count": click_count})

        return True
    
    def get_items_bycategory(self,cate):
        items=self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value=res.val()
            key_value=res.key()
            
            if value['category'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value", target_value)
        new_dict={}
            
        for k,v in zip(target_key, target_value):
             new_dict[k]=v
                
        return new_dict
    
    def get_item_byseller(self, name):
        items=self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value=res.val()
            key_value=res.key()
            
            if value['seller'] == name:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value", target_value)
        new_dict={}
            
        for k,v in zip(target_key, target_value):
             new_dict[k]=v
                
        return new_dict
    
    def get_review_byseller(self, name):
        items = self.db.child("item").get()
        reviews = self.db.child("review").get()

        target_value = []
        target_key = []

        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['seller'] == name and value['sold'] == True:
                if reviews:
                    for rev_res in reviews.each():
                        rev_value = rev_res.val()
                        rev_key_value = rev_res.key()
                        if rev_key_value == key_value:
                            target_value.append(rev_value)
                            target_key.append(rev_key_value)

        print("######target_value", target_value)

        new_dict = {}

        for k, v in zip(target_key, target_value):
            new_dict[k] = v

        return new_dict
    
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
                return target_value
    
    def get_item_bylike(self, name):
        likes = self.db.child("heart").child(name).get()
        items = self.db.child("item").get()
        
        target_value = []
        target_key = []

        for like_res in likes.each():
            like_value = like_res.val()
            like_key_value = like_res.key()

            if like_value['interested'] == 'Y':
                for res in items.each():
                    value = res.val()
                    key_value = res.key()
                    if like_key_value == key_value:
                        target_value.append(value)
                        target_key.append(key_value)
                        
        print("######target_value", target_value)

        new_dict = {}

        for k, v in zip(target_key, target_value):
            new_dict[k] = v

        return new_dict
        
    def update_sold(self, uid, name, data):
        items = self.db.child("item").get()
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                item_ref = self.db.child("item").child(name)
                target_value = res.val()
                target_value['sold'] = True
                target_value['buyer'] = uid
                item_ref.update(target_value)
                return target_value
        
    def reg_review(self, uid, data, img_path):
        review_info ={
            "title": data['title'],
            "rate": data['reviewStar'],
            "review": data['reviewContents'],
            "writer": uid,
            "img_path": img_path
        }
        self.db.child("review").child(data['name']).set(review_info)
        return True
    
    def get_reviews(self ):
        reviews = self.db.child("review").get().val()
        
        if reviews is not None:
            return reviews
        else :
            return {}
    
    def get_review_byname(self, name):
        reviews = self.db.child("review").get()
        target_value=""
        print("#########", name)
        for res in reviews.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
                return target_value
            
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value
        
        for res in hearts.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value
    
    
    def update_heart(self, user_id, isHeart, item):
        heart_info ={
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    