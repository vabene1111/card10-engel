import ujson
import os
import utime
import buttons
import display


def make_timestamp(time):
    """
    Generates a nice timestamp in format hh:mm:ss from the devices localtime
    :return: timestamp
    """
    localtime = utime.localtime(time)
    timestamp = str(utime.localtime(time)[2]) + '.' + str(utime.localtime(time)[1]) + ' '
    if localtime[3] < 10:
        timestamp = timestamp + '0'
    timestamp = timestamp + str(localtime[3]) + ':'
    if localtime[4] < 10:
        timestamp = timestamp + '0'
    timestamp = timestamp + str(localtime[4])
    return timestamp


def loop(shifts):
    shift_index = 0
    last_btn_poll = utime.time() - 2
    while True:
        pressed = buttons.read(
            buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT
        )
        if utime.time() - last_btn_poll >= 1:
            last_btn_poll = utime.time()
            if pressed & buttons.BOTTOM_RIGHT != 0:
                shift_index = shift_index + 1
                if shift_index >= len(shifts):
                    shift_index = 0
            if pressed & buttons.BOTTOM_LEFT != 0:
                shift_index = shift_index - 1
                if shift_index < 0:
                    shift_index = len(shifts) - 1
        with display.open() as disp:
            disp.clear()
            shift = shifts[shift_index]
            disp.print(shift['name'])
            disp.print(shift['Name'], posy=20)
            disp.print(make_timestamp(shift['start']), posy=40)
            disp.print(make_timestamp(shift['end']), posy=60)
            disp.update()
            disp.close()
        utime.sleep(0.5)


f = open('shifts.json', 'r')
shifts_json = ujson.loads(f.read())
f.close()
shifts_json.reverse()
loop(shifts_json)
