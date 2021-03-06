from vegchill.extension import VegChillPlugin, VegChillInitExt
import platform

BANNERS = [
    r'''                                                                                  
                                                                                  
                                       ,----..    ,---,               ,--,    ,--,    
           ,---.                      /   /   \ ,--.' |      ,--,   ,--.'|  ,--.'|    
          /__./|                     |   :     :|  |  :    ,--.'|   |  | :  |  | :    
     ,---.;  ; |            ,----._,..   |  ;. /:  :  :    |  |,    :  : '  :  : '    
    /___/ \  | |   ,---.   /   /  ' /.   ; /--` :  |  |,--.`--'_    |  ' |  |  ' |    
    \   ;  \ ' |  /     \ |   :     |;   | ;    |  :  '   |,' ,'|   '  | |  '  | |    
     \   \  \: | /    /  ||   | .\  .|   : |    |  |   /' :'  | |   |  | :  |  | :    
      ;   \  ' ..    ' / |.   ; ';  |.   | '___ '  :  | | ||  | :   '  : |__'  : |__  
       \   \   ''   ;   /|'   .   . |'   ; : .'||  |  ' | :'  : |__ |  | '.'|  | '.'| 
        \   `  ;'   |  / | `---`-'| |'   | '/  :|  :  :_:,'|  | '.'|;  :    ;  :    ; 
         :   \ ||   :    | .'__/\_: ||   :    / |  | ,'    ;  :    ;|  ,   /|  ,   /  
          '---"  \   \  /  |   :    : \   \ .'  `--''      |  ,   /  ---`-'  ---`-'   
                  `----'    \   \  /   `---`                ---`-'                    
                             `--`-'                                                   

''', r'''
  o              o                              o__ __o     o            o     o    o  
 <|>            <|>                            /v     v\   <|>         _<|>_  <|>  <|> 
 < >            < >                           />       <\  / >                / \  / \ 
  \o            o/  o__  __o     o__ __o/   o/             \o__ __o      o    \o/  \o/ 
   v\          /v  /v      |>   /v     |   <|               |     v\    <|>    |    |  
    <\        />  />      //   />     / \   \\             / \     <\   / \   / \  / \ 
      \o    o/    \o    o/     \      \o/     \         /  \o/     o/   \o/   \o/  \o/ 
       v\  /v      v\  /v __o   o      |       o       o    |     <|     |     |    |  
        <\/>        <\/> __/>   <\__  < >      <\__ __/>   / \    / \   / \   / \  / \ 
                                       |                                               
                               o__     o                                               
                               <\__ __/>                                               

''', r'''
 _     _____ _____ ____  _     _  _     _    
/ \ |\/  __//  __//   _\/ \ /|/ \/ \   / \   
| | //|  \  | |  _|  /  | |_||| || |   | |   
| \// |  /_ | |_//|  \__| | ||| || |_/\| |_/\
\__/  \____\\____\\____/\_/ \|\_/\____/\____/
                                             
''', r'''
 /$$    /$$                     /$$$$$$  /$$       /$$ /$$ /$$
| $$   | $$                    /$$__  $$| $$      |__/| $$| $$
| $$   | $$ /$$$$$$   /$$$$$$ | $$  \__/| $$$$$$$  /$$| $$| $$
|  $$ / $$//$$__  $$ /$$__  $$| $$      | $$__  $$| $$| $$| $$
 \  $$ $$/| $$$$$$$$| $$  \ $$| $$      | $$  \ $$| $$| $$| $$
  \  $$$/ | $$_____/| $$  | $$| $$    $$| $$  | $$| $$| $$| $$
   \  $/  |  $$$$$$$|  $$$$$$$|  $$$$$$/| $$  | $$| $$| $$| $$
    \_/    \_______/ \____  $$ \______/ |__/  |__/|__/|__/|__/
                     /$$  \ $$                                
                    |  $$$$$$/                                
                     \______/                                 
''', r'''
 _  _  ____  ___   ___  _   _  ____  __    __   
( \/ )( ___)/ __) / __)( )_( )(_  _)(  )  (  )  
 \  /  )__)( (_-.( (__  ) _ (  _)(_  )(__  )(__ 
  \/  (____)\___/ \___)(_) (_)(____)(____)(____)
''', r'''
 __      __         _____ _     _ _ _ 
 \ \    / /        / ____| |   (_) | |
  \ \  / /__  __ _| |    | |__  _| | |
   \ \/ / _ \/ _` | |    | '_ \| | | |
    \  /  __/ (_| | |____| | | | | | |
     \/ \___|\__, |\_____|_| |_|_|_|_|
              __/ |                   
             |___/                    
''', r"""
                                                  _..._                              
                                               .-'_..._''.                .---..---. 
 .----.     .----.   __.....__               .' .'      '.\  .        .--.|   ||   | 
  \    \   /    /.-''         '.     .--./) / .'           .'|        |__||   ||   | 
   '   '. /'   //     .-''"'-.  `.  /.''\\ . '            <  |        .--.|   ||   | 
   |    |'    //     /________\   \| |  | || |             | |        |  ||   ||   | 
   |    ||    ||                  | \`-' / | |             | | .'''-. |  ||   ||   | 
   '.   `'   .'\    .-------------' /("'`  . '             | |/.'''. \|  ||   ||   | 
    \        /  \    '-.____...---. \ '---. \ '.          .|  /    | ||  ||   ||   | 
     \      /    `.             .'   /'""'.\ '. `._____.-'/| |     | ||__||   ||   | 
      '----'       `''-...... -'    ||     ||  `-.______ / | |     | |    '---''---' 
                                    \'. __//            `  | '.    | '.              
                                     `'---'                '---'   '---'             
"""
]


class EightColorInitExt(VegChillInitExt):

    COLOR_TABLE = {
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b36m',
        'reset': '\x1b[0m',
    }

    def colorize(self, color, content):
        return COLOR_TABLE[color] + content + COLOR_TABLE['reset']

    def red(self, content):
        return self.colorize('red', content)

    def green(self, content):
        return self.colorize('green', content)

    def yellow(self, content):
        return self.colorize('yellow', content)

    def blue(self, content):
        return self.colorize('blue', content)

    def magenta(self, content):
        return self.colorize('magenta', content)

    def cyan(self, content):
        return self.colorize('cyan', content)

    @classmethod
    def name(self):
        return 'eight_color'


class DefaultThemeInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.util:util']

    def __init__(self):
        util = self.vegchill.init_exts['vegchill.plugins.util:util']
        prompt_text = 'veg> '
        self.show_banner()
        if platform.system() != 'windows':
            prompt = '\001\033[1;32m\002{0:s}\001\033[0m\002'.format(prompt_text)
            # TODO FIXME fix this when lldb can handle this correctly
            if self.vegchill.environ['debugger'] == 'gdb':
                util.set_prompt(prompt)
            else:
                util.set_prompt(prompt_text)
        else:
            util.set_prompt(prompt_text)

    @staticmethod
    def show_banner():
        import random
        print(random.choice(BANNERS))

    @classmethod
    def name(cls):
        return 'default_theme_init'


class Plugin(VegChillPlugin):
    @classmethod
    def init_ext(cls):
        return [DefaultThemeInitExt]

    @classmethod
    def cmd_ext(cls):
        return []
