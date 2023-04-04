import requests
import json
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
mydb = client["rkit"]
mycol = mydb["plans"]
k=0
operator_id=4
# mycol.update_one(
#     { "operator_id": operator_id },
#     { "$set": { "operator_name": "Vodafone" } },
    
# )

# exit()
for state_name in ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]:
    url = f"https://digitalcatalog.paytm.com/dcat/v1/browseplans/mobile/7166?channel=HTML5&version=2&per_page=20&sort_price=asce&pagination=1&circle={state_name.replace(' ', '%20')}&operator=BSNL"
    response = requests.get(url)
    data = response.json()
    plans=data['groupings']
    k=k+1
    arr=[]
    cirlce_plans=[]
    for plan in plans:
        arr.append(plan["productList"])
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            obj={
                "amount": arr[i][j]["price"], 
                "validity": arr[i][j]["validity"],
                "description": arr[i][j]["description"],
                "is_valid": 1
            }
            cirlce_plans.append(obj)
    circle_id=k
    
    # print(mydb.list_collection_names())
    # collection = db.test_collection
    mycol.update_one(
    { "operator_id": operator_id, "circles.circle_id": circle_id },
        { "$set": { "circles.$.plan": cirlce_plans } },
        upsert=True
    )
    print(f"{state_name} done")


    # with open(f"{state_name}.json", 'w') as f:
    #     json.dump(arr, f)




# collection.update_one(
#     {"_id": 1},
#     {"$push": {"scores": 89}}
# )