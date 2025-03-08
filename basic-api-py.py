from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/updates')
def updates():
    send = {
        "ID": "1232133",
        "GuildID": "XXXXXXX",
        "ChannelID": "XXXXXXX",
        "CreatedTs": 3333333,
        "EditedTs": 3333333,
        "AuthorID": "XXXXXXX",
        "AuthorName": "kokofixcomputers",
        "AuthorImage": "https://cdn.discordapp.com/avatars/1096839213313446019/b614a5ea08657b33de938e0152c6c0ce?size=1024",
        "Content": "This is a test",
        "CleanContent": "This is a test",
        "Image": "https://cdn.discordapp.com/avatars/1096839213313446019/b614a5ea08657b33de938e0152c6c0ce?size=1024",
    }
    return jsonify(send)

app.run(host='0.0.0.0', port=23235)