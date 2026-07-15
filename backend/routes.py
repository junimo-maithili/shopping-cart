from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)


@api.route("/submitSiteData", methods=["POST"])
def submitSite():
    global budgetData
    data = request.get_json()

    budget = data["budgetInfo"]
    budgetData = budget

    return jsonify({
        "message": "Received",
        "data": data
    })

@api.route("/submitExtensionData", methods=["POST"])
def submitExtension():
    global priceData
    data = request.get_json()

    price = data["priceInfo"]
    priceData = price

    return jsonify({
        "message": "Received",
        "data": data
    })

@api.route("/budgetAnalysis", methods=["GET"])
def budgetAnalysis():
    difference = budgetData - priceData
    percentage = priceData/budgetData
    message = ""

    if percentage <= 1.0:
        message = "Under budget, this is ok!"
    elif priceData/budgetData <= 1.25:
        message = "This is a little over your budget. Be cautious of your purchase."
    else:
        message = "This purchase is WAYYYY over your budget. Don't even think about it..."
    

    
    return jsonify({
        "message": "Received",
        "difference": difference,
        "percentage": percentage,
        "message": "message"
    })