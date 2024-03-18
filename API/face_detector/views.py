from django.http import JsonResponse
import cv2

def detect_faces(request):
    if request.method == 'POST':
        image_data = request.FILES.get('image')
        if image_data:
            # Read the image
            image_array = cv2.imdecode(np.fromstring(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
            # Convert the image to grayscale
            gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            # Load the face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            # Process detected faces
            num_faces = len(faces)
            # Return response
            return JsonResponse({'num_faces': num_faces})
        else:
            return JsonResponse({'error': 'No image provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

