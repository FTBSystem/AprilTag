import pupil_apriltags 
import cv2

#only support tag36h11 (0-586)

cam = cv2.VideoCapture(0)# Open the default camera
cam.set(cv2.CAP_PROP_FPS, 30.0)
codec = 0x47504A4D  # MJPG
cam.set(cv2.CAP_PROP_FOURCC, codec)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

radius = 2
colorA = (51,170,255)
colorB = (0,0,255)
thickness = 2

detector=pupil_apriltags.Detector()

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1


while True:
    try:
        ret, frame = cam.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        result = detector.detect(gray)
        
        for cell in result:
            #print(cell)
            print(f"{cell.tag_id} {cell.decision_margin}")
            center_coordinates = (int(cell.center[0]),int(cell.center[1]))
            
            org = (int(cell.center[0]),int(cell.center[1]))
            
            a=(  int(cell.corners[0][0]) , int(cell.corners[0][1])  )
            b=(  int(cell.corners[1][0]) , int(cell.corners[1][1])  )
            c=(  int(cell.corners[2][0]) , int(cell.corners[2][1])  )
            d=(  int(cell.corners[3][0]) , int(cell.corners[3][1])  )
            
            frame = cv2.circle(frame, a, radius, colorB, thickness)
            frame = cv2.circle(frame, b, radius, colorB, thickness)
            frame = cv2.circle(frame, c, radius, colorB, thickness)
            frame = cv2.circle(frame, d, radius, colorB, thickness)

            frame = cv2.circle(frame, center_coordinates, radius, colorA, thickness)
            
            frame = cv2.putText(frame, str(cell.tag_id), org, font, fontScale, colorA, thickness, cv2.LINE_AA)
            

        cv2.imshow('Camera', frame)    # Display the captured frame
        cv2.imshow('gray', gray)    # Display the captured frame


        if cv2.waitKey(1) == ord('q'):     # Press 'q' to exit the loop
            break
    except Exception as e:
        print(e)
        break


# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()



