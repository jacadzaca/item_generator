## About
This repository contains code for a simple item generator for a 3.3.5 [TrinityCore](https://www.trinitycore.org/) server.
It doesn't really create *random* items per se, it just takes an YAML file as input and outputs a DBC and SQL files that
contain *every* possible combination of the attributes specifed in the input file. Then (after patching both the client and the server with the DBC,
and after updating your database with the SQL file), you can write some server-side
script that draws one of the generated items. Bang! You just got yourself a 'random' item generator. As the script outputs
both SQL and DBC files, the items icons are not red question marks.

## Installation
```bash
cd item_generator && python3 -m pip install -r requirements.txt
```

## Example definition file
```yaml
# list of display ids that an item can have
display_ids:
    - 20298
    - 20299

name: Random Staff  # the items' name
first_entry: 56807  # the first new item's entry
template_entry: 873 # the entry of the item that is going to be used as a template, e.g
                    # fields other than entry, display_id and the attributes
                    # will be copied form it. For example, whether the item is an
                    # staff, axe etc.

# the list of attributes that the item is supposed to have,
# for the list of names see below
# min is the minimal value of an attribute an item can have
# max is the maximal value of an attribute an item can have
attributes:
    -
        name: intellect
        min: 10
        max: 11
    -
        name: spirit
        min: 10
        max: 11

```

This definition would create four different items. One with 10 intellect and 10 spirit,
10 intellect and 11 spirit, another with 11 intellect and 10 spirit and lastly one with 11 intellect
and 11 spirit. Each item will be randomly assigned the display_id 20298 or 20299.

## Attribute names
 - mana
 - health
 - agility
 - strength
 - intellect
 - spirit
 - stamina
 - defense skill rating
 - dodge rating
 - parry rating
 - block rating
 - hit melee rating
 - hit ranged rating
 - hit spell rating
 - crit melee rating
 - crit ranged rating
 - crit spell rating
 - hit taken melee rating
 - hit taken ranged rating
 - hit taken spell rating
 - crit taken melee rating
 - crit taken ranged rating
 - crit taken spell rating
 - haste melee rating
 - haste ranged rating
 - haste spell rating
 - hit rating
 - crit rating
 - hit taken rating
 - crit taken rating
 - resilience rating
 - haste rating
 - expertise rating
 - attack power
 - ranged attack power
 - spell healing done
 - spell damage done
 - mana regeneration
 - armor penetration rating
 - spell power
 - health regen
 - spell penetration
 - block

