#!/usr/bin/env python3

# From ChatGPT
from gpiozero import Button

# Check if Button class is as expected
print(Button.__init__.__code__.co_varnames)
print(Button.__init__.__code__.co_argcount)
