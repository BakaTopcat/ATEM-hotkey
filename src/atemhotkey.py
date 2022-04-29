import time
import sys
import PyATEMMax
import pyautogui
import keyboard
import configparser

print(f"[{time.ctime()}] ATEM tally to hotkey (c) Kyrylo Ageyev build 1.10.2021")

inifile = "atemhotkey.ini"
# INI file section (read)
config = configparser.ConfigParser()
config.read(inifile)
c_ip = config.get("MAIN", "ip", fallback=1)
c_source = int(config.get("MAIN", "source", fallback=1))
c_me = int(config.get("MAIN", "me", fallback=0))
c_hotkey1 = config.get("MAIN", "hotkey1", fallback="space")
c_hotkey2 = config.get("MAIN", "hotkey2", fallback="")

# ini file likely not found, let's create one
if c_ip == 1:
    c_ip = input(f"[{time.ctime()}] Switcher IP address: ")
    c_source = int(input(f"[{time.ctime()}] Source to monitor: "))
    c_me = int(input(f"[{time.ctime()}] ME program to monitor (0 - ME1, 1 - ME2): "))
    print(f"[{time.ctime()}] Hotkey example: Ctrl+A: hotkey1 = ctrl, hotkey2 = a; Spacebar: hotkey1 = space, hotkey2 is empty")
    c_hotkey1 = input(f"[{time.ctime()}] Hotkey to press part 1: ")
    c_hotkey2 = input(f"[{time.ctime()}] Hotkey to press part 2: ")

    config = configparser.ConfigParser(allow_no_value=True)
    config["MAIN"] = {"# ATEM switcher's IP": None,
                      "ip": c_ip,
                      "\r# Source to monitor: (see text file attached)": None,
                      "source": c_source,
                      "\r# ME program to monitor (0 - ME1, 1 - ME2)": None,
                      "me": c_me,
                      "\r# Hotkey to press:\r# example: Ctrl+A: hotkey1 = ctrl, hotkey2 = a": None,
                      "hotkey1": c_hotkey1,
                      "hotkey2": c_hotkey2}
    with open(inifile, 'w') as configfile:
        config.write(configfile)
    print(f"[{time.ctime()}] New INI file created.")

# Hotkeys: \\t \\n \\r ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ [ \\ ] ^ _ ` a b c d e f g h i j k
# l m n o p q r s t u v w x y z { | } ~ accept add alt altleft altright apps backspace browserback browserfavorites
# browserforward browserhome browserrefresh browsersearch browserstop capslock clear convert ctrl ctrlleft ctrlright
# decimal del delete divide down end enter esc escape execute f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14 f15 f16 f17
# f18 f19 f20 f21 f22 f23 f24 final fn hanguel hangul hanja help home insert junja kana kanji launchapp1 launchapp2
# launchmail launchmediaselect left modechange multiply nexttrack nonconvert num0 num1 num2 num3 num4 num5 num6 num7 num8
# num9 numlock pagedown pageup pause pgdn pgup playpause prevtrack print printscreen prntscrn prtsc prtscr return right
# scrolllock select separator shift shiftleft shiftright sleep space stop subtract tab up volumedown volumemute volumeup
# win winleft winright yen command option optionleft optionright
#
# Video sources:
# 0: Black        1000: Color Bars      3010: MP 1          4010: Key 1 Mask      7001: CLF 1      10010: ME 1 Prg
# 1: Input 1      2001: Color 1         3011: MP 1 Key      4020: Key 2 Mask      7002: CLF 2      10011: ME 1 Pvw
# 2: Input 2      2002: Color 2         3020: MP 2          4030: Key 3 Mask      8001: Aux 1      10020: ME 2 Prg
# ....                                  3021: MP 2 Key      4040: Key 4 Mask      8002: Aux 2      10021: ME 2 Pvw
# 20: Input 20                                              5010: DSK 1 Mask      ....
# 6000: Super Source                                        5020: DSK 2 Mask      8006: Aux 6


# Connect to the switcher
print(f"[{time.ctime()}] Connecting to switcher at {c_ip}")
switcher = PyATEMMax.ATEMMax()
switcher.connect(c_ip)
switcher.waitForConnection(timeout=10)
if not switcher.connected:
    print(f"[{time.ctime()}] Switcher connect fail. Exiting (2).")
    switcher.disconnect()
    input(f"[{time.ctime()}] Press Enter to continue...")
    sys.exit(2)


print(f"[{time.ctime()}] Model: {switcher.atemModel}")
print(f"[{time.ctime()}] Sources: {switcher.topology.sources}")
print(f"[{time.ctime()}] M/Es: {switcher.topology.mEs}")

# Show initial tally state
last_src = switcher.programInput[c_me].videoSource.value
print(f"[{time.ctime()}] Connected, tally {c_source} is [{'ON' if last_src == c_source else 'OFF'}]")

# Loop forever watching for changes
print(f"[{time.ctime()}] Watching for tally changes on videoSource {c_source}")
print(f"[{time.ctime()}] will be emulating hotkey: {c_hotkey1} {c_hotkey2}")
print(f"[{time.ctime()}] Press Q to terminate")

while True:
    # Watch for tally changes
    # src integer type
    src = switcher.programInput[c_me].videoSource.value
    if src != last_src:
        print(f"[{time.ctime()}] programInput.videoSource changed! {src}")
        if src == c_source:
            print(f"[{time.ctime()}] Tally {c_source} [ON]")
            pyautogui.hotkey(c_hotkey1, c_hotkey2)
        elif last_src == c_source:
            print(f"[{time.ctime()}] Tally {c_source} [OFF]")

        last_src = src

    time.sleep(0.04)  # Avoid hogging processor; 1 frame delay

    if keyboard.is_pressed('q'):
        break

switcher.disconnect()
print(f"[{time.ctime()}] Good bye!")
