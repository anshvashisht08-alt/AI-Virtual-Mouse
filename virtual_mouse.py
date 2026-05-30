import cv2
import mediapipe as mp
import pyautogui
import math
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# -----------------------------
# INSTALL THESE LIBRARIES FIRST
# pip install opencv-python mediapipe pyautogui
# pip install screen-brightness-control pycaw comtypes
# -----------------------------

# Webcam
cap = cv2.VideoCapture(0)
print(cap.isOpened())

# Screen Size
screen_w, screen_h = pyautogui.size()

# Mediapipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

mp_draw = mp.solutions.drawing_utils

# Volume Setup
#devices = AudioUtilities.GetSpeakers()

#interface = devices._ctl.QueryInterface(IAudioEndpointVolume)

#volume = interface

# Variables
click_delay = 0
drag_mode = False

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            landmark_list = []

            for id, lm in enumerate(hand_landmarks.landmark):

                x = int(lm.x * w)
                y = int(lm.y * h)

                landmark_list.append((x, y))

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Fingertips
            thumb_x, thumb_y = landmark_list[4]
            index_x, index_y = landmark_list[8]
            middle_x, middle_y = landmark_list[12]
            ring_x, ring_y = landmark_list[16]
            pinky_x, pinky_y = landmark_list[20]

            # =========================
            # CURSOR MOVEMENT
            # =========================
            screen_x = screen_w / w * index_x
            screen_y = screen_h / h * index_y

            pyautogui.moveTo(
                screen_x,
                screen_y,
                duration=0.02
            )

            cv2.circle(
                frame,
                (index_x, index_y),
                10,
                (0, 255, 0),
                -1
            )

            # =========================
            # LEFT CLICK
            # =========================
            click_distance = math.hypot(
                thumb_x - index_x,
                thumb_y - index_y
            )

            if click_distance < 35 and click_delay == 0:

                pyautogui.click()

                click_delay = 15

                cv2.putText(
                    frame,
                    "LEFT CLICK",
                    (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

            # =========================
            # RIGHT CLICK
            # Thumb + Middle Finger
            # =========================
            right_click_distance = math.hypot(
                thumb_x - middle_x,
                thumb_y - middle_y
            )

            if right_click_distance < 35 and click_delay == 0:

                pyautogui.rightClick()

                click_delay = 15

                cv2.putText(
                    frame,
                    "RIGHT CLICK",
                    (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3
                )

            # =========================
            # DOUBLE CLICK
            # Thumb + Ring Finger
            # =========================
            double_click_distance = math.hypot(
                thumb_x - ring_x,
                thumb_y - ring_y
            )

            if double_click_distance < 35 and click_delay == 0:

                pyautogui.doubleClick()

                click_delay = 15

                cv2.putText(
                    frame,
                    "DOUBLE CLICK",
                    (30, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 0),
                    3
                )

            # =========================
            # DRAG & DROP
            # Thumb + Pinky
            # =========================
            drag_distance = math.hypot(
                thumb_x - pinky_x,
                thumb_y - pinky_y
            )

            if drag_distance < 40:

                if not drag_mode:
                    pyautogui.mouseDown()
                    drag_mode = True

                cv2.putText(
                    frame,
                    "DRAG MODE",
                    (30, 230),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

            else:
                if drag_mode:
                    pyautogui.mouseUp()
                    drag_mode = False

            # =========================
            # VOLUME CONTROL
            # Distance Thumb + Index
            # =========================
            volume_distance = math.hypot(
                thumb_x - index_x,
                thumb_y - index_y
            )

            volume_level = max(
                min(volume_distance / 2, 100),
                0
            )

            #volume.SetMasterVolumeLevelScalar(
                #volume_level / 100,
                #None
            #)

            # =========================
            # BRIGHTNESS CONTROL
            # Distance Thumb + Middle
            # =========================
            brightness_distance = math.hypot(
                thumb_x - middle_x,
                thumb_y - middle_y
            )

            brightness_level = max(
                min(brightness_distance * 2, 100),
                0
            )

            try:
                sbc.set_brightness(int(brightness_level))
            except:
                pass

            # =========================
            # SCREENSHOT
            # All fingers close
            # =========================
            all_close = (
                click_distance < 40 and
                right_click_distance < 40 and
                double_click_distance < 40
            )

            if all_close and click_delay == 0:

                screenshot = pyautogui.screenshot()

                screenshot.save("AI_Screenshot.png")

                click_delay = 30

                cv2.putText(
                    frame,
                    "SCREENSHOT SAVED",
                    (30, 280),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    3
                )

            # Reduce Delay
            if click_delay > 0:
                click_delay -= 1

    # =========================
    # TITLE
    # =========================
    cv2.putText(
        frame,
        "AI VIRTUAL MOUSE PRO",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        3
    )

    cv2.imshow("AI Virtual Mouse Pro", frame)

    # ESC = EXIT
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
