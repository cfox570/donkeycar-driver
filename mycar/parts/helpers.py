# Helper parts from complete.py

import donkeycar as dk

'''
    AIPilot: 
        class:  AI_Pilot
        module: parts.helpers
        enable: True
        args: 
            cfg:    cfg
        inputs:  [cam/image_array] 
        outputs: [pilot/angle, pilot/throttle]
'''
class AI_Pilot:
    def __init__(self, cfg):   
        self.kl = dk.utils.get_model_by_type(cfg.DEFAULT_MODEL_TYPE, cfg)
        self.kl.load(cfg.MODEL_PATH)

    def run(self,image):
    # Note: Does not handle parameter: other_array in keras.py
        return self.kl.run(image)

    def shutdown(self):
        self.kl.shutdown()

'''
    DriveMode: 
        class:  DriveMode
        module: parts.helpers
        enable: True
        args: 
            cfg:    cfg
        inputs:  [user/mode, user/angle, user/throttle, pilot/angle, pilot/throttle] 
        outputs: [angle, throttle]
'''
class DriveMode:

    def __init__(self, multiplier):
        self.multiplier = multiplier
    
    def run(self, mode, user_angle, user_throttle, pilot_angle, pilot_throttle):
        if mode == 'user':
            return user_angle, user_throttle

        elif mode == 'local_angle':
            return pilot_angle if pilot_angle else 0.0, user_throttle

        else:
                return pilot_angle if pilot_angle else 0.0, \
                       pilot_throttle * self.multiplier \
                           if pilot_throttle else 0.0

    def shutdown(self):
        pass

'''
    PilotCondition:
        module: parts.helpers
        enable: True
        class: PilotCondition
        args: {}
        inputs:  [user/mode] 
        outputs: [run_pilot]

'''

class PilotCondition:
    def __init__(self):
        pass  
        
    def run(self, mode):
        return False if mode == 'user' else True

    def shutdown(self):
        pass


def get_record_alert_color(num_records, color_array):
    col = (0, 0, 0)
    for count, color in color_array:
        if num_records >= count:
            col = color
    return col


'''
    Tracker:
        class:          RecordTracker
        module:         parts.helpers
        enable:         True
        args:     
            cfg:        cfg
        inputs:         [tub/num_records]
        outputs:        [records/alert]
        run_condition:  recording

'''

class RecordTracker:
    def __init__(self,cfg):
        self.last_num_rec_print = 0
        self.dur_alert = 0
        self.force_alert = 0
        self.REC_COUNT_ALERT = cfg.REC_COUNT_ALERT
        self.REC_COUNT_ALERT_CYC = cfg.REC_COUNT_ALERT_CYC
        self.color_arr = cfg.RECORD_ALERT_COLOR_ARR

    def run(self, num_records):
        if num_records is None:
            return 0

        if self.last_num_rec_print != num_records or self.force_alert:
            self.last_num_rec_print = num_records

            if num_records % 10 == 0:
                print("recorded", num_records, "records")

            if num_records % self.REC_COUNT_ALERT == 0 or self.force_alert:
                self.dur_alert = num_records // self.REC_COUNT_ALERT * self.REC_COUNT_ALERT_CYC
                self.force_alert = 0

        if self.dur_alert > 0:
            self.dur_alert -= 1

        if self.dur_alert != 0:
            return get_record_alert_color(num_records, self.color_arr)

        return 0

# PulseController is the new version of PWM 
from donkeycar.parts.actuator import PWMSteering, PWMThrottle, PulseController
from donkeycar.parts import pins

'''
    PWMDriveTrain_Steering:
        class:      SteeringDriveTrain
        module:     parts.helpers
        enable:     True
        args:
            pin:        PCA9685.1:40.1
            scale:      1.0
            inverted:   False
            left_p:     410
            right_p:    290
        inputs:     [angle] 
        outputs:    []
        threaded:   True

'''
class SteeringDriveTrain(PWMSteering):
    def __init__(self, pin, scale, inverted, left_p, right_p):
        super().__init__(PulseController(
                            pwm_pin=pins.pwm_pin_by_id(pin),
                            pwm_scale=scale,
                            pwm_inverted=inverted),
                        left_pulse=left_p,
                        right_pulse=right_p)

'''
    PWMDriveTrain_Throttle:
        class:      ThrottleDriveTrain
        module:     parts.helpers
        enable:     True
        args:
            pin:        PCA9685.1:40.0
            scale:      1.0
            inverted:   False
            max_p:      420
            zero_p:     370
            min_p:      300
        inputs:     [throttle] 
        outputs:    []
        threaded:   True

'''
class ThrottleDriveTrain(PWMThrottle):
    def __init__(self, pin, scale, inverted, max_p, zero_p, min_p):
        super().__init__(PulseController(
                            pwm_pin=pins.pwm_pin_by_id(pin),
                            pwm_scale=scale,
                            pwm_inverted=inverted),
                        max_pulse=max_p,
                        zero_pulse=zero_p,
                        min_pulse=min_p)

# Alternate implementation supporting parameters in config.py
'''
   PWMDriveTrain_Steering:
       class:      SteeringDriveTrain
       module:     parts.helpers
       enable:     True
       args:
         setting:    cfg.PWM_STEERING_THROTTLE          
         pin:        PWM_STEERING_PIN
         scale:      PWM_STEERING_SCALE
         inverted:   PWM_STEERING_INVERTED
         left_p:     STEERING_LEFT_PWM
         right_p:    STEERING_RIGHT_PWM
       inputs:     [angle] 
       outputs:    []
       threaded:   True
'''
# class SteeringDriveTrain(PWMSteering):
#     def __init__(self, setting, pin, scale, inverted, left_p, right_p):
#         super().__init__(PulseController(
#                             pwm_pin=pins.pwm_pin_by_id(setting[pin]),
#                             pwm_scale=setting[scale],
#                             pwm_inverted=setting[inverted]),
#                         left_pulse=setting[left_p],
#                         right_pulse=setting[right_p])
#   

'''
   PWMDriveTrain_Throttle:
       class:      ThrottleDriveTrain
       module:     parts.helpers
       enable:     True
       args:
         setting:    cfg.PWM_STEERING_THROTTLE          
         pin:        PWM_THROTTLE_PIN
         scale:      PWM_THROTTLE_SCALE
         inverted:   PWM_THROTTLE_INVERTED
         max_p:    THROTTLE_FORWARD_PWM
         zero_p:   THROTTLE_STOPPED_PWM
         min_p:    THROTTLE_REVERSE_PWM
       inputs:     [throttle] 
       outputs:    []
       threaded:   True
'''

# class ThrottleDriveTrain(PWMThrottle):
#     def __init__(self, setting, pin, scale, inverted, max_p, zero_p, min_p):
#         super().__init__(PulseController(
#                             pwm_pin=pins.pwm_pin_by_id(setting[pin]),
#                             pwm_scale=setting[scale],
#                             pwm_inverted=setting[inverted]),
#                         max_pulse=setting[max_p],
#                         zero_pulse=setting[zero_p],
#                         min_pulse=setting[min_p])

