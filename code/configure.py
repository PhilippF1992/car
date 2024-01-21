from configparser import ConfigParser

def configure_mqtt():
    print('These questions will configure the configure the connection to the mqtt server:')
    config_object['mqtt'] = {}
    u_input=input('MQTT host (Default: 199.22.2.1):\n')
    if u_input=='':
        print('Using default host: 199.22.2.1')
        u_input='199.22.2.1'
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
    print('These questions will configure the relays:')
    config_object['relays']={}
    number_gpio_inputs=int(input('How many relays did you connect?:\n'))
    for i in range(0, number_gpio_inputs):
        u_input=input(f"Name the {i+1}. relay:\n")
        config_object['relays'][f"relay_{i+1}"]=u_input
    print('Relays are configured!')

def configure_gpio_inputs():
    print('These questions will configure the GPIO inputs:')
    config_object['gpio_inputs']={}
    number_gpio_inputs=int(input('How many gpio_inputs did you connect?:\n'))
    for i in range(0, number_gpio_inputs):
        u_input=input(f"Name the {i+1}. gpio input:\n")
        config_object['gpio_inputs'][f"gpio_input_{i+1}"]=u_input
    print('GPIO inputs are configured!')

def configure_dimmers():
    print('These questions will configure the dimmers:')
    config_object['dimmers']={}
    number_gpio_inputs=int(input('How many dimmers did you connect?:\n'))
    for i in range(0, number_gpio_inputs):
        u_input=input(f"Name the {i+1}. dimmer:\n")
        config_object['dimmers'][f"dimmer_{i+1}"]=u_input
    print('dimmers are configured!')

def configure_ds18b20s():
    print('These questions will configure the ds18b20:')
    config_object['ds18b20s']={}
    number_gpio_inputs=int(input('How many ds18b20s did you connect?:\n'))
    for i in range(0, number_gpio_inputs):
        u_input=input(f"Name the {i+1}. ds18b20:\n")
        config_object['ds18b20s'][f"ds18b20_{i+1}"]=u_input
    print('ds18b20s are configured!')

def configure_all():
    configure_mqtt()
    configure_relays()
    configure_gpio_inputs()
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
        u_input=input('Which config do you want to rework? (all, mqtt, relays, gpio_inputs, dimmers, ds18b20s)\n')
        if u_input == 'all':
            configure_all()
            break
        if u_input == 'mqtt':
            configure_mqtt()
        if u_input == 'relays':
            configure_relays()
        if u_input == 'gpio_inputs':
            configure_gpio_inputs()
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
with open('config/config.ini', 'w') as conf:
    config_object.write(conf)