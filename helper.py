import re


def createModuleName(prefix, moduleName):
    # Regular expression to find all uppercase letters
    pattern = r'([A-Z])'
    # Substitute each uppercase letter with _ followed by the letter
    modified_string = re.sub(pattern, r'_\1', moduleName)
    result = str(prefix).upper() + modified_string.upper()
    return result

def createDisplayName(moduleName):
    # Regular expression to find all uppercase letters
    first_char = moduleName[0]
    pattern = r'([A-Z])'
    # Substitute each uppercase letter with " " followed by the letter
    result = re.sub(pattern, r' \1', moduleName[1:])
    result = (first_char + result).strip()
    return result

def createDeklarationName(prefix, name):
    result = str(prefix) + name
    return result

def createCommentHeader(moduleName):
    modulName = str(moduleName).upper()
    headerString = f"""
//=========================================================
// +++ {moduleName} +++
//=========================================================\n"""
    return headerString

def createPouHeader(pouType, moduleName, date):
    """ possible pou types 
        1 PRG
        2 FB
        3 FC """
    upperModuleName = pouType + "_" + str(moduleName).upper()
    headerString = f"""
// =============================
// Firmware Version:    
// Codesys Version:     
// Release Date:        {date}
// Author:              MDrost 
// Function:              
// =============================
FUNCTION_BLOCK {upperModuleName} EXTENDS FB_UNIT_BASE IMPLEMENTS ITF_UNIT_BASE
VAR_INPUT
    //NAME              TYPE                INIT                                COMMENT
    xAck                : bool;
    {createDeklarationName('ut', moduleName)} : {createModuleName('ST_CONF', moduleName)};
END_VAR\n"""
    return headerString    
    

def createStepInSqc (enumName, stepName, stepComment, sqcHandler):
    stepInSqcStr = f"""
// +++ {stepComment} +++
{enumName}.{stepName}:
// your Code here
    IF FALSE THEN
        {sqcHandler}.nextState({enumName}.);
    END_IF
    """
    return stepInSqcStr

POU_FRAME_START = """
//=========================================================
// +++ INIT +++

//=========================================================

//=========================================================
// +++ FLAGS & TIMER +++

//=========================================================

//=========================================================
// +++ INPUTS +++
	
//=========================================================

//=========================================================
// +++ PROGRAMM +++
	
//=========================================================

//=========================================================
// +++ UNITS  INSTANCES +++
"""

POU_FRAME_END = """
//=========================================================

//=========================================================
// +++ OUTPUTS +++

//=========================================================

//=========================================================
// +++ VISU +++

//=========================================================

//=========================================================
// +++ ALARMS +++

//=========================================================
"""