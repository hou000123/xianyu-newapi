from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NEW_API_URL = os.getenv("SITE_URL", "https://www.si-hk.cn/")
NEW_API_TOKEN = os.getenv("NEWAPI_API_KEY")

@app.route('/get_voucher', methods=['POST'])
def get_voucher():
    # 接收來自 XianYuSmart 的觸發數據（例如訂單號、商品金額等）
    data = request.json
    
    # 根據閒魚商品金額動態設定配額 (假設 1 元人民幣 = 500000 額度)
    # 你也可以在 XianYuSmart 固定傳入特定參數
    quota = data.get("quota", 500000) 
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NEW_API_TOKEN}"
    }
    
    payload = {
        "name": f"XianYu_Order_{data.get('order_id', 'unknown')}",
        "quota": quota,
        "count": 1
    }
    
    try:
        response = requests.post(NEW_API_URL, json=payload, headers=headers)
        res_json = response.json()
        
        if res_json.get("success") and res_json.get("data"):
            # 提取兌換碼
            voucher_code = res_json["data"][0]["key"]
            
            # 返回給 XianYuSmart 要求的格式 (純文字卡密或固定 JSON)
            return jsonify({
                "code": 200,
                "card_key": voucher_code,
                "msg": "success"
            })
        else:
            return jsonify({"code": 500, "msg": "New API 建立失敗", "detail": res_json}), 500
            
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
