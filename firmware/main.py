"""cprisef interface board firmware (micropython on a raspberry pi pico).

design submission status: written for the board in pcb/, not yet run on hardware.

what it does
  reads the load cell through the hx711 on the board, finds each compression as a force peak,
  measures the compression rate, sounds the buzzer when the rate leaves the target window or the
  emergency stop is pressed, and sends one json line per second to the raspberry pi over uart0.

pins (match pcb/kicad/cprisef.kicad_sch)
  gp0 uart tx, gp1 uart rx, gp26 hx711 sck, gp27 hx711 dt,
  gp22 emergency stop input (low means stopped), gp18 buzzer, gp14 status led
"""
import json
import time

from machine import UART, Pin

TARGET_MIN, TARGET_MAX = 100, 120      # compressions per minute (aha window)
PEAK_FORCE = 200.0                     # newtons that count as a compression (tune after calibration)
COUNTS_PER_NEWTON = 1000.0             # hx711 counts per newton, set during calibration

dt = Pin(27, Pin.IN)
sck = Pin(26, Pin.OUT, value=0)
estop = Pin(22, Pin.IN, Pin.PULL_UP)
buzzer = Pin(18, Pin.OUT, value=0)
led = Pin(14, Pin.OUT, value=0)
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))


def read_hx711():
    """one 24 bit reading at gain 128, or None if the chip is not ready."""
    if dt.value():
        return None
    value = 0
    for _ in range(24):
        sck.value(1)
        value = (value << 1) | dt.value()
        sck.value(0)
    sck.value(1)          # one extra pulse selects channel a, gain 128
    sck.value(0)
    if value & 0x800000:
        value -= 1 << 24
    return value


def tare(samples=20):
    total, n = 0, 0
    while n < samples:
        v = read_hx711()
        if v is not None:
            total += v
            n += 1
    return total / n


def beep(ms):
    buzzer.value(1)
    time.sleep_ms(ms)
    buzzer.value(0)


def main():
    offset = tare()
    peaks = []                          # timestamps (ms) of recent compressions
    above = False
    last_report = time.ticks_ms()
    while True:
        raw = read_hx711()
        now = time.ticks_ms()
        if raw is not None:
            force = (raw - offset) / COUNTS_PER_NEWTON
            if force > PEAK_FORCE and not above:
                above = True
                peaks.append(now)
                led.value(1)
            elif force < PEAK_FORCE * 0.5 and above:
                above = False
                led.value(0)
            peaks = [t for t in peaks if time.ticks_diff(now, t) < 15000]
        stopped = estop.value() == 0
        if time.ticks_diff(now, last_report) >= 1000:
            last_report = now
            rate = 0.0
            if len(peaks) >= 2:
                span = time.ticks_diff(peaks[-1], peaks[0]) / 1000.0
                rate = (len(peaks) - 1) * 60.0 / span if span > 0 else 0.0
            in_range = TARGET_MIN <= rate <= TARGET_MAX
            uart.write(json.dumps({"rate": round(rate, 1), "in_range": in_range,
                                   "estop": stopped}) + "\n")
            if stopped:
                beep(500)
            elif peaks and not in_range:
                beep(80)


main()
