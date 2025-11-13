import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# State variables
in_jump_state = False 
is_ducking = False

print("✅ Ultimate Controller Ready! Fist to Duck, Up to Jump.")

def check_fist(landmarks):
    """Returns True if the hand is a fist (fingers curled down)"""
    # Finger tip IDs: Index(8), Middle(12), Ring(16), Pinky(20)
    # Finger PIP joint IDs (middle knuckle): 6, 10, 14, 18
    
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    
    fingers_folded = 0
    
    for i in range(4):
        # Remember: Y increases as you go DOWN the screen.
        # If Tip Y > PIP Y, the finger is bent down.
        if landmarks.landmark[tips[i]].y > landmarks.landmark[pips[i]].y:
            fingers_folded += 1
            
    # If 4 fingers are folded, we consider it a fist
    return fingers_folded == 4

while True:
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Draw the Jump Line
    jump_line_y = int(h * 0.4) 
    cv2.line(frame, (0, jump_line_y), (w, jump_line_y), (0, 255, 0), 2)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Track Index Finger for visual feedback
            index_tip = hand_landmarks.landmark[8]
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

            # --- 1. CHECK FOR FIST (DUCK) ---
            if check_fist(hand_landmarks):
                cv2.putText(frame, "DUCKING! 🦆", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
                if not is_ducking:
                    pyautogui.keyDown('down') # Hold the key down
                    is_ducking = True
            
            # --- 2. CHECK FOR JUMP ---
            else:
                # If we were ducking, stop ducking now
                if is_ducking:
                    pyautogui.keyUp('down') # Release the key
                    is_ducking = False

                # Now check if we should jump
                # Logic: Hand is OPEN (not fist) AND above the line
                if cy < jump_line_y:
                    cv2.putText(frame, "JUMP! 🚀", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                    
                    if not in_jump_state:
                        pyautogui.press('space')
                        in_jump_state = True
                
                elif cy > jump_line_y:
                    in_jump_state = False

    cv2.imshow("My Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()