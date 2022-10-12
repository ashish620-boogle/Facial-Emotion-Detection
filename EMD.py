from tensorflow.keras.models import model_from_json
from tensorflow.keras.utils import img_to_array
import cv2
import numpy as np

model = model_from_json(open("Emotional Face detection/model.json", "r").read())
model.load_weights('Emotional Face detection/model.h5')
face_haar_cascade = cv2.CascadeClassifier('Emotional Face detection/haarcascade_frontalface_default.xml')

while 1:
    cap=cv2.VideoCapture(-1)
    while cap.isOpened():
        res,frame=cap.read()
        height, width , channel = frame.shape
        #---------------------------------------------------------------------------
        # Creating an Overlay window to write prediction and cofidence
        sub_img = frame[0:int(height/6),0:int(width)]
        black_rect = np.ones(sub_img.shape, dtype=np.uint8)*0
        res = cv2.addWeighted(sub_img, 0.77, black_rect,0.23, 0)
        FONT = cv2.FONT_HERSHEY_SIMPLEX
        FONT_SCALE = 0.8
        FONT_THICKNESS = 2
        lable_color = (10, 10, 255)
        lable = "Emotion Detection"
        lable_dimension = cv2.getTextSize(lable,FONT ,FONT_SCALE,FONT_THICKNESS)[0]
        textX = int((res.shape[1] - lable_dimension[0]) / 2)
        textY = int((res.shape[0] + lable_dimension[1]) / 2)
        cv2.putText(res, lable, (textX,textY), FONT, FONT_SCALE, (0,0,0), FONT_THICKNESS)
        # prediction part --------------------------------------------------------------------------
        gray_image= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_haar_cascade.detectMultiScale(gray_image )
        try:
            for (x,y, w, h) in faces:
                cv2.rectangle(frame, pt1 = (x,y),pt2 = (x+w, y+h), color = (255,0,0),thickness =  2)
                roi_gray = gray_image[y-5:y+h+5,x-5:x+w+5]
                roi_gray=cv2.resize(roi_gray,(48,48))
                image_pixels = img_to_array(roi_gray)
                image_pixels = np.expand_dims(image_pixels, axis = 0)
                image_pixels /= 255
                predictions = model.predict(image_pixels)
                max_index = np.argmax(predictions[0])
                emotion_detection = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
                emotion_prediction = emotion_detection[max_index]
                cv2.putText(res, "Sentiment: {}".format(emotion_prediction), (0,textY+22+5), FONT,0.7, lable_color,2)
                lable_violation = 'Confidence: {}'.format(str(np.round(np.max(predictions[0])*100,1))+ "%")
                violation_text_dimension = cv2.getTextSize(lable_violation,FONT,FONT_SCALE,FONT_THICKNESS )[0]
                violation_x_axis = int(res.shape[1]- violation_text_dimension[0])
                cv2.putText(res, lable_violation, (violation_x_axis,textY+22+5), FONT,0.7, lable_color,2)
        except :
            pass
        frame[0:int(height/6),0:int(width)] = res
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cap.release()
    cv2.destroyAllWindows