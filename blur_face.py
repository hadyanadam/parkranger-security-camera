import cv2
import numpy as np

prototxt_path = "./deploy.prototxt.txt"
model_path = "./res10_300x300_ssd_iter_140000_fp16.caffemodel"
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

def muka_blur(img_path):
    # read the desired image
    image = cv2.imread(img_path)
    # get width and height of the image
    h, w = image.shape[:2]
    # gaussian blur kernel size depends on width and height of original image
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1
    # preprocess the image: resize and performs mean subtraction
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    # set the image into the input of the neural network
    model.setInput(blob)
    # perform inference and get the result
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        confidence = output[i, 2]
        # get the confidence
        # if confidence is above 40%, then blur the bounding box (face)
        if confidence > 0.4:
            # get the surrounding box cordinates and upscale them to original image
            box = output[i, 3:7] * np.array([w, h, w, h])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int)
            # get the face image
            face = image[start_y: end_y, start_x: end_x]
            # apply gaussian blur to this face
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            # put the blurred face into the original image
            image[start_y: end_y, start_x: end_x] = face
        # cv2.imshow("image", image)
        # cv2.waitKey(0)
        cv2.imwrite("capture1_blurred.jpg", image)
        return "capture_blurred.jpg"

if __name__ == "__main__":
    muka_blur("./capture_blurred.jpg")