import cv2
import mediapipe as mp
import pyautogui
import math
import time
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

CAMERA_INDEX = 0

SMOOTHING = 0.25

FRAME_MARGIN_X = 80
FRAME_MARGIN_Y = 60

CLICK_THRESHOLD = 35
DRAG_THRESHOLD = 40

GESTURE_STABLE_FRAMES = 3

CLICK_COOLDOWN = 0.4
DOUBLE_CLICK_COOLDOWN = 0.7

AUTO_SCROLL_DELAY = 0.45
AUTO_SCROLL_SPEED = 4

CONTROL_DEADZONE = 8
CONTROL_UPDATE_INTERVAL = 0.08

BRIGHTNESS_STEP = 2
VOLUME_STEP = 0.02

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

screen_w, screen_h = pyautogui.size()

print("Screen:", screen_w, "x", screen_h)

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

mp_draw = mp.solutions.drawing_utils

try:
    devices = AudioUtilities.GetSpeakers()

    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(
        interface,
        POINTER(IAudioEndpointVolume)
    )

    volume_available = True

    print("Volume control: READY")

except Exception as e:
    print("Volume control unavailable:", e)

    volume_available = False
    volume = None

smooth_x = screen_w / 2
smooth_y = screen_h / 2

drag_mode = False

last_click_time = 0
last_double_click_time = 0

scroll_start_time = None

previous_control_y = None
last_control_time = 0

previous_time = time.time()
fps = 0


def distance(point1, point2):
    return math.hypot(
        point1[0] - point2[0],
        point1[1] - point2[1]
    )


def get_fingers(landmarks):
    index_up = landmarks[8][1] < landmarks[6][1]
    middle_up = landmarks[12][1] < landmarks[10][1]
    ring_up = landmarks[16][1] < landmarks[14][1]
    pinky_up = landmarks[20][1] < landmarks[18][1]

    return index_up, middle_up, ring_up, pinky_up


def put_text(frame, text, y, color=(255, 255, 255)):
    cv2.putText(
        frame,
        text,
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
        cv2.LINE_AA
    )


while True:

    success, frame = cap.read()

    if not success:
        print("Camera frame could not be read.")
        break

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape

    current_time = time.time()

    delta_time = current_time - previous_time

    if delta_time > 0:
        fps = 1 / delta_time

    previous_time = current_time

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    result = hands.process(rgb)

    cv2.rectangle(
        frame,
        (FRAME_MARGIN_X, FRAME_MARGIN_Y),
        (w - FRAME_MARGIN_X, h - FRAME_MARGIN_Y),
        (80, 80, 80),
        2
    )

    if result.multi_hand_landmarks:

        hand_landmarks = result.multi_hand_landmarks[0]

        landmark_list = []

        for landmark in hand_landmarks.landmark:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            landmark_list.append((x, y))

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        thumb = landmark_list[4]
        index = landmark_list[8]
        middle = landmark_list[12]
        ring = landmark_list[16]
        pinky = landmark_list[20]

        index_up, middle_up, ring_up, pinky_up = get_fingers(
            landmark_list
        )

        thumb_index = distance(thumb, index)
        thumb_middle = distance(thumb, middle)
        thumb_ring = distance(thumb, ring)
        thumb_pinky = distance(thumb, pinky)

        only_index = (
            index_up
            and not middle_up
            and not ring_up
            and not pinky_up
        )

        two_fingers = (
            index_up
            and middle_up
            and not ring_up
            and not pinky_up
        )

        three_fingers = (
            index_up
            and middle_up
            and ring_up
            and not pinky_up
        )

        four_fingers = (
            index_up
            and middle_up
            and ring_up
            and pinky_up
        )

        if only_index and not drag_mode:

            camera_x = max(
                FRAME_MARGIN_X,
                min(index[0], w - FRAME_MARGIN_X)
            )

            camera_y = max(
                FRAME_MARGIN_Y,
                min(index[1], h - FRAME_MARGIN_Y)
            )

            target_x = (
                (camera_x - FRAME_MARGIN_X)
                / (w - 2 * FRAME_MARGIN_X)
            ) * screen_w

            target_y = (
                (camera_y - FRAME_MARGIN_Y)
                / (h - 2 * FRAME_MARGIN_Y)
            ) * screen_h

            target_x = max(
                0,
                min(target_x, screen_w - 1)
            )

            target_y = max(
                0,
                min(target_y, screen_h - 1)
            )

            smooth_x = (
                smooth_x
                + (target_x - smooth_x) * SMOOTHING
            )

            smooth_y = (
                smooth_y
                + (target_y - smooth_y) * SMOOTHING
            )

            pyautogui.moveTo(
                int(smooth_x),
                int(smooth_y)
            )

            put_text(
                frame,
                "CURSOR",
                80,
                (0, 255, 0)
            )

        elif two_fingers and not drag_mode:

            if scroll_start_time is None:
                scroll_start_time = current_time

            if current_time - scroll_start_time > AUTO_SCROLL_DELAY:

                pyautogui.scroll(
                    -AUTO_SCROLL_SPEED
                )

                put_text(
                    frame,
                    "AUTO SCROLL",
                    80,
                    (255, 200, 0)
                )

            else:

                put_text(
                    frame,
                    "SCROLL READY",
                    80,
                    (255, 200, 0)
                )

        else:

            scroll_start_time = None

        if four_fingers and not drag_mode:

            current_y = (
                index[1]
                + middle[1]
                + ring[1]
                + pinky[1]
            ) / 4

            if previous_control_y is not None:

                movement = (
                    previous_control_y - current_y
                )

                if (
                    abs(movement) > CONTROL_DEADZONE
                    and current_time - last_control_time
                    > CONTROL_UPDATE_INTERVAL
                ):

                    try:

                        current_brightness = int(
                            sbc.get_brightness()[0]
                        )

                        change = int(
                            movement / 8
                        ) * BRIGHTNESS_STEP

                        if change != 0:

                            new_brightness = max(
                                0,
                                min(
                                    100,
                                    current_brightness + change
                                )
                            )

                            sbc.set_brightness(
                                new_brightness
                            )

                            last_control_time = current_time

                    except Exception:
                        pass

            previous_control_y = current_y

            try:

                brightness_value = int(
                    sbc.get_brightness()[0]
                )

            except Exception:
                brightness_value = 0

            put_text(
                frame,
                f"BRIGHTNESS: {brightness_value}%",
                120,
                (255, 255, 255)
            )

        elif three_fingers and not drag_mode:

            current_y = (
                index[1]
                + middle[1]
                + ring[1]
            ) / 3

            if previous_control_y is not None:

                movement = (
                    previous_control_y - current_y
                )

                if (
                    abs(movement) > CONTROL_DEADZONE
                    and current_time - last_control_time
                    > CONTROL_UPDATE_INTERVAL
                ):

                    if volume_available:

                        try:

                            current_volume = (
                                volume.GetMasterVolumeLevelScalar()
                            )

                            change = (
                                int(movement / 8)
                                * VOLUME_STEP
                            )

                            new_volume = max(
                                0.0,
                                min(
                                    1.0,
                                    current_volume + change
                                )
                            )

                            volume.SetMasterVolumeLevelScalar(
                                new_volume,
                                None
                            )

                            last_control_time = current_time

                        except Exception:
                            pass

            previous_control_y = current_y

            if volume_available:

                try:

                    volume_value = int(
                        volume.GetMasterVolumeLevelScalar()
                        * 100
                    )

                except Exception:
                    volume_value = 0

            else:
                volume_value = 0

            put_text(
                frame,
                f"VOLUME: {volume_value}%",
                160,
                (0, 255, 255)
            )

        else:

            previous_control_y = None

        double_click_gesture = (
            thumb_index < CLICK_THRESHOLD
            and not middle_up
            and not ring_up
            and not pinky_up
        )

        single_click_gesture = (
            thumb_middle < CLICK_THRESHOLD
            and index_up
            and not ring_up
            and not pinky_up
        )

        right_click_gesture = (
            thumb_ring < CLICK_THRESHOLD
            and index_up
            and middle_up
            and not pinky_up
        )

        if double_click_gesture:

            if (
                current_time - last_double_click_time
                > DOUBLE_CLICK_COOLDOWN
            ):

                pyautogui.doubleClick()

                last_double_click_time = current_time

                put_text(
                    frame,
                    "DOUBLE CLICK",
                    200,
                    (255, 255, 0)
                )

        elif single_click_gesture:

            if (
                current_time - last_click_time
                > CLICK_COOLDOWN
            ):

                pyautogui.click()

                last_click_time = current_time

                put_text(
                    frame,
                    "SINGLE CLICK",
                    200,
                    (0, 255, 0)
                )

        elif right_click_gesture:

            if (
                current_time - last_click_time
                > CLICK_COOLDOWN
            ):

                pyautogui.rightClick()

                last_click_time = current_time

                put_text(
                    frame,
                    "RIGHT CLICK",
                    200,
                    (255, 150, 0)
                )

        drag_gesture = (
            thumb_pinky < DRAG_THRESHOLD
            and index_up
            and not middle_up
            and not ring_up
        )

        if drag_gesture:

            if not drag_mode:

                pyautogui.mouseDown()

                drag_mode = True

            put_text(
                frame,
                "DRAG MODE",
                240,
                (0, 0, 255)
            )

        else:

            if drag_mode:

                pyautogui.mouseUp()

                drag_mode = False

        cv2.circle(
            frame,
            index,
            8,
            (0, 255, 0),
            -1
        )

    else:

        scroll_start_time = None
        previous_control_y = None

        if drag_mode:

            pyautogui.mouseUp()

            drag_mode = False

    cv2.putText(
        frame,
        "AI VIRTUAL MOUSE PRO - V2",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (w - 110, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        "ESC = EXIT",
        (20, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (200, 200, 200),
        1,
        cv2.LINE_AA
    )

    cv2.imshow(
        "AI Virtual Mouse Pro V2",
        frame
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break


if drag_mode:
    pyautogui.mouseUp()

cap.release()
hands.close()
cv2.destroyAllWindows()

print("AI Virtual Mouse V2 stopped.")