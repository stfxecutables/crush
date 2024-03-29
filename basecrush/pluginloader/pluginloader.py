import imp
import os,inspect
from basecrush.ux import MsgUser

PluginFolder = "%s/../../plugins" %(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) 
MainModule = "__init__"

def getPlugins():
    plugins = []        
    for i in os.listdir(PluginFolder):
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])        
        plugins.append({"name": i, "info": info})

    if(len(plugins)==0):
        MsgUser.warning("%s pipeline plugins found.  There should be at least one in the crush/plugins directory" %(len(plugins)))
            
    return plugins

def loadPlugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])