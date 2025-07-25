import os
import json
import xml
import shutil
from datetime import date



import unit_modules as units
import helper as helper

today = date.today()

# MAIN
if __name__ == "__main__":

    # --------------------------------------------------------------------------- #
    # Open and load the Json Configuration File
    # --------------------------------------------------------------------------- #
    f = open('machineconfig.json')
    configData = json.load(f)

    # clear all exisiting content in generated folder
    shutil.rmtree('generated')
    if not os.path.exists('generated'):
        os.makedirs('generated')

    configString    = ""
    visuString      = ""

    # --------------------------------------------------------------------------- #
    # Create GVLs
    # --------------------------------------------------------------------------- #
    for i in range(0, len(configData["machine_config"]["modules"])):
        module       = configData["machine_config"]["modules"][i]

        configString += helper.createCommentHeader(module["name"])

        configString += helper.createDeklarationName('    ut',module["name"]) + " : " + helper.createModuleName('ST_CONF',module["name"]) + " := ("
        visuString   += helper.createDeklarationName('ut',module["name"]) + " : " + helper.createModuleName('ST_VIS',module["name"]) + ";\n" 



        for j in range(0, len(module["units"])):
            unit = module["units"][j]

            if j > 0: configString += ","

            if unit["type"] in units.unitTypeMapper:
                unittype = units.unitTypeMapper[unit["type"]]
                concreteUnit = unittype(unit["name"])
                configString += concreteUnit.getConfig()
            else:
                concreteUnit = units.unit(unit["name"])
                configString += concreteUnit.getInstanceCall()


        configString += "); \n"

    configfile = open("generated\gvl_config.txt", "x")
    configfile.write(configString)    
    visufile = open("generated\gvl_visu.txt", "x")
    visufile.write(visuString)


    # --------------------------------------------------------------------------- #
    # Create POUs
    # --------------------------------------------------------------------------- #
    for i in range(0, len(configData["machine_config"]["modules"])):
        module       = configData["machine_config"]["modules"][i]
        modulePath   = f"""generated\{module["name"]}"""

        if not os.path.exists(modulePath):
            os.makedirs(modulePath)
        # ------------
        # Declaration 
        # ------------   
        if  module["is_sqc"] == True:
            pouString = helper.createPouHeader("FB_SQC", module["name"], today)
        else:
            pouString = helper.createPouHeader("FB", module["name"], today)
        # Var_In_Out Area
        pouString += f"""
    VAR_IN_OUT
        //NAME              TYPE                INIT                                COMMENT
        utVisItf : {helper.createModuleName('ST_VIS', module["name"])};
    END_VAR\n"""
        # Var Area
        pouString += f"""
    VAR
        //NAME              TYPE                INIT                                COMMENT
        // locals 
    """
        if module["is_sqc"] == True: 
            pouString += """
        // sequence handler
    """
            for sqc in module["sqc"]:
                pouString += helper.createDeklarationName("      _oSqc", sqc["name"]) + " : FB_SQC_HANDLER;    //" + sqc["comment"] + "\n"

        pouString += "\n     // units\n"

        for unit in module["units"]:
            pouString += helper.createDeklarationName("      _o", unit["name"]) + " : " + unit["type"] + "   //\n"

        pouString += """\nEND_VAR
        ///////////Ab hier kommt der Programm teil\n\n"""
        # ------------
        # Programm Part 
        # ------------  
        pouString += helper.POU_FRAME_START

        for unit in module["units"]:
            if unit["type"] in units.unitTypeMapper:
                unittype = units.unitTypeMapper[unit["type"]]
                concreteUnit = unittype(unit["name"])
                pouString += concreteUnit.getInstanceCall()
            else:
                concreteUnit = units.unit(unit["name"])
                pouString += concreteUnit.getInstanceCall()


        pouString += helper.POU_FRAME_END

        modulfile = open(modulePath+"\POUs.txt", "x")
        modulfile.write(pouString)

    # --------------------------------------------------------------------------- #
    # Create DUTs
    # --------------------------------------------------------------------------- #
    for i in range(0, len(configData["machine_config"]["modules"])):
        module       = configData["machine_config"]["modules"][i]
        modulePath   = f"""generated\{module["name"]}"""

        if not os.path.exists(modulePath):
            os.makedirs(modulePath)

        # ------------
        # Create ST_CONFIG
        # ------------  
        dutString = f"""
        // FIRST THE CONFIG STRUCTs
    TYPE {helper.createModuleName("ST_CONF", module["name"])} :
    STRUCT
        //NAME              TYPE                INIT                                COMMENT
        sName               : STRING(10);
    """
        for unit in module["units"]:
            dutString += helper.createDeklarationName("      ut", unit["name"]) + "  : ST_CONF_" + unit["type"][3:] + ";\n"

        dutString += """
    END_STRUCT
    END_TYPE"""
        # ------------
        # Create ST_VIS
        # ------------  
        dutString += f"""
        // THEN THE VIS STRUCTs
    TYPE {helper.createModuleName("ST_VIS", module["name"])} :
    STRUCT
        //NAME              TYPE                INIT                                COMMENT
    """
        for unit in module["units"]:
            dutString += helper.createDeklarationName("      ut", unit["name"]) + "  : ST_VIS_" + unit["type"][3:] + ";\n"

        dutString += """
    END_STRUCT
    END_TYPE"""
        # ------------
        # Create SQC ENUMs
        # ------------  
        if module["is_sqc"] == True: 
            dutString += "// THEN THE ENUMS\n"
            for sqc in module["sqc"]:
                dutString += f"""TYPE {helper.createModuleName("EN", module["name"])}_{sqc["name"].upper()}_STATE :\n(\n"""

                for step in sqc["steps"]:
                    dutString += f"""{step["name"].upper()},     // {step["comment"]}\n"""

                dutString += ");\nEND_TYPE\n\n "

        modulfile = open(modulePath+"\DUTs.txt", "x")
        modulfile.write(dutString)

    # --------------------------------------------------------------------------- #
    # Create SQCs Methods
    # --------------------------------------------------------------------------- #
    for i in range(0, len(configData["machine_config"]["modules"])):
        module       = configData["machine_config"]["modules"][i]
        modulePath   = f"""generated\{module["name"]}"""

        if not os.path.exists(modulePath):
            os.makedirs(modulePath)
        methodString = ""

        if module["is_sqc"] == True: 
            for sqc in module["sqc"]:
                sqcHanlderName = helper.createDeklarationName("_oSqc", sqc["name"])
                methodString += f"""// NEUE SCHRITTKETTE +++++++++++
    CASE {sqcHanlderName} OF
                """
                for step in sqc["steps"]:
                    enumName = f"""{helper.createModuleName("EN", module["name"])}_{sqc["name"].upper()}_STATE"""
                    methodString += f"""   {helper.createStepInSqc(enumName, step["name"].upper(), step["comment"], sqcHanlderName)}
                    """
                methodString += "END_CASE\n\n"

        modulfile = open(modulePath+"\Methods.txt", "x")
        modulfile.write(methodString)



