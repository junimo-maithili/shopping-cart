from flask import Blueprint, request, jsonify
from database import updateDb, sendInfo

api = Blueprint("api", __name__)
budgetData = None
priceData = None
uuid = None
fbId = None



# Gets UUID
@api.route("/submitUUID", methods=["POST"])
def submitUUID():
    global uuid
    data = request.get_json()
    uuid = data["UUID"]

    userInfo = sendInfo(fbId)
    budgetData = userInfo[1]
    priceData = userInfo[2]
    print("budget and price")
    print(budgetData)
    print(priceData)

    return jsonify({
        "message": "Received",
        "data": data
    })

# Gets Firebase UUID
@api.route("/submitFbId", methods=["POST"])
def submitFbId():
    global uuid
    data = request.get_json()
    fbId = data["uuid"]
    updateDb(None, None, None, fbId)

    return jsonify({
        "message": "Received",
        "data": data
    })


# Gets information about a user's budget
@api.route("/submitSiteData", methods=["POST"])
def getBudget():
    global budgetData
    data = request.get_json()

    budget = data["budgetInfo"]
    print("WOW!")
    print(budget)

    print(budgetData)

    updateDb(fbId, budgetData, None, None)
    print("db updated")

    return jsonify({
        "message": "Received",
        "data": data
    })


# Gets information about the price of a given product
@api.route("/submitExtensionData", methods=["POST"])
def getPrice():
    global priceData
    data = request.get_json()

    price = data["priceInfo"]
    
    if fbId and price != priceData:
        updateDb(fbId, None, priceData, None)

    return jsonify({
        "message": "Received",
        "data": data
    })

# Compares price and budget and sends results to the frontend
@api.route("/budgetAnalysis", methods=["GET"])
def budgetAnalysis():
    global budgetData, priceData
    message = ""

    if not budgetData:
        message = "Please enter a budget on the website that you want to follow!"
        return jsonify({
            "difference": 0,
            "percentage": 0,
            "message": message
        })
    
    priceData = float(priceData[1::])
    budgetData = float(budgetData)

    difference = budgetData - priceData
    percentage = priceData/budgetData

    if percentage <= 1.0:
        message = "Under budget, this is ok!"
    elif percentage <= 1.25:
        message = "This is a little over your budget. Be cautious of your purchase."
    else:
        message = "This purchase is WAYYYY over your budget. Don't even think about it..."
    

    return jsonify({
        "difference": difference,
        "percentage": percentage,
        "message": message
    })
