import instaloader
from datetime import datetime
import json
import os

def loadJsonFile(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def exportDataToTextFile(file, data):
    with open(file, 'w') as f:
        f.write(json.dumps(data))

def GetInfoFromUsername(target_username):
    # Config credentiels
    L = instaloader.Instaloader()
    L.context.user_agent = 'Mozilla/5.0 (Linux; Android 12; vivo 1939 Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36 Instagram 244.0.0.17.110 Android (31/12; 480dpi; 1080x2278; vivo; vivo 1939; 2004; qcom; en_US; 383877305)'
    print("[Debug] Login...")
    L.login("USERNAME", "PASSWORD")
    print("[Debug] Login successfuly")

    print("[Debug] Profile loading...")
    profile = instaloader.Profile.from_username(L.context, target_username)
    print("[Debug] Profile loaded")

    # Create followees list
    # Profiles that are followed by given user.
    print("[Debug] Followees processing...")
    followees_list = []
    followees_id_list = []
    for followee in profile.get_followees():
        followees_list.append(followee.__dict__["_node"])
        followees_id_list.append(followee.__dict__["_node"]["username"])
    print("[Debug] Followees processing successfuly")

    # Create followers list 
    # Profiles that follow given user.
    print("[Debug] Followers processing...")
    followers_list = []
    followers_id_list = []
    for followers in profile.get_followers():
        followers_list.append(followers.__dict__["_node"])
        followers_id_list.append(followers.__dict__["_node"]["username"])
    print("[Debug] Followers processing successfuly")

    print("[Debug] Saving data...")
    save_data = {}
    save_data["followers_id_list"] = followers_id_list
    save_data["followees_id_list"] = followees_id_list

    now = datetime.now()
    now_string = now.strftime("%d-%b-%Y_%H-%M-%S")

    exportDataToTextFile("save/"+target_username+"_"+now_string+".json", save_data)

    print("[Debug] Data has been saved")

def compareDataFiles():
    # Select files
    files = os.listdir("save")
    username_list = []
    for file_name in files:
        username_list.append((file_name.split("_")[0]).lower())
    username_list = list(dict.fromkeys(username_list))

    for idx,username in enumerate(username_list):
        print("["+str(idx)+"] " + username)

    print("")
    select_username_idx = input("[input] Select username : ")

    for idx,file_name in enumerate(files):
        if username_list[int(select_username_idx)] in file_name:
            print("["+str(idx)+"] " + file_name)

    print("")
    select_base_file_idx = input("[input] Select base file : ")
    select_new_file_idx = input("[input] Select new file : ")

    # Load files
    base_file = loadJsonFile("save/" + files[int(select_base_file_idx)])
    new_file = loadJsonFile("save/" + files[int(select_new_file_idx)])

    print("")
    print("======================[ Followers lose ]=========================")
    # Lose follower
    for user_id in base_file["followers_id_list"]:
        if user_id not in new_file["followers_id_list"]:
            print(user_id)
    print("======================[ Followers get  ]=========================")
    # Get follower
    for user_id in new_file["followers_id_list"]:
        if user_id not in base_file["followers_id_list"]:
            print(user_id)
    print("======================[ Followees lose ]=========================")
    # Lose followee
    for user_id in base_file["followees_id_list"]:
        if user_id not in new_file["followees_id_list"]:
            print(user_id)
    print("======================[ Followees get  ]=========================")
    # Get followee
    for user_id in new_file["followees_id_list"]:
        if user_id not in base_file["followees_id_list"]:
            print(user_id)
    print("=================================================================")

def header():
    print("=================================================================")
    print("                                 _                     ")
    print("               /\               | |                    ")
    print("              /  \   _ __   __ _| |_   _ ___  ___ _ __ ")
    print("             / /\ \ | '_ \ / _` | | | | / __|/ _ \ '__|")
    print("            / ____ \| | | | (_| | | |_| \__ \  __/ |   ")
    print("           /_/    \_\_| |_|\__,_|_|\__, |___/\___|_|   ")
    print("                                    __/ |              ")
    print("               NothingElse.fr      |___/               ")
    print("=================================================================")
    print("[Python Script] Instagram followers & followees analyser.")
    print("=================================================================")
    print("")

def choice():
    # Select choice
    print("[1] Save data from IG username")
    print("[2] Compare saves")
    print("")
    choice_resp = input("[input] Select choice : ")

    if(choice_resp == "1"):
        target_username = input("[input] What username : ")
        GetInfoFromUsername(target_username)
    elif(choice_resp == "2"):
        compareDataFiles()
    else:
        print("[Error] Unknown choice")
    print("\n\n")

def main():
    while 1 :
        header()
        choice()

os.system('cls')
main()