#!/usr/bin/env python3

from swagger_client.models.gesture_definition import GestureDefinition

# Emotional Gestures Library, contains:
# 1.  ExpressHappyLow - ExpressHappyMedium - ExpressHappyHigh
# 2.  ExpressAngerLow - ExpressAngerMedium - ExpressAngerHigh
# 3.  ExpressDisgustLow - ExpressDisgustMedium - ExpressDisgustHigh
# 4.  ExpressFearLow - ExpressFearMedium - ExpressFearHigh
# 5.  ExpressSadLow - ExpressSadMedium - ExpressSadHigh
# 6.  SurpriseLow - SurpriseMedium - SurpriseHigh
# 7.  SurprisePositive - SurpriseNegative
# 8.  Thoughtful
# 9.  Doubious
# 10. NodListening
# 12. Awake1 - Awake2 - Awake3


# ----------------------------------------------------------------------------------------------------
# Definition of gestures: ExpressHappyLow - ExpressHappyMedium - ExpressHappyHigh

# Gesture definition: ExpressHappyLow
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressHappyLow)
ExpressHappyLow = GestureDefinition(
    name="ExpressHappyLow",
    frames=[
        {
            # FACS. Happyness: 6+12
            # 6: Cheek raiser
            # 12: Lip corner puller
            "time": [0.32, 1.64],
            "persist": False,
            "params": {
                "SMILE_OPEN": 0.1,
                "SMILE_CLOSED": 1.0,

                # raise eyebrows
                "BROW_UP_LEFT": 0.2,
                "BROW_UP_RIGHT": 0.2,
            }
        },
        {
            "time": [1.96],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressHappyMedium
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressHappyMedium)
ExpressHappyMedium = GestureDefinition(
    name="ExpressHappyMedium",
    frames=[
        {
            # FACS. Happyness: 6+12
            # 6: Cheek raiser
            # 12: Lip corner puller
            "time": [0.32, 1.64],
            "persist": False,
            "params": {
                "SMILE_OPEN": 0.3,
                "SMILE_CLOSED": 0.7,

                # raise eyebrows
                "BROW_UP_LEFT": 0.33,
                "BROW_UP_RIGHT": 0.33,
            }
        },
        {
            "time": [1.96],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressHappyHigh
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressHappyHigh)
ExpressHappyHigh = GestureDefinition(
    name="ExpressHappyHigh",
    frames=[
        {
            # FACS. Happyness: 6+12
            # 6: Cheek raiser
            # 12: Lip corner puller
            "time": [0.32, 1.64],
            "persist": False,
            "params": {
                "PHONE_AAH": 0.3,
                "PHONE_I": 0.2,
                "PHONE_K": 0.1,

                "SMILE_OPEN": 0.6,
                "SMILE_CLOSED": 1.0,

                # raise eyebrows
                "BROW_UP_LEFT": 1.0,
                "BROW_UP_RIGHT": 1.0,
            }
        },
        {
            "time": [1.96],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: ExpressAngerLow - ExpressAngerMedium - ExpressAngerHigh

# Gesture definition: ExpressAngerLow
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressAngerLow)
ExpressAngerLow = GestureDefinition(
    name="ExpressAngerLow",
    frames=[
        {
            # FACS. Anger: 4+5+7+23
            # 4: Brow lowerer
            # 5: Upper lid raiser
            # 7: Lid tightener
            # 23: Lip tightener
            "time": [0.9, 1.5],
            "persist": False,
            "params": {
                # eyebrows
                "BROW_DOWN_LEFT": 1.0,
                "BROW_DOWN_RIGHT": 1.0,
                "BROW_IN_LEFT": 1.0,
                "BROW_IN_RIGHT": 1.0,

                # epicantic fold
                "EPICANTHIC_FOLD": 0.3,

                # squint eyes
                "EYE_SQUINT_LEFT": 0.8,
                "EYE_SQUINT_RIGHT": 0.8,

                # tight mouth
                "PHONE_F_V": 1.0,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressAngerMedium
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressAngerMedium)
ExpressAngerMedium = GestureDefinition(
    name="ExpressAngerMedium",
    frames=[
        {
            # FACS. Anger: 4+5+7+23
            # 4: Brow lowerer
            # 5: Upper lid raiser
            # 7: Lid tightener
            # 23: Lip tightener
            "time": [0.9, 1.5],
            "persist": False,
            "params": {
                "EXPR_ANGER": 0.4,

                # epicantic fold
                "EPICANTHIC_FOLD": 0.1,

                # squint eyes
                "EYE_SQUINT_LEFT": 0.4,
                "EYE_SQUINT_RIGHT": 0.4,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressAngerHigh
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressAngerHigh)
ExpressAngerHigh = GestureDefinition(
    name="ExpressAngerHigh",
    frames=[
        {
            # FACS. Anger: 4+5+7+23
            # 4: Brow lowerer
            # 5: Upper lid raiser
            # 7: Lid tightener
            # 23: Lip tightener
            "time": [0.9, 1.5],
            "persist": False,
            "params": {
                "EXPR_ANGER": 0.8,

                # eyebrows
                "BROW_DOWN_LEFT": 0.8,
                "BROW_DOWN_RIGHT": 0.8,
                "BROW_IN_LEFT": 0.8,
                "BROW_IN_RIGHT": 0.8,

                # epicantic fold
                "EPICANTHIC_FOLD": 0.3,

                # squint eyes
                "EYE_SQUINT_LEFT": 0.3,
                "EYE_SQUINT_RIGHT": 0.3,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: ExpressDisgustLow - ExpressDisgustMedium - ExpressDisgustHigh

# Gesture definition: ExpressDisgustLow
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressDisgustLow)
ExpressDisgustLow = GestureDefinition(
    name="ExpressDisgustLow",
    frames=[
        {
            # FACS. Disgust: 9+15+17
            # 9: Nose wrinkler
            # 15: Lip corner depressor
            # 17: Chin raiser
            "time": [0.64, 1.4],
            "persist": False,
            "params": {
                "EXPR_DISGUST": 0.4,
                "PHONE_F_V": 0.1,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressDisgustMedium
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressDisgustMedium)
ExpressDisgustMedium = GestureDefinition(
    name="ExpressDisgustMedium",
    frames=[
        {
            # FACS. Disgust: 9+15+17
            # 9: Nose wrinkler
            # 15: Lip corner depressor
            # 17: Chin raiser
            "time": [0.64, 1.4],
            "persist": False,
            "params": {
                "EXPR_DISGUST": 0.6,
                "PHONE_F_V": 0.3,
                "NECK_PAN": 4,
            }
        },
        {
            "time": [1.4],
            "persist": False,
            "params": {
                "NECK_PAN": 0.0,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressDisgustHigh
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressDisgustHigh)
ExpressDisgustHigh = GestureDefinition(
    name="ExpressDisgustHigh",
    frames=[
        {
            # FACS. Disgust: 9+15+17
            # 9: Nose wrinkler
            # 15: Lip corner depressor
            # 17: Chin raiser
            "time": [0.64, 1.4],
            "persist": False,
            "params": {
                "EXPR_DISGUST": 1.0,
                "PHONE_F_V": 0.5,
                "NECK_PAN": 8,
                "NECK_TILT": 2,
            }
        },
        {
            "time": [0.8],
            "persist": False,
            "params": {
                "NECK_PAN": 4,
            }
        },
        {
            "time": [1.0],
            "persist": False,
            "params": {
                "NECK_PAN": 8,
            }
        },
        {
            "time": [1.2],
            "persist": False,
            "params": {
                "NECK_PAN": 4,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: ExpressFearLow - ExpressFearMedium - ExpressFearHigh

# Gesture definition: ExpressFearLow
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressFearLow)
ExpressFearLow = GestureDefinition(
    name="ExpressFearLow",
    frames=[
        {
            # FACS. Fear: 1+2+4+5+7+20+26
            # 1: Inner brow raiser
            # 2: Outer brow raiser
            # 4: Brow lowerer
            # 5: Upper lid raiser
            # 7: Lid tightener
            # 20: Lip stretcher
            # 26: Mouth stretch
            "time": [1.0, 1.5],
            "persist": False,
            "params": {
                "EXPR_FEAR": 0.4,
                "PHONE_B_M_P": 0.4,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressFearMedium
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressFearMedium)
ExpressFearMedium = GestureDefinition(
    name="ExpressFearMedium",
    frames=[
        {
            # FACS. Fear: 1+2+4+5+7+20+26
            # 1: Inner brow raiser
            # 2: Outer brow raiser
            # 4: Brow lowerer
            # 5: Upper lid raiser
            # 7: Lid tightener
            # 20: Lip stretcher
            # 26: Mouth stretch
            "time": [1.0, 1.5],
            "persist": False,
            "params": {
                "EXPR_FEAR": 0.6,
                "PHONE_B_M_P": 0.3,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressFearHigh
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressFearHigh)
ExpressFearHigh = GestureDefinition(
    name="ExpressFearHigh",
    frames=[
        {
            # FACS. Fear: 1+2+4+5+7+20+26
            # 1: Inner brow raiser
            # 2: Outer brow raiser
            # 4: Brow lowerer
            # 5: Upper lid raiser
            # 7: Lid tightener
            # 20: Lip stretcher
            # 26: Mouth stretch            
            "time": [1.0, 1.5],
            "persist": False,
            "params": {
                "EXPR_FEAR": 1.0,
                "PHONE_AAH": 0.3,
            }
        },
        {
            "time": [0.3],
            "persist": False,
            "params": {
                "NECK_PAN": 8,
            }
        },
        {
            "time": [0.6],
            "persist": False,
            "params": {
                "NECK_PAN": -8,
            }
        },
        {
            "time": [0.9],
            "persist": False,
            "params": {
                "NECK_PAN": 8,
            }
        },
        {
            "time": [1.2],
            "persist": False,
            "params": {
                "NECK_PAN": -8,
            }
        },
        {
            "time": [1.5],
            "persist": False,
            "params": {
                "NECK_PAN": 0,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: ExpressSadLow - ExpressSadMedium - ExpressSadHigh

# Gesture definition: ExpressSadLow
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressSadLow)
ExpressSadLow = GestureDefinition(
    name="ExpressSadLow",
    frames=[
        {
            # FACS. Sadness: 1+4+15
            # 1: Inner brow raiser
            # 4: Brow lowerer
            # 15: Lip corner depressor
            "time": [1.0, 2.5],
            "persist": False,
            "params": {
                # 1: inner brow raiser
                "BROW_IN_LEFT": 1.0,
                "BROW_IN_RIGHT": 1.0,

                # 4: brow lowerer
                "BROW_DOWN_LEFT": 0.1,
                "BROW_DOWN_RIGHT": 0.1,

                # 15: lip corner depressor
                "PHONE_B_M_P": 0.8,

                # looks slightly lowered
                "LOOK_DOWN": 0.2,

                # epicantic fold
                "EPICANTHIC_FOLD": 0.2,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressSadMedium
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressSadMedium)
ExpressSadMedium = GestureDefinition(
    name="ExpressSadMedium",
    frames=[
        {
            # FACS. Sadness: 1+4+15
            # 1: Inner brow raiser
            # 4: Brow lowerer
            # 15: Lip corner depressor
            "time": [1.0, 2.5],
            "persist": False,
            "params": {
                # 1: inner brow raiser
                "BROW_IN_LEFT": 1.0,
                "BROW_IN_RIGHT": 1.0,

                # 4: brow lowerer
                "BROW_DOWN_LEFT": 0.2,
                "BROW_DOWN_RIGHT": 0.2,

                # 15: lip corner depressor
                "PHONE_B_M_P": 1.0,
                "PHONE_EH": 0.25,

                # looks slightly lowered
                "LOOK_DOWN": 0.2,

                # epicantic fold
                "EPICANTHIC_FOLD": 0.3,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: ExpressSadHigh
# Usage: furhat.gesture(body=emotionGestureDefinition.ExpressSadHigh)
ExpressSadHigh = GestureDefinition(
    name="ExpressSadHigh",
    frames=[
        {
            # FACS. Sadness: 1+4+15
            # 1: Inner brow raiser
            # 4: Brow lowerer
            # 15: Lip corner depressor
            "time": [1.0, 2.5],
            "persist": False,
            "params": {
                # 1: inner brow raiser
                "BROW_IN_LEFT": 1.0,
                "BROW_IN_RIGHT": 1.0,

                # 4: eyebrows
                "BROW_DOWN_LEFT": 0.4,
                "BROW_DOWN_RIGHT": 0.4,

                # 15: lip corner depressor
                "PHONE_B_M_P": 1.0,
                "PHONE_EH": 0.25,

                # looks slightly lowered
                "GAZE_PAN": 20,
                "GAZE_TILT": 8,
                # "LOOK_DOWN": 0.2,

                # epicantic fold
                "EPICANTHIC_FOLD": 0.4,

                # slight lowering of the head
                "NECK_TILT": 12,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: SurpriseLow - SurpriseMedium - SurpriseHigh

# Gesture definition: SurpriseLow
# Usage: furhat.gesture(body=emotionGestureDefinition.SurpriseLow)
SurpriseLow = GestureDefinition(
    name="SurpriseLow",
    frames=[
        {
            # FACS. Surprise: 1+2+5B (B means light) +26
            # 1: Inner brow raiser
            # 2: Outer brow raiser
            # 5B: Upper lid raiser
            # 26: Mouth stretch
            "time": [0.32, 0.64],
            "persist": False,
            "params": {
                "SURPRISE": 0.4,
                "PHONE_OH": 0.1,
            }
        },
        {
            "time": [0.96],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: SurpriseMedium
# Usage: furhat.gesture(body=emotionGestureDefinition.SurpriseMedium)
SurpriseMedium = GestureDefinition(
    name="SurpriseMedium",
    frames=[
        {
            # FACS. Surprise: 1+2+5B (B means light) +26
            # 1: Inner brow raiser
            # 2: Outer brow raise
            # 5B: Upper lid raiser
            # 26: Mouth stretc
            "time": [0.32, 0.64],
            "persist": False,
            "params": {
                "SURPRISE": 0.4,
                "PHONE_OH": 0.3,
            }
        },
        {
            "time": [0.96],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: SurpriseHigh
# Usage: furhat.gesture(body=emotionGestureDefinition.SurpriseHigh)
SurpriseHigh = GestureDefinition(
    name="SurpriseHigh",
    frames=[
        {
            # FACS. Surprise: 1+2+5B (B means light) +26
            # 1: Inner brow raiser
            # 2: Outer brow raiser
            # 5B: Upper lid raiser
            # 26: Mouth stretch
            "time": [0.32, 0.64],
            "persist": False,
            "params": {
                "SURPRISE": 1.0,
                "PHONE_OH": 0.6,
                "PHONE_BIGAAH": 0.01,
            }
        },
        {
            "time": [0.2],
            "persist": False,
            "params": {
                "NECK_TILT": -8,
            }
        },
        {
            "time": [0.6],
            "persist": False,
            "params": {
                "NECK_TILT": 8,
            }
        },
        {
            "time": [1.3],
            "persist": False,
            "params": {
                "NECK_TILT": 0,
            }
        },
        {
            "time": [1.96],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: SurprisePositive - SurpriseNegative

# Gesture definition: SurprisePositive
# Usage: furhat.gesture(body=emotionGestureDefinition.SurprisePositive)
SurprisePositive = GestureDefinition(
    name="SurprisePositive",
    frames=[
        {
            "time": [0.32, 1.64],
            "persist": False,
            "params": {
                "SURPRISE": 1.0,
                "PHONE_OH": 0.2,
            }
        },
        {
            "time": [1.64, 1.64],
            "persist": False,
            "params": {
                "PHONE_OH": 0.25,
                "SMILE_OPEN": 0.2,
                "SMILE_CLOSED": 1.0,
            }
        },
        {
            "time": [2.0, 2.64],
            "persist": False,
            "params": {
                "PHONE_OH": 0.1,
                "SMILE_OPEN": 0.1,
                "SMILE_CLOSED": 1.0,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: SurpriseNegative
# Usage: furhat.gesture(body=emotionGestureDefinition.SurpriseNegative)
SurpriseNegative = GestureDefinition(
    name="SurpriseNegative",
    frames=[
        {
            "time": [0.32, 1.64],
            "persist": False,
            "params": {
                "SURPRISE": 1.0,
                "PHONE_OH": 0.1,
            }
        },
        {
            "time": [1.64, 2.5],
            "persist": False,
            "params": {
                "SURPRISE": 0.0,
                "PHONE_OH": 0.0,
                "EXPR_FEAR": 0.6,
            }
        },
        {
            "time": [3.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Gesture definition: Thoughtful
# Usage: furhat.gesture(body=emotionGestureDefinition.Thoughtful)
Thoughtful = GestureDefinition(
    name="Thoughtful",
    frames=[
        {
            "time": [0.3, 4.0],
            "persist": False,
            "params": {
                # eyebrows and eyes
                "BROW_DOWN_LEFT": 1.0,
                "BROW_DOWN_RIGHT": 1.0,
                "BROW_IN_LEFT": 1.0,
                "BROW_IN_RIGHT": 1.0,
                "EYE_SQUINT_LEFT": 0.7,
                "EYE_SQUINT_RIGHT": 0.4,
            }
        },
        {
            "time": [1.3, 4.0],
            "persist": False,
            "params": {
                # mouth
                "PHONE_B_M_P": 0.8,
                "PHONE_CH_J_SH": 0.3,
                "PHONE_W": 0.5,

                # head
                "NECK_PAN": -6,
                "NECK_ROLL": -8,
                "NECK_TILT": -4
            }
        },
        {
            "time": [2.3, 4.0],
            "persist": False,
            "params": {
                "LOOK_RIGHT": 0.5,
                "LOOK_UP": 0.3,
            }
        },
        {
            "time": [5.6],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Gesture definition: Doubious
# Usage: furhat.gesture(body=emotionGestureDefinition.Doubious)
Doubious = GestureDefinition(
    name="Doubious",
    frames=[
        {
            "time": [0.9, 1.0],
            "persist": False,
            "params": {
                "NECK_ROLL": -10,
                "NECK_TILT": 2,
                "NECK_PAN": -6,
            }
        },
        {
            "time": [2.1],
            "persist": False,
            "params": {
                # head
                "NECK_ROLL": 0,
                "NECK_TILT": 0,
                "NECK_PAN": 0,
            }
        },
        {
            "time": [0.5, 2.0],
            "persist": False,
            "params": {
                # eyebrows
                "BROW_UP_RIGHT": 1.0,
                "BROW_DOWN_LEFT": 1.0,
                "BROW_IN_LEFT": 1.0,
                "BROW_IN_RIGHT": 1.0,

                # eyelids and eyes
                "EPICANTHIC_FOLD": 0.1,
                "EYE_SQUINT_LEFT": 0.4,

                # mouth
                "PHONE_B_M_P": 1.0,
                "PHONE_CH_J_SH": 0.3,
            }
        },
        {
            "time": [3.5],
            "persist": False,
            "params": {
                "GAZE_TILT": 20,
                "LOOK_DOWN": 0.1,
            }
        },
        {
            "time": [4.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Definition of gestures: Awake1 - Awake2 - Awake3

# Gesture definition: Awake1
# Usage: furhat.gesture(body=emotionGestureDefinition.Awake1)
Awake1 = GestureDefinition(
    name="Awake1",
    frames=[
        {
            "time": [0.8, 1.0],
            "persist": False,
            "params": {
                "NECK_PAN": -15,
                "LOOK_RIGHT": 0.4,
                "LOOK_UP": 0.2,
            }
        },
        {
            "time": [1.8],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: Awake2
# Usage: furhat.gesture(body=emotionGestureDefinition.Awake2)
Awake2 = GestureDefinition(
    name="Awake2",
    frames=[
        {
            "time": [0.2, 0.6],
            "persist": False,
            "params": {
                "EYE_SQUINT_LEFT": 0.4,
                "NECK_ROLL": -15
            }
        },
        {
            "time": [0.8],
            "persist": False,
            "params": {
                "reset": True
            }
        },
        {
            "time": [1.2, 1.6],
            "persist": False,
            "params": {
                "NECK_ROLL": 15
            }
        },
        {
            "time": [1.8],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# Gesture definition: Awake3
# Usage: furhat.gesture(body=emotionGestureDefinition.Awake3)
Awake3 = GestureDefinition(
    name="Awake3",
    frames=[
        {
            "time": [0.8, 1.0],
            "persist": False,
            "params": {
                "NECK_PAN": 15,
                "LOOK_LEFT": 0.4,
                "LOOK_UP": 0.2,
            }
        },
        {
            "time": [1.8],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)

# ----------------------------------------------------------------------------------------------------
# Gesture definition: NodListening
# Usage: furhat.gesture(body=emotionGestureDefinition.NodListening)
NodListening = GestureDefinition(
    name="NodListening",
    frames=[
        {
            "time": [0.2, 0.3],
            "persist": False,
            "params": {
                "NECK_TILT": -10
            }
        },
        {
            "time": [0.5],
            "persist": False,
            "params": {
                "reset": True
            }
        },
        {
            "time": [0.7, 0.8],
            "persist": False,
            "params": {
                "NECK_TILT": 10
            }
        },
        {
            "time": [1.0],
            "persist": False,
            "params": {
                "reset": True
            }
        },
        {
            "time": [1.2, 1.3],
            "persist": False,
            "params": {
                "NECK_TILT": -10
            }
        },
        {
            "time": [1.5],
            "persist": False,
            "params": {
                "reset": True
            }
        },
        {
            "time": [1.7, 1.8],
            "persist": False,
            "params": {
                "NECK_TILT": 10
            }
        },
        {
            "time": [2.0],
            "persist": False,
            "params": {
                "reset": True
            }
        }],
    _class="furhatos.gestures.Gesture"
)
