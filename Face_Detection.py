import cv2
import sys
import os

# Loading Haar Cascade XML file
def load_cascade():
    cascade_path=cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade=cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print("Could not load Haar Cascade XML file.")
        sys.exit(1)

    print("Haar Cascade loaded successfully.")
    return face_cascade


def detect_faces(frame, face_cascade, mode="webcam"):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if mode == "webcam":
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=9,   
            minSize=(90, 90),  # only detect large nearby faces
            flags=cv2.CASCADE_SCALE_IMAGE
        )
    else:
        #IMAGE settings
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5, 
            minSize=(30, 30),  
            flags=cv2.CASCADE_SCALE_IMAGE
        )

    # Aspect ratio filter
    filtered_faces = []
    for (x, y, w, h) in faces:
        aspect_ratio = w / float(h)
        if 0.7 <= aspect_ratio <= 1.5:
            filtered_faces.append((x, y, w, h))
    faces = filtered_faces

    face_count = len(faces)

    # Draw a green rectangle and label around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Face", (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display total face count in top-left corner
    label = f"Faces Detected: {face_count}"
    cv2.putText(frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    return frame, face_count


# MODE 1: Real-time detection from webcam

def run_webcam_mode(face_cascade):
    """Capture video from webcam and detect faces in real time."""
    print("\n[MODE] Real-Time Webcam Face Detection")
    print("[INFO] Press 'Q' to quit\n")

    cap=cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Cannot access webcam.")
        return False

    while True:
        ret, frame = cap.read()

        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Use webcam-tuned parameters
        output_frame, count = detect_faces(frame, face_cascade, mode="webcam")

        cv2.imshow("Face Detection - Press Q to Quit", output_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == ord('Q'):
            print("[INFO] Exiting webcam mode.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


# MODE 2: Detection on a static image file

def run_image_mode(face_cascade, image_path):
    """Detect faces in a given image file and save the result."""
    print(f"\n[MODE] Static Image Face Detection")
    print(f"[INFO] Processing: {image_path}\n")

    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        sys.exit(1)

    image = cv2.imread(image_path)

    if image is None:
        print("[ERROR] Could not read image file.")
        sys.exit(1)

    output_image, face_count = detect_faces(image, face_cascade, mode="image")

    print(f"[RESULT] Total Faces Detected: {face_count}")

    output_path = "output_detected.jpg"
    cv2.imwrite(output_path, output_image)
    print(f"[INFO] Result saved as '{output_path}'")

    cv2.imshow("Face Detection Result", output_image)
    print("[INFO] Press any key to close the window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()




# Main
def main():
    print("   FACE DETECTION USING HAAR CASCADES")
    print("=" * 55)

    face_cascade = load_cascade()

    print("\nSelect Mode:")
    print("  1. Real-Time Webcam Detection")
    print("  2. Detect Faces in an Image File")
    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        success = run_webcam_mode(face_cascade)
        if not success:
            image_path = input("Enter image file path: ").strip()
            run_image_mode(face_cascade, image_path)

    elif choice == "2":
        image_path = input("Enter image file path (e.g. photo.jpg): ").strip()
        run_image_mode(face_cascade, image_path)

    else:
        print("[ERROR] Invalid choice. Please enter 1 or 2.")
        sys.exit(1)


if __name__ == "__main__":
    main()
