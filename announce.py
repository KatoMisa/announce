#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file announce.py
 @brief RTC for clearly conveying the destination to the user
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

from gtts import gTTS
import pygame 
# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
announce_spec = ["implementation_id", "announce", 
         "type_name",         "announce", 
         "description",       "RTC for clearly conveying the destination to the user", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class announce
# @brief RTC for clearly conveying the destination to the user
# 
# 
# </rtc-template>
class announce(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_command_in = OpenRTM_aist.instantiateDataType(RTC.TimedLongSeq)
        """
        """
        self._command_inIn = OpenRTM_aist.InPort("command_in", self._d_command_in)
        self._d_place = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._placeIn = OpenRTM_aist.InPort("place", self._d_place)
        self._d_command_out = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._command_outOut = OpenRTM_aist.OutPort("command_out", self._d_command_out)


		
        self.file = ""

        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("command_in",self._command_inIn)
        self.addInPort("place",self._placeIn)
		
        # Set OutPort buffers
        self.addOutPort("command_out",self._command_outOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	

    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	

    def onDeactivated(self, ec_id):

        return RTC.RTC_OK
	

    def onExecute(self, ec_id):
        try:
            if self._placeIn.isNew():
                place  = self._placeIn.read() 
                self.file = makefile(place.data)
                
            if self._command_inIn.isNew(): 
                command = self._command_inIn.read()                

                speak_result = speak(command.data[0], self.file)
                
                self._d_command_out.data = speak_result
                self._command_outOut.write()
                
        except Exception as e:
            print(e)
        
        
        return RTC.RTC_OK


def speak(state, file_path):
    if state == 1:
        print(state)
        return "ERROR"
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while state == 0:
            time.sleep(0.1)
            if not pygame.mixer.music.get_busy():
                result = "OK"
                return result

    except pygame.error as e:
        print(f"Pygame error occurred: {e}")
        result = "ERROR" 
        return result

    except FileNotFoundError as e:
        print(f"File error: {e}")
        result = "ERROR" 
        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        result = "ERROR" 
        return result

    

def makefile(place):        
    print(place)
    file = '/home/rsdlab/workspace/announce/announce.mp3'
    text='今から' + place + 'へ移動します．ご注意ください'
    tts1 = gTTS(text, lang='ja')
    tts1.save(file)

    return file
	

def announceInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=announce_spec)
    manager.registerFactory(profile,
                            announce,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    announceInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("announce" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

