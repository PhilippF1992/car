from configparser import ConfigParser

def configure_mqtt():
    print('These questions will configure the configure the connection to the mqtt server:')
    config_object['mqtt'] = {}
    u_input=input('MQTT host (Default: 192.168.8.113):\n')
    if u_input=='':
        print('Using default host: 192.168.8.113')
        u_input='192.168.8.113'
    config_object['mqtt']['host']=u_input
    u_input=input('MQTT port (Default: 1883):\n')
    if u_input=='':
        print('Using default port: 1883')
        u_input='1883'
    config_object['mqtt']['port']=u_input
    u_input=input('MQTT user (Default: hass):\n')
    if u_input=='':
        print('Using default user: hass')
        u_input='hass'
    config_object['mqtt']['user']=u_input
    u_input=input('MQTT password:\n')
    config_object['mqtt']['password']=u_input
    print('MQTT connection configured!\n')
    

def configure_mcp27013():
    print('These questions will configure the MCP27013 modules:')
    for key in list(config_object.keys()):
        if key.startswith('mcp27013'):
            del config_object[key]
    config_object['mcp27013']={}
    number_of_modules=int(input('How many MCP27013 modules did you connect?\n'))
    config_object['mcp27013']['number_of_modules'] = str(number_of_modules)
    for i in range(0, number_of_modules):
        config_object[f"mcp27013_{i+1}"] = {}
        u_input=input(f"Which address does the {i+1}. MCP27013 module use?\n")
        config_object[f"mcp27013_{i+1}"]['address']=u_input
        u_input=input(f"Which type of module is the {i+1}. MCP27013 module? (relays/inputs)\n")
        config_object[f"mcp27013_{i+1}"]['type']=u_input
        if u_input == 'relays':
            u_input=input(f"On which state does the relay connect? (high/low)\n")
            config_object[f"mcp27013_{i+1}"]['connect_on']=u_input
    print('MCP27013`s are configured!')


def configure_all():
    configure_mqtt()
    configure_mcp27013()

def first_configuration():
    print('No configs found!')
    config_object['base'] = {}
    u_input=input('Name your device please:\n')
    config_object['base']['name']=u_input
    print(f"Welcome to the configuration of '{config_object['base']['name']}'")
    configure_all()

def reconfigure():
    print('Configs found!')
    print(f"Welcome back to the configuration of '{config_object['base']['name']}'")
    while True:
        u_input=input('Which config do you want to rework? (all, mqtt, mcp27013)\n')
        if u_input == 'all':
            configure_all()
            break
        if u_input == 'mqtt':
            configure_mqtt()
        if u_input == 'mcp27013':
            configure_mcp27013()
        u_input = input('Do you want to change more configurations? (Yes/No)\n')
        if u_input == 'No' or u_input == 'n' or u_input == 'no' or u_input == 'N':
            break

#Read config.ini file
config_object = ConfigParser()
config_object.read("config/config.ini")
print('Starting Configurations Setup')
if (config_object.sections()==[]):
    first_configuration()
else:
    reconfigure()
with open('config/config.ini', 'w+') as conf:
    config_object.write(conf)

#TODO ADS1115