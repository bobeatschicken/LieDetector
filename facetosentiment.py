import io

def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    if (not image):
        return
    try:
        response = client.face_detection(image=image)
    except:
        print ("image is empty")
        return
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    if(len(faces) == 0):
        return

    main_face = faces[0]
    return main_face
