import json
import os

FILE_NAME = "users.json"


# 讀取玩家資料
def load_users():
    if not os.path.exists(FILE_NAME):
        return {}

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


# 儲存玩家資料
def save_users(users):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


# 根據等級判斷境界
def get_realm(level):
    if level >= 10:
        return "金丹"
    elif level >= 7:
        return "築基"
    elif level >= 4:
        return "煉氣後期"
    elif level >= 2:
        return "煉氣中期"
    else:
        return "煉氣初期"


# 升級判斷
def check_level_up(player):
    if player["exp"] >= 100:
        player["exp"] -= 100
        player["level"] += 1
        player["realm"] = get_realm(player["level"])
        print("突破成功！")
        print(f"你的等級提升到 {player['level']}，目前境界為：{player['realm']}")


# 註冊帳號
def register():
    users = load_users()

    username = input("請輸入要註冊的帳號：")
    password = input("請輸入要註冊的密碼：")

    if username in users:
        print("這個帳號已經存在了！")
        return

    users[username] = {
        "password": password,
        "level": 1,
        "exp": 0,
        "money": 100,
        "hp": 100,
        "realm": "煉氣初期"
    }

    save_users(users)
    print("註冊成功！你已踏上修仙之路。")


# 登入帳號
def login():
    users = load_users()

    username = input("請輸入帳號：")
    password = input("請輸入密碼：")

    if username not in users:
        print("查無此帳號！")
        return

    if users[username]["password"] == password:
        print(f"登入成功！歡迎回來，道友 {username}。")
        player_menu(username)
    else:
        print("密碼錯誤！")


# 查看角色資料
def show_player(username):
    users = load_users()
    player = users[username]

    print("\n===== 角色資料 =====")
    print(f"道號：{username}")
    print(f"境界：{player['realm']}")
    print(f"等級：{player['level']}")
    print(f"經驗值：{player['exp']} / 100")
    print(f"生命值：{player['hp']} / 100")
    print(f"靈石：{player['money']}")


# 修煉功能
def train(username):
    users = load_users()
    player = users[username]

    print("\n你開始打坐修煉，吸收天地靈氣……")
    player["exp"] += 25

    print("修煉完成！經驗值 +25")

    check_level_up(player)
    save_users(users)


# 簽到功能
def daily_reward(username):
    users = load_users()
    player = users[username]

    print("\n你完成今日簽到，獲得靈石 100。")
    player["money"] += 100

    save_users(users)


# 外出歷練
def adventure(username):
    users = load_users()
    player = users[username]

    if player["hp"] <= 0:
        print("\n你目前生命值太低，無法外出歷練，請先休息恢復。")
        return

    print("\n你進入後山歷練，遇到了一隻低階妖獸！")
    print("你與妖獸展開戰鬥……")

    player["hp"] -= 20
    player["exp"] += 30
    player["money"] += 50

    if player["hp"] < 0:
        player["hp"] = 0

    print("戰鬥勝利！")
    print("經驗值 +30")
    print("靈石 +50")
    print("生命值 -20")

    check_level_up(player)
    save_users(users)


# 休息恢復
def rest(username):
    users = load_users()
    player = users[username]

    if player["money"] < 30:
        print("\n你的靈石不足，無法休息恢復。")
        return

    player["money"] -= 30
    player["hp"] = 100

    print("\n你花費 30 靈石休息，生命值已恢復到 100。")

    save_users(users)


# 排行榜
def ranking():
    users = load_users()

    if not users:
        print("目前沒有任何玩家資料。")
        return

    sorted_users = sorted(
        users.items(),
        key=lambda item: item[1]["level"],
        reverse=True
    )

    print("\n===== 修仙排行榜 =====")
    for index, (username, data) in enumerate(sorted_users, start=1):
        print(f"{index}. {username}｜等級：{data['level']}｜境界：{data['realm']}｜靈石：{data['money']}")


# 登入後的玩家選單
def player_menu(username):
    while True:
        print("\n===== 修仙系統 =====")
        print("1. 查看角色")
        print("2. 修煉")
        print("3. 每日簽到")
        print("4. 排行榜")
        print("5. 外出歷練")
        print("6. 休息恢復")
        print("7. 登出")

        choice = input("請選擇功能：")

        if choice == "1":
            show_player(username)
        elif choice == "2":
            train(username)
        elif choice == "3":
            daily_reward(username)
        elif choice == "4":
            ranking()
        elif choice == "5":
            adventure(username)
        elif choice == "6":
            rest(username)
        elif choice == "7":
            print("你已登出修仙系統。")
            break
        else:
            print("請輸入 1 到 7。")


# 主選單
def main():
    while True:
        print("\n===== 文字修仙模擬器 =====")
        print("1. 註冊帳號")
        print("2. 登入帳號")
        print("3. 離開系統")

        choice = input("請選擇功能：")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("系統已關閉。")
            break
        else:
            print("請輸入 1、2 或 3。")


main()

