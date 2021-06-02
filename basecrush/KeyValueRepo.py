import configparser
from basecrush.ux import MsgUser


              
class KeyValueRepo:

    def __init__(self,path,rebuild,voi,recrush,fixmissing,maxcores,disable_log,pipeline):        

        config = configparser.ConfigParser() 
        config.read(os.path.join(os.path.dirname(__file__), 'crush.ini'))    
        

    if config['CORE']['repository'] =='postgres':
            if self.dbtest()==False:
                MsgUser.failed("Database not setup, exiting" )
                exit()
