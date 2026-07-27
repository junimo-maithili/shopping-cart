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
    uuid = data["extensionUUID"]


    return jsonify({
        "message": "Received",
        "data": data
    })

# Gets Firebase UUID
@api.route("/submitFbId", methods=["POST"])
def submitFbId():
    global fbId
    data = request.get_json()
    uuid = data["uuid"]
    updateDb(uuid, None, None, fbId)

    return jsonify({
        "message": "Received",
        "data": data
    })


# Gets information about a user's budget
@api.route("/submitSiteData", methods=["POST"])
def getBudget():
    global budgetData

    data = request.get_json()
    print("Received budget request:", data)

    budgetData = data["budgetInfo"]
    uuid = data["uuid"]
    print("budgetData is now:", budgetData)

    updateDb(uuid, budgetData, None, None)

    return jsonify({
        "message": "Received"
    })

# Gets information about the price of a given product
@api.route("/submitExtensionData", methods=["POST"])
def getPrice():
    global priceData
    data = request.get_json()

    price = data["priceInfo"]
    priceData = price
    uuid = data["uuid"]

    print("PRICE UUID:", uuid)
    updateDb(uuid, None, price, None)

    return jsonify({
        "message": "Received",
        "data": data
    })

# Compares price and budget and sends results to the frontend
@api.route("/budgetAnalysis", methods=["GET"])
def budgetAnalysis():
    global budgetData, priceData

    print("budgetAnalysis called")
    print("budgetData =", repr(budgetData))
    print("priceData =", repr(priceData))
    message = ""

    if not budgetData:
        message = "Please enter a budget on the website that you want to follow!"
        return jsonify({
            "difference": 0,
            "percentage": 0,
            "message": message
        })
    
    if priceData == None or budgetData == None:
        return  jsonify({
        "difference": difference,
        "percentage": percentage,
        "message": "NO"
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
