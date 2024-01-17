#Set jumper to B 
opkg update
opkg install usb-modeswitch kmod-mii kmod-usb-net kmod-usb-wdm kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option qmi-utils libqmi

#setup via ui, new interace QMI cellular + /dev/cdc-wdm0 
#apn internet.t-d1.de
#auth PAP
#user t-mobile
#pw tm
#PDP IPv4/IPv6

#apn internet.v6.telekom
#auth PAP
#user telekom
#pw tm
PDP IPv6

uqmi -d /dev/cdc-wdm0 --start-network --apn internet.t-d1.de --auth-type pap --username t-mobile --password tm --ip-family ipv4
uqmi -d /dev/cdc-wdm0 --start-network --apn internet.telekom --auth-type pap --username telekom --password tm --ip-family ipv4




Usage: uqmi <options|actions>
Options:
  --single, -s:                     Print output as a single line (for scripts)
  --device=NAME, -d NAME:           Set device name to NAME (required)
  --keep-client-id <name>:          Keep Client ID for service <name>
  --release-client-id <name>:       Release Client ID after exiting
  --mbim, -m                        NAME is an MBIM device with EXT_QMUX support
  --timeout, -t                     response timeout in msecs

Services:                           dms, nas, pds, wds, wms

Actions:
  --get-versions:                   Get service versions
  --set-client-id <name>,<id>:      Set Client ID for service <name> to <id>
                                    (implies --keep-client-id)
  --get-client-id <name>:           Connect and get Client ID for service <name>
                                    (implies --keep-client-id)
  --sync:                           Release all Client IDs
  --start-network:                  Start network connection (use with options below)
    --apn <apn>:                    Use APN
    --auth-type pap|chap|both|none: Use network authentication type
    --username <name>:              Use network username
    --password <password>:          Use network password
    --ip-family <family>:           Use ip-family for the connection (ipv4, ipv6, unspecified)
    --autoconnect:                  Enable automatic connect/reconnect
    --profile <index>:              Use connection profile
  --stop-network <pdh>:             Stop network connection (use with option below)
    --autoconnect:                  Disable automatic connect/reconnect
  --get-data-status:                Get current data access status
  --set-ip-family <val>:            Set ip-family (ipv4, ipv6, unspecified)
  --set-autoconnect <val>:          Set automatic connect/reconnect (disabled, enabled, paused)
  --get-current-settings:           Get current connection settings
  --get-capabilities:               List device capabilities
  --get-pin-status:                 Get PIN verification status
  --verify-pin1 <pin>:              Verify PIN1
  --verify-pin2 <pin>:              Verify PIN2
  --set-pin1-protection <state>:    Set PIN1 protection state (disabled, enabled)
    --pin <pin>:                    PIN1 needed to change state
  --set-pin2-protection <state>:    Set PIN2 protection state (disabled, enabled)
    --pin <pin2>:                   PIN2 needed to change state
  --change-pin1:                    Change PIN1
    --pin <old pin>:                Current PIN1
    --new-pin <new pin>:            New pin
  --change-pin2:                    Change PIN2
    --pin <old pin>:                Current PIN2
    --new-pin <new pin>:            New pin
  --unblock-pin1:                   Unblock PIN1
    --puk <puk>:                    PUK needed to unblock
    --new-pin <new pin>:            New pin
  --unblock-pin2:                   Unblock PIN2
    --puk <puk>:                    PUK needed to unblock
    --new-pin <new pin>:            New pin
  --get-iccid:                      Get the ICCID
  --get-imsi:                       Get International Mobile Subscriber ID
  --get-imei:                       Get International Mobile Equipment ID
  --get-msisdn:                     Get the MSISDN (telephone number)
  --reset-dms:                      Reset the DMS service
  --get-device-operating-mode       Get the device operating mode
  --set-device-operating-mode <m>   Set the device operating mode
                                    (modes: online, low_power, factory_test, offline
                                     reset, shutting_down, persistent_low_power,
                                     mode_only_low_power)
  --fcc-auth:                       Set FCC authentication
  --uim-verify-pin1 <pin>:          Verify PIN1 (new devices)
  --uim-verify-pin2 <pin>:          Verify PIN2 (new devices)
  --uim-get-sim-state:                  Get current SIM state
  --set-network-modes <modes>:      Set usable network modes (Syntax: <mode1>[,<mode2>,...])
                                    Available modes: all, lte, umts, gsm, cdma, td-scdma
  --set-network-preference <mode>:  Set preferred network mode to <mode>
                                    Available modes: auto, gsm, wcdma
  --set-network-roaming <mode>:     Set roaming preference:
                                    Available modes: any, off, only
  --network-scan:                   Initiate network scan
  --network-register:               Initiate network register
  --set-plmn:                       Register at specified network
    --mcc <mcc>:                    Mobile Country Code (0 - auto)
    --mnc <mnc>:                    Mobile Network Code
  --get-plmn:                       Get preferred network selection info
  --get-signal-info:                Get signal strength info
  --get-serving-system:             Get serving system info
  --get-system-info:                Get system info
  --get-lte-cphy-ca-info:           Get LTE Cphy CA Info
  --get-cell-location-info:         Get Cell Location Info
  --get-tx-rx-info <radio>:         Get TX/RX Info (gsm, umts, lte)
  --list-messages:                  List SMS messages
    --storage <mem>:                Messages storage (sim (default), me)
  --delete-message <id>:            Delete SMS message at index <id>
    --storage <mem>:                Messages storage (sim (default), me)
  --get-message <id>:               Get SMS message at index <id>
    --storage <mem>:                Messages storage (sim (default), me)
  --get-raw-message <id>:           Get SMS raw message contents at index <id>
    --storage <mem>:                Messages storage (sim (default), me)
  --send-message <data>:            Send SMS message (use options below)
    --send-message-smsc <nr>:       SMSC number
    --send-message-target <nr>:     Destination number (required)
    --send-message-flash:           Send as Flash SMS
  --wda-set-data-format <type>:     Set data format (type: 802.3|raw-ip)
  --wda-get-data-format:            Get data format