from flask import Flask, jsonify
import requests
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/api/<token>/muhammedkaanyavuz', methods=['GET'])
def check_token_full(token):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Authorization": token
    }

    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data["id"]
            username = user_data["username"]
            discriminator = user_data["discriminator"]
            creation_date = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        
            servers_response = requests.get(f"https://discord.com/api/v9/users/@me/guilds", headers=headers)
            servers = servers_response.json()

           
            friends_response = requests.get(f"https://discord.com/api/v9/users/@me/relationships", headers=headers)
            friends_data = friends_response.json()
            friends_count = len(friends_data)
            
            
            server_info = [{"name": server["name"], "id": server["id"]} for server in servers]

           
            friends_info = [{"username": friend["user"]["username"], "id": friend["id"]} for friend in friends_data]

            result = {
                "status": "success",
                "data": {
                    "id": user_id,
                    "username": f"{username}#{discriminator}",
                    "creation_date": creation_date,
                    "avatar_url": f"https://cdn.discordapp.com/avatars/{user_id}/{user_data.get('avatar', 'default_avatar_id')}.png",
                    "banner_url": f"https://cdn.discordapp.com/banners/{user_id}/{user_data.get('banner', 'default_banner_id')}.png",
                    "locale": user_data.get("locale", "Not Available"),
                    "nsfw_allowed": user_data.get("nsfw_allowed", False),
                    "mfa_enabled": user_data.get("mfa_enabled", False),
                    "premium_type": user_data.get("premium_type", 0),
                    "verified": user_data.get("verified", False),
                    "phone": user_data.get("phone", None),
                    "email": user_data.get("email", None),
                    "servers_count": len(servers),
                    "friends_count": friends_count,

                    "servers": server_info,
            
                    "friends": friends_info
                },
                "code": 200
            }
        elif response.status_code == 401:
            result = {"status": "error", "message": "Invalid token", "code": 401}
        elif response.status_code == 403:
            result = {"status": "error", "message": "Locked token", "code": 403}
        else:
            result = {"status": "error", "message": "Unknown error", "code": 500}
    except Exception as e:
        result = {"status": "error", "message": str(e), "code": 500}

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=80)
