#!/usr/bin/env python
"""
Attach to a MIDI device and send the contents of a MIDI file to it.
"""
import sys
import time
import midi
import midi.sequencer as sequencer

if len(sys.argv) != 3:
    print "Usage: {0} <client> <port>".format(sys.argv[0])
    exit(2)

client   = sys.argv[1]
port     = sys.argv[2]

hardware = sequencer.SequencerHardware()

if not client.isdigit:
    client = hardware.get_client(client)

if not port.isdigit:
    port = hardware.get_port(port)    

seq = sequencer.SequencerWrite(sequencer_resolution=120)
seq.subscribe_port(client, port)

events = []
e = midi.ControlChangeEvent()
e.control = 0x7B
e.value = 0
events.append(e)

seq.start_sequencer()
for event in events:
    buf = seq.event_write(event, False, False, True)
    if buf == None:
        continue
    if buf < 1000:
        time.sleep(.5)

print 'All notes should be off?'
