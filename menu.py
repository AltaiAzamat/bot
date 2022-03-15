import json

def add_new_meal(name, price, category):
    with open("menu.json","r",encoding="utf-8") as json_file:
        data = json.load(json_file)
        meal_data = {
            "name":name,
            "price":price
        }
        json_file.close
        if not data.get("menu",None):
            file = open("menu.json", "w", encoding="utf-8")
            new_data = {
                "menu":{
                    category:[meal_data]
                }
            }
            json.dump(new_data, file,indent=4)
            return True
        else:
            menu = data["menu"]
            if not menu.get(category, None):
                file = open("menu.json", "w", encoding="utf-8")
                menu[category]=[meal_data]
                data["menu"] = menu
                json.dump(data,file, indent=4)
                return True
            else:
                file = open("menu.json", "w", encoding="utf-8")
                menu[category].append(meal_data)
                data["menu"] = menu
                json.dump(data,file, indent=4)
                return True

# add_new_meal("Двойной бургер", 400, "FastFood")

def get_categories():
    with open('menu.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
        if not data.get('menu', None):
            return {"status":False, "message":"Нету меню", "data":[]}
        else:
            menu = data['menu']
            categories = menu.keys()
            return {
                "status":True,
                "message": "Успешно!", 
                "data": categories
            }

def get_by_category(category):
    with open('menu.json', 'r', encoding="utf-8") as file:
        data = json.load(file) 
        if not data.get('menu', None): # меню есть в файле
            return {"status":False, "message":"Нету меню", "data":[]}
        else: # если меню есть  
            menu = data['menu']
            if not menu.get(category, None): # проверка наличие категории внутри меню
                return {"status":False, "message":"Нету такой категории", "data":[]}
            else:
                category_data = menu.get(category)
                return {
                    "status":True,
                    "message": "Успешно!", 
                    "data": category_data
                }








