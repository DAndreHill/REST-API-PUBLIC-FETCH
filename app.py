from flask import Flask, jsonify, send_from_directory
import httpx

app = Flask(__name__)
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json"


@app.route("/items", methods=["GET"])
async def get_items():
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()

        data = response.json()

        filtered = [
            item for item in data.get("Results", [])
            if item.get("GroupName") == "Active Safety System"
        ]

        return jsonify(filtered), 200

    except httpx.HTTPStatusError as err:
        return jsonify({
            "error": f"HTTP error: {err}"
        }), 502

    except httpx.RequestError as err:
        return jsonify({
            "error": f"Network error: {err}"
        }), 503

    except ValueError:
        return jsonify({
            "error": "Invalid JSON response"
        }), 502


if __name__ == "__main__":
    app.run(debug=True, port=5001)
