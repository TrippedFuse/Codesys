# Project Generation for MD Std

# How To edit Json
## Project information are used for FB Header
'''
  "project_config": {
    "version": "SP21 P1",
    "author": "MD"
  },
'''

## Machine Config 
This is an array of modules (or functiongroups) each module contains a number of units. A module can also be used with an state machine, you can declare it using "is_sqc". 
you can declare various state machines per module and also the steps.
'''
  "machine_config": {
    "modules": [
      { "name" : "module1",
        "comment" : "yes",
        "is_sqc" : true}
        ]}
'''
unit config:
'''
        "units" : [
            {   "type": "FB_DUO_ACTOR",
                "name": "unit1"
            },
            {   "type": "FB_DUO_ACTOR",
                "name": "unit2"
            }
'''
sqc and steps config:
'''
  "sqc" : [
          {   "name" : "Auto",
              "comment" : "Automatik Ablauf",
              "steps" : [
                { "name" : "idle",
                  "comment" : "leerlauf"
                } 
              ]
            },
          {   "name" : "Homing",
              "comment" : "Grundstellungsfahrt",
              "steps" : [
                { "name" : "idle",
                  "comment" : "leerlauf"
                },
'''



# How to Add new Units
it is important to set the unit type mapper for each new unit and also write a implementation
'''
unitTypeMapper ={
    "FB_DUO_ACTOR":FB_DUO_ACTOR,
    "FB_INPUT":FB_INPUT
}
'''
