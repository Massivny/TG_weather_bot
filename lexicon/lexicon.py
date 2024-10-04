class Lexicon_cmd_main_menu: 
    Commands = {
    '/start' : 'Start working with bot',
    '/addlocation': 'Add new location',
    '/getforecast': 'Get a daily forecast',
    '/getfurtherforecast': 'Get a forecast up to 6 days ahead',
    '/help': 'View avaliable command and see credits',
}
    
class Lexicon_info:
    Commands = {
        'addlocation':  'If You want to share your location use button <b>Share location</b>\n\n'
                        'Either way еnter coordinates in WGS-84 longitude-latitude format without using minute and second designations.\n\n'
                        'The coordinates are written in common fractions, e.g. 15.625348, 60.729910',
        'help': 'Hello again! Personal weatherman at your service!\n\n'
                f'Here are the list of avaliable commands:\n'
                +''.join(f'{cmd} - {desc}\n' for cmd, desc in Lexicon_cmd_main_menu.Commands.items())+
                '\nAnd be careful! You never know when it\'s gonna rain <b>freakadillos</b>.'
                
    }
    
@staticmethod
def get_cmd(command: str) -> str:
    return Lexicon_cmd_main_menu.Commands.get(command, 'Unknown_command')