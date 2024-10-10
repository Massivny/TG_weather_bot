class Lexicon_cmd_main_menu: 
    Commands = {
    '/start' : 'Start working with bot',
    #'/addlocation': 'Add new location (up to 5 locations)',
    '/locations': 'Manage your locations',
    #'/getforecast': 'Get a daily forecast',
    #'/getfurtherforecast': 'Get a forecast up to 6 days ahead',
    '/help': 'View avaliable command and see credits',
}
    
class Lexicon_info:
    Commands = {
        'start': 'Welcome to the your personal weather station!🌤\n\n'
                 'Here you can immediately get the daily weather forecast for your location ' 
                 'or add <b>up to 5 locations</b> to view\n\n'
                 'Also you can get a weather report up to 6 days ahead, '
                 'and if you ask me how i do it — it\'s just a <a href="https://app.tomorrow.io/home">Magic</a>\n\n'
                 'To manage locations: /locations\n'
                 'Or if you want to see the list of avaliable commands and read about: /help',
        'locations': 'This is a list of your locations',
        'addlocation':  'If You want to share your location use button <b>Share location</b>\n\n'
                        'Either way еnter coordinates in WGS-84 longitude-latitude format without using minute and second designations.\n\n'
                        'The coordinates are written in common fractions, e.g. 15.625348, 60.729910',
        'help': 'Hello again! Personal weatherman at your service!\n\n'
                f'Here are the list of avaliable commands:\n'
                +''.join(f'{cmd} - {desc}\n' for cmd, desc in Lexicon_cmd_main_menu.Commands.items())+
                '\nAnd be careful! You never know when it\'s gonna rain <b>freakadillos</b>.',
        'outofloc': 'Sorry, but you can\'t have more than 5 locations😞\n\n'
                    'Do you want to edit the list of your locations?',
        'edit_locations': 'Chose locations you want to delete',
        'no_locations': 'You don\'t have any locations yet.\n\n'
                        'To add new location send /addlocation '
    }

class Lexicon_but:
    Commands = {
        'addlocation_but': '➕Add',
        'edit_locations_but': '❌ Edit',
        'cancel_but': 'Cancel',
        'back_but': 'Back',
        'del_but': '❌',
    }
    
@staticmethod
def get_cmd(command: str) -> str:
    return Lexicon_cmd_main_menu.Commands.get(command, 'Unknown_command')