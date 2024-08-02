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
    
def configure_relays():
    print('These questions will configure the relay modules:')
    config_object['relays']={}
    u_input=input('Did you connect one or more relay modules? (Yes/No)\n')
    if u_input == 'Yes' or u_input == 'Y' or u_input == 'yes' or u_input == 'y':
        number_of_relay_modules=int(input('How many relay modules did you connect?\n'))
        config_object['relays']['number_of_modules'] = str(number_of_relay_modules)
        for i in range(0, number_of_relay_modules):
            u_input=input(f"Which address does the {i+1}. relay module use?\n")
            config_object['relays'][f"relay_module_{i+1}_address"]=u_input
            for j in range(0, 16):
                u_input=input(f"Name the {j+1}. relay of the {i+1}. relay_module:\n")
                config_object['relays'][f"relay_module_{i+1}_relay_{j+1}"]=u_input
    print('Relays are configured!')

def configure_inputs():
    print('These questions will configure the input modules:')
    config_object['inputs']={}
    u_input=input('Did you connect one or more input modules? (Yes/No)\n')
    if u_input == 'Yes' or u_input == 'Y' or u_input == 'yes' or u_input == 'y':
        number_of_input_modules=int(input('How many input modules did you connect?\n'))
        config_object['inputs']['number_of_modules'] = str(number_of_input_modules)
        for i in range(0, number_of_input_modules):
            u_input=input(f"Which address does the {i+1}. input module use?\n")
            config_object['inputs'][f"input_module_{i+1}_address"]=u_input
            for j in range(0, 16):
                u_input=input(f"Name the {j+1}. input of the {i+1}. input_module:\n")
                config_object['relays'][f"input_module_{i+1}_input_{j+1}"]=u_input
    print('GPIO inputs are configured!')

def configure_dimmers():
    print('These questions will configure the dimmers:')
    config_object['dimmers']={}
    number_dimmers=int(input('How many dimmers did you connect?:\n'))
    for i in range(0, number_dimmers):
        u_input=input(f"Name the {i+1}. dimmer:\n")
        config_object['dimmers'][f"dimmer_{i+1}"]=u_input
    print('dimmers are configured!')

def configure_ds18b20s():
    print('These questions will configure the ds18b20 temperature sensors:')
    config_object['ds18b20s']={}
    number_gpio_inputs=int(input('How many ds18b20s did you connect?:\n'))
    for i in range(0, number_gpio_inputs):
        u_input=input(f"Name the {i+1}. ds18b20:\n")
        config_object['ds18b20s'][f"ds18b20_{i+1}"]=u_input
    print('ds18b20s are configured!')

def configure_all():
    configure_mqtt()
    configure_relays()
    configure_inputs()
    configure_dimmers()
    configure_ds18b20s()

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
        u_input=input('Which config do you want to rework? (all, mqtt, relays, inputs, dimmers, ds18b20s)\n')
        if u_input == 'all':
            configure_all()
            break
        if u_input == 'mqtt':
            configure_mqtt()
        if u_input == 'relays':
            configure_relays()
        if u_input == 'inputs':
            configure_inputs()
        if u_input == 'dimmers':
            configure_dimmers()
        if u_input == 'ds18b20s':
            configure_ds18b20s()
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