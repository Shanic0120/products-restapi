from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"message":"Pong!"})

@app.route("/products", methods=["GET"]) # Usar para llamar datos del server, GET está por defecto
def getProducts():
    return jsonify({"products":products},{"message":"Product's List"})

@app.route("/products/<string:product_name>")
def getProduct(product_name):
    productsFound = [product for product in products if product["name"]==product_name]
    
    if len(productsFound)>0:
        return jsonify({"product":productsFound[0]})
    else:
        return jsonify({"message":f"Product {product_name} not found"})

@app.route("/products",methods=["POST"])
def addProduct():
    new_product = {
        "name":request.json["name"],
        "price":request.json["price"],
        "quantity":request.json["quantity"]
    }
    products.append(new_product) # Esta función está en la RAM, por lo que los cambios no se mantienen
    return jsonify({"message":"Product added succesfully",
                    "products":products});

@app.route("/products/<string:product_name>",methods=["PUT"])
def updateProduct(product_name):
    productFound = [product for product in products if product["name"]==product_name]
    if len(productFound) > 0:
        productFound[0]["name"] = request.json["name"]
        productFound[0]["price"] = request.json["price"]
        productFound[0]["quantity"] = request.json["quantity"]
        return jsonify({
            "message":"Product updated",
            "product":productFound[0]
        })
    return "Product Not Found"

@app.route("/products/<string:product_name>",methods=["DELETE"])
def deleteProduct(product_name):
    productFound = [product for product in products if product["name"]==product_name]
    if len(productFound) > 0:
        products.remove(productFound[0])
        return jsonify({
            "message":"Product Deleted",
            "products":products
        })
    return "Product Not Found"


if __name__ == "__main__":
    app.run(debug=True,port=4000)