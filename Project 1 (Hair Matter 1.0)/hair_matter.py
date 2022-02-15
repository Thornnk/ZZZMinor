from random import randint

game_running = True
player_name = ()
yes = ('Yes', 'Y')
no = ('No', 'N')

def function():
    function(sumatory.par)
    function2()

def monster_attack():
    return randint(monster['attack_min'], monster['attack_max'])


while game_running:
    new_game = True
    print('-----' * 10)
    print('Welcome')
    print('-----' * 10)
    player_name = input('Introduce your name:').lower().title()
    print('-----' * 10)
    print('Hello', player_name, '!')

    while new_game:
        player_alive = True
        player_won = False
        player_lost = False
        again = True

        print('Oh! A wild fluffy but evil monster appeared!')
        print('-----' * 10)
#STATS
        player = {'attack': 10, 'heal': 20, 'health': 100}
        monster = {'attack_min': 12, 'attack_max': 20, 'health': 100}
######
        while player_alive:
            player_choice_list = ('1', '2', '3')
            print('What do you want to do?')
            print('1) Attack')
            print('2) Heal')
            print('3) Run away')
            player_choice = input()
            print('-----' * 10)

            if player_choice == '1':
                monster['health'] = monster['health'] - player['attack']
                if monster['health'] <= 0:
                    player_won = True

                else:
                    player['health'] = player['health'] - monster_attack()
                    print(player_name, 'attacked! The fluffy but evil monster is bleeding!', player_name, 'inflicted', player['attack'], 'points of damage.')
                    if player['health'] <= 0:
                        player_lost = True

                    else:
                        print('Holy moly! The fluffy but evil monster attacked back!', player_name, 'received', monster_attack(), 'points of damage.')
                        print('-----' * 10)

            elif player_choice == '2':
                player['health'] = player['health'] + player['heal']
                print(player_name, 'healed himself with bandages, white magic...and stuff.', str(player_name) + '\'s heal power increased his health by', player['heal'], '.')
                player['health'] = player['health'] - monster_attack()
                print('Bloody bastard! The fluffy but evil monster attacked', player_name, 'while he was healing!', player_name, 'received', monster_attack(), 'points of damage.')
                print('-----' * 10)

            elif player_choice == '3':
                player['health'] = player['health'] - monster_attack()
                print('You little coward! Come on! Fight it bravely!')
                print('Oh no! The fluffy but evil monster attacked', player_name, 'while he was deciding!', player_name, 'received', monster_attack(), 'points of damage.')
                if player['health'] <= 0:
                    player_lost = True
                print('-----' * 10)

            else:
                print('Invalid Input. Please enter the options: "1", "2" or "3".')
                print('-----' * 10)

            if player_won is False and player_lost is False and not player_choice not in player_choice_list:
                print(player_name, 'has', player['health'], 'HP left.')
                print('The fluffy but evil monster has', monster['health'], 'HP left.')
                print('-----' * 10)

            if player_won is True:
                print('Congratulations', player_name, '! You killed the fluffy but evil monster and you can finally go back to your couch and have a hot chocolate under a big thick soft blanket.')
                print('YOU WIN!')
                print()

                while again is True:
                    print('Play again?')
                    game_continue = input().lower().title()
                    print('-----' * 10)
                    if game_continue in yes:
                        again = False
                        player_alive = False

                    elif game_continue in no:
                        print('See you later!')
                        print('-----' * 10)
                        again = False
                        player_alive = False
                        new_game = False
                        game_running = False

                    else:
                        print('Invalid input. Please enter "yes" or "no".')

            elif player_lost:
                print('The fluffy but evil monster defeated you and you suffered an awful painful death.')
                print('What a loser!')
                print('GAME OVER')
                print()
                while again:
                    print('Continue?')
                    game_continue = input().lower().title()
                    print('-----' * 10)
                    if game_continue in yes:
                        again = False
                        player_alive = False

                    elif game_continue in no:
                        print('See you later!')
                        print('-----' * 10)
                        again = False
                        player_alive = False
                        new_game = False
                        game_running = False

                    else:
                        print('Invalid input. Please enter "yes" or "no".')
