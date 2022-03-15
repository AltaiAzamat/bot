import json 
 
def add_cart_new_meal(meal_data, user_id): 
    with open('cart.json', 'r', encoding="utf-8") as json_file: 
        user_id = str(user_id) 
        data = json.load(json_file) 
        json_file.close() 
        cart = data.get('cart') 
        if not cart.get(user_id, None): 
            file = open('cart.json', 'w', encoding="utf-8") 
            cart[user_id]=[meal_data] 
            data['cart'] = cart  
            json.dump(data, file, indent=4) 
            file.close() 
            return {"status":True, "message":"Блюдо добавлено в корзину"} 
        else: 
            cart =data.get('cart') 
            file = open('cart.json', 'w', encoding="utf-8") 
            cart[user_id].append(meal_data) 
            data['cart'] = cart 
            json.dump(data ,file, indent=4) 
            file.close() 
            return {"status":True, "message":"Блюдо добавлено в корзину"} 
 
 
                     
# meal_data = {"name":"Босо", "price":"200"}           это работает! не удаляй так добавляем в карт джйсон 
# meal_data = {"name":"Жалап", "price":"100"} 
# meal_data = {"name":"Жарма", "price":"50"} 
# add_cart_new_meal(meal_data=meal_data, user_id="322819743") 
 
def get_user_cart(user_id):
    user_id = str(user_id)
    with open("cart.json", 'r', encoding="utf-8") as file:
        data=json.load(file)
        cart = data['cart']
        if not cart.get(str(user_id),None):
            response = {
                "status":True, 
                "message":"Пустая корзина", 
                "data":[]
                }
            return response
        else:
            user_data = cart.get(user_id)
            response = {
                "status":True, 
                "message":"Блюда в вашей корзине", 
                "data":user_data
                }
            return response
 
user_id ='322819743' 
print(get_user_cart(user_id=user_id)) 
             
             
 
# data={ 
#     "cart":{ 
#         "322819743":[ 
#             {"name":"Босо", "price": "128"} meal_data, 
#             {"name":"Босо", "price": "128"}, 
#         ], 
#         "338779081":[ 
             
#         ] 
#     } 
# }