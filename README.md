# Chronicon Stash Editor

Simple stash editor for Chronicon 

Why am I making this? All the other stash editors have been outdated for years, and the stash is encoded completely differently now.
I wanted to re-create these old projects to the best of my ability and give the community a new tool to play around with. 

Features:
- Change health / damage / mana and other values of items
- Change item IDs
- Duplicate items
- Add multiple runes to one item
- Make runes innate enchantments
- Increase enchantment power past the cap
- And more!


WARNING: I do not take responsibility for any changes made, either intentional or unintentional.
         Make a backup of your stash file before using this tool!


Instructions for Use:
```
  1) Download Repository
  2) Install Required Dependencies (codecs, struct)
  3) Run main.py
  4) Enter File Location of Stash (%localappdata%\Chronicon\save\player.stash)
  5) Wait for stash to load
```

Commands
```
Base:
- list all:                   List all items in stash
- list page [number]:         List items at page number
- list items [start] [end]:   List items between starting and ending indexes
- edit [number]:              Edit item with given index
- write:                      Write stash to file


Items:
- done:                       Go back to Base Commands

- item:                       View item data
- enchants:                   View enchants data
- enchant [integer]:          View detailed information on specific enchantment
- sockets:                    View sockets data
- socket [integer]:           View detailed information on specific socket

- damage [integer]:           Change damage of current item to [integer]
- health [integer]:           Change health of current item to [integer]
- mana [integer]:             Change mana of current item to [integer]
- stamina [integer]:          Change stamina of current item to [integer]
- attackspeed [integer]:      Change attack speed of current item to [integer]
- crit [integer]:             Change critical chance of current item to [integer]
- level [integer]:            Change level of current item to [integer]
- quality [integer]:          Change quality of current item to [integer]
- type [integer]:             Change type of current item to [integer]
- quanity [integer]:          Change quanity of current item to [integer]
- id [integer]:               Change id of current item to [integer]

- enchant [integer] [key] [integer]
- socket [integer] [key] [integer]



Enchants:
Start with "enchant [integer]" to specify which enchant to change.
Between 1 and 10
EX: enchant 5 power 100    -> Change enchantment #5's power to 100

- enchant [integer]:          Change specified enchantment's type to [integer]
- power [integer]:            Change specified enchantment's power to [integer]
- innate [1/0]:               Change whether the specified enchantment is innate or not
- rune [1/0]:                 Change whether the specified enchantment is a rune or not
- locked [1/0]:               Change whether the specified enchantment is locked or not


Sockets:
Start with "socket [integer]" to specify which socket to change.
Between 1 and 6
EX: socket 5 prismatic 1   -> Change socket #5 to be prismatic
                              
- gem [integer]:              Change specified socket's gem to [integer]
- value [integer]:            Change specified socket's value to [integer]
- type [integer]:             Change specified socket's type to [integer]
- prismatic [1/0]:            Change whether the specified enchantment is prismatic or not
```

Make sure to be on the title screen before writing!

Note: There are some bytes in the stash that I have not figured out what they represent. If anyone knows, please let me know.

Directions to Obtain Item IDs (From Chronicon Discord):
```
  Note: Tinka builds are usually Windows-only
  1) Right-click Chronicon in your Steam library and select Properties
  2) Click the BETAS tab, and enter the following code: tinkaistheking
  3) Click CHECK CODE, select "tinkabuilds" from the drop down list, and click CLOSE
  4) Wait for update to finish
  4) Ctrl + p -> Print an item list to file (in appdata location)
```
