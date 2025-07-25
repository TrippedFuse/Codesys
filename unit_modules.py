import helper as helper

# for every new class there has to be a entry in the unit type mapper

class unit:
    """ Basic class """
    def __init__(self, name):
        self._name = name

    def getConfig(self):
        confStr = f"""
        {helper.createDeklarationName('ut', self._name)} := 
        (sName           := '{helper.createDisplayName(self._name)}')"""
        return confStr

    def getInstanceCall(self):
        instanceStr = f"""
        {helper.createDeklarationName('_o', self._name)}(
            xEnable                 := xEnable,
		    utConfig				:= utConfig.{helper.createDeklarationName('ut', self._name)},
		    utVisItf				:= utVisItf.{helper.createDeklarationName('ut', self._name)});
            """
        return instanceStr


class FB_DUO_ACTOR(unit):
    def __init__(self, name):
        super().__init__(name)

    def getConfig(self):
        """ generate blank config for duo actor """
        confStr = f"""
                    {helper.createDeklarationName('ut', self._name)} := 
                        (sSensBasPos    := 'B1.0',
                        sSensWrkPos     := 'B1.2', 
                        sActorBasPos    := 'Y1.1', 
                        sActorWrkPos    := 'Y1.2', 
                        sMoveToBasPos   := 'toBas', 
                        sMoveToWrkPos   := 'toWrk', 
                        sName           := '{helper.createDisplayName(self._name)}')"""
        return confStr

    def getInstanceCall(self):
        """ generate the instance call for the duoactor """
        instanceStr = f"""
        {helper.createDeklarationName('_o', self._name)}(
            xEnable                 := xEnable,
            xManual					:= NOT (Command > 0) AND (ExecState = EN_EXEC_STATE.MANUAL), 
		    utConfig				:= utConfig.{helper.createDeklarationName('ut', self._name)}, 
		    xAck					:= xAck, 
		    xSensIsInBasPos			:= , 
		    xSensIsInWrkPos			:= , 
		    xOnManReleaseToBasPos	:= TRUE, 
		    xOnManReleaseToWrkPos	:= TRUE, 
		    xGoToBasPos				=> , 
		    xGoToWrkPos				=> , 
		    utVisItf				:= utVisItf.{helper.createDeklarationName('ut', self._name)});
            """
        return instanceStr

class FB_INPUT(unit):
    def __init__(self, name):
        super().__init__(name)

    def getConfig(self):
        """ generate blank config for inputfb """
        confStr = f"""
                    {helper.createDeklarationName('ut', self._name)} := 
                        (sName           := '{helper.createDisplayName(self._name)}')"""
        return confStr

    def getInstanceCall(self):
        """ generate the instance call for the fbinput """
        instanceStr = f"""
        {helper.createDeklarationName('_o', self._name)}(
            xEnable                 := xEnable,
		    utVisItf				:= utVisItf.{helper.createDeklarationName('ut', self._name)});
            """
        return instanceStr


unitTypeMapper ={
    "FB_DUO_ACTOR":FB_DUO_ACTOR,
    "FB_INPUT":FB_INPUT
}
