import pprint
import random
import json
import sys
import argparse
import os

from Objects import Obj, Room

parser = argparse.ArgumentParser()
   
parser.add_argument('-s', '--story', default="Demon_King",
    help="specify story default is %(default)s")

args = parser.parse_args()

filename = args.story
save_file = "_SAVE.json"
if ".json" not in filename:
    filename = filename + ".json"


def not_valid(array, user_opt):
    while not user_opt in array:
        print("'%s' Not a Valid Option"%(user_opt))
        user_opt = str(input('\n:'))
    return user_opt

def save(overwrite_data):
    with open(save_file, 'w') as fh:
        json.dump(overwrite_data, fh, indent=4, sort_keys=True)

def Enter_Room(Story_data, RoomID):
    print()
    RoomID = str(RoomID)
    print("Now Entering Room:", RoomID)
    room = Room(Story_data["Rooms"][RoomID])

    print('\n', room.Description, '\n')

    if 'Enemies' in room.__dict__:
        num_enemies = []
        for enemies in room.Enemies:
            enemy = Obj(enemies)
            num_enemies.append(enemy)
        print(f"You find {len(num_enemies)} Enemie(s)")
        print()
        while len(num_enemies) > 0:
            for enemy in room.Enemies:
                enemy = Obj(enemy)
                print(f"{enemy.name} : {enemy.health}/{enemy.max_health}")
                print(f"{Player.name} : {Player.health}/{Player.max_health}")
                while enemy.health > 0:
                    opt_arr = ["1","2"]
                    if Player.mana:
                        print("1) Attack")
                        print("2) Mana Blast")
                    else:
                        print("1) Attack")
                    print()
                    user_opt = not_valid(opt_arr, input(":"))

                    if user_opt == "1":
                        setattr(enemy, 'health', (getattr(enemy, 'health') - getattr(Player, 'attack')))
                    if user_opt == "2":
                        setattr(enemy, 'health', (getattr(enemy, 'health') - getattr(Player, 'mana')))
                    print(f"{enemy.name} : {enemy.health}/{enemy.max_health}")
                    print(f"{Player.name} : {Player.health}/{Player.max_health}")
                Story_data["Rooms"][RoomID]["Enemies"][0] = {"Attributes":enemy.__dict__}
                save(Story_data)
                room.Enemies.pop(0)
                num_enemies.pop(0)

    if 'NPCs' in room.__dict__:
        for npc in room.NPCs:
            NPc = Obj(npc)
            while len(room.NPCs) != 0:
                print(NPc.description)
                opt_arr = []
                for question_index in range(len(NPc.questions)):
                    print("%s) %s"%(question_index+1, NPc.questions[question_index][0]))
                    opt_arr.append(str(question_index+1))
                print("Q) None")
                opt_arr.append("Q")

                user_opt = input('\n:')
                user_opt = not_valid(opt_arr, user_opt)
                if user_opt == "Q":
                    break

                print("%s) %s"%(Player.name, NPc.questions[int(user_opt)-1][0]))
                print("%s) %s"%(NPc.name, NPc.questions[int(user_opt)-1][1]))

    if 'Items' in room.__dict__:
        for item_i in room.Items:
                item = Obj(item_i)
                if item.used == 1:
                    room.Items.remove(item_i)
        if len(room.Items) != 0:
            print("\n%s) xp: %s"%(Player.name,Player.xp))
            opt_arr = []
            while len(room.Items) != 0:
                for item_index in range(len(room.Items)):
                    print("%s) %s" % (item_index+1, room.Items[item_index]["Attributes"]["name"]))
                    opt_arr.append(str(item_index+1))
                print('Q) None')
                opt_arr.append('Q')
                user_opt_i = input(":")
                user_opt_i = not_valid(opt_arr, user_opt_i)
                if user_opt_i == 'Q':
                    break
                item = Obj(room.Items[int(user_opt_i)-1])
                opt_arr = []
                for action_index in range(len(item.actions)):
                    print("%s) %s" % (action_index+1, item.actions[action_index][0]))
                    opt_arr.append(str(action_index+1))
                user_opt = input(":")

                user_opt = not_valid(opt_arr, user_opt)
                if 'xp' in item.actions[0][1]["Attributes"]:
                    if  (getattr(Player, 'xp') + item.actions[0][1]["Attributes"]['xp']) > 0:
                        for attr in item.actions[0][1]["Attributes"]:
                            before = getattr(Player, attr)
                            setattr(Player, attr, (getattr(Player, attr) + item.actions[0][1]["Attributes"][attr]))
                            print("Your '%s' was '%s' and is now '%s'"%(attr, before, getattr(Player, attr)))
                        print("setting '%s' as used "%(item.name))
                        setattr(item, 'used', 1)
                        Story_data["Rooms"][RoomID]["Items"][int(user_opt)-1]["Attributes"] = item.__dict__
                        save(Story_data)
                    else:
                        print(random.choice(["You don't have the funds for that","I can't waste my time on you if you aren't spending anything", "I'm Afraid you don't have enough"]))
                else:
                    for attr in item.actions[0][1]["Attributes"]:
                        before = getattr(Player, attr)
                        setattr(Player, attr, (getattr(Player, attr) + item.actions[0][1]["Attributes"][attr]))
                        print("Your '%s' was '%s' and is now '%s'"%(attr, before, getattr(Player, attr)))
                    print("setting '%s' as used "%(item.name))
                    setattr(item, 'used', 1)
                    Story_data["Rooms"][RoomID]["Items"][int(user_opt)-1]["Attributes"] = item.__dict__
                    save(Story_data)
                room.Items.pop(int(user_opt_i)-1)

    if 'Exits' in room.__dict__:
        opt_arr = []
        for exit_index in range(len(room.Exits)):
            print("%s) %s"%(exit_index+1, room.Exits[exit_index][0]))
            opt_arr.append(str(exit_index+1))

        user_opt = input('\n:')
        not_valid(opt_arr, user_opt)
        print(str(room.Exits[int(user_opt)-1][1]))
        Enter_Room(Story_data, str(room.Exits[int(user_opt)-1][1]))


try:
    with open(save_file, 'r') as fh:
        Story_data = json.load(fh)

    Player_data = Story_data['Player']
    
    Player = Obj(Player_data)
except FileNotFoundError:
    with open(filename,'r') as fh:
        Story_data = json.load(fh)
    
    Player_data = Story_data['Player']
    
    Player = Obj(Player_data)

    setattr(Player, 'name', input('Enter your name: '))

    Story_data["Player"]["Attributes"]["name"] = Player.name
    save(Story_data)
    with open(save_file, 'w') as fh:
        json.dump(Story_data, fh, indent=4, sort_keys=True)

parser.add_argument('-p', '--position', default=Player.position,
    help="specify starting room (DEBUG USE ONLY)")

print()
print("=-=-=-=-=-=-=-=-=-=")
for attr in Player.__dict__:
    print(f"{attr} '{getattr(Player, attr)}'")
print("=-=-=-=-=-=-=-=-=-=")

if Player.name.lower() == "admin":
    print()
    print("=-= Game Master Active =-=")
    print()
    Enter_Room(Story_data, str(input("Starting Room :")))    

# from char_create import Character_Creation
# print(Character_Creation(Obj(Player_data)))

Enter_Room(Story_data, Player.position)
