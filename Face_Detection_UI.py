import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
import sys


# ── Load Haar Cascade ────────────────────────────────────────────────────────

def load_cascade():
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        messagebox.showerror("Error", "Could not load Haar Cascade XML file.")
        sys.exit(1)
    return cascade

FACE_CASCADE = load_cascade()


# ── Face detection logic ─────────────────────────────────────────────────────

def detect_faces(frame, mode="webcam"):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if mode == "webcam":
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.equalizeHist(gray)
        faces = FACE_CASCADE.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=9,
            minSize=(90, 90), flags=cv2.CASCADE_SCALE_IMAGE
        )
    else:
        gray = cv2.equalizeHist(gray)
        faces = FACE_CASCADE.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5,
            minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
        )

    filtered = []
    for (x, y, w, h) in faces:
        if 0.7 <= w / float(h) <= 1.5:
            filtered.append((x, y, w, h))

    for (x, y, w, h) in filtered:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 230, 100), 2)
        cv2.putText(frame, "Face", (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 230, 100), 2)

    cv2.putText(frame, f"Faces: {len(filtered)}", (10, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 220, 255), 2)

    return frame, len(filtered)


# ── Main Application ─────────────────────────────────────────────────────────

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection — COMSATS CV Lab")
        self.root.resizable(False, False)
        self.root.configure(bg="#0d0d14")

        self.cap = None
        self.webcam_running = False
        self.webcam_thread = None

        self._build_ui()

    # ── UI Layout ────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg="#0d0d14")
        header.pack(fill="x", padx=24, pady=(20, 0))

        tk.Label(header, text="FACE DETECTION", font=("Courier", 22, "bold"),
                 fg="#00e5ff", bg="#0d0d14").pack(side="left")

        tk.Label(header, text="Haar Cascades · OpenCV · COMSATS",
                 font=("Courier", 9), fg="#445566", bg="#0d0d14").pack(side="right", pady=6)

        # Divider
        tk.Frame(self.root, height=1, bg="#00e5ff").pack(fill="x", padx=24, pady=(8, 16))

        # ── Canvas (video/image display) ─────────────────────────────────────
        self.canvas = tk.Canvas(self.root, width=640, height=420,
                                bg="#111825", highlightthickness=0)
        self.canvas.pack(padx=24)

        # Placeholder text on canvas
        self.canvas.create_text(320, 210,
                                text="📷  Choose Webcam or Upload an Image",
                                fill="#334455", font=("Courier", 13))

        # ── Face count badge ─────────────────────────────────────────────────
        badge_row = tk.Frame(self.root, bg="#0d0d14")
        badge_row.pack(fill="x", padx=24, pady=(12, 0))

        tk.Label(badge_row, text="FACES DETECTED", font=("Courier", 9, "bold"),
                 fg="#445566", bg="#0d0d14").pack(side="left")

        self.count_var = tk.StringVar(value="—")
        tk.Label(badge_row, textvariable=self.count_var,
                 font=("Courier", 22, "bold"), fg="#00e5ff",
                 bg="#0d0d14").pack(side="left", padx=12)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(badge_row, textvariable=self.status_var,
                 font=("Courier", 9), fg="#556677",
                 bg="#0d0d14").pack(side="right")

        # Divider
        tk.Frame(self.root, height=1, bg="#1a2233").pack(fill="x", padx=24, pady=(12, 16))

        # ── Buttons ──────────────────────────────────────────────────────────
        btn_row = tk.Frame(self.root, bg="#0d0d14")
        btn_row.pack(pady=(0, 8))

        self.webcam_btn = self._make_btn(btn_row, "▶  START WEBCAM",
                                         "#00e5ff", "#0d0d14", self.start_webcam)
        self.webcam_btn.pack(side="left", padx=8)

        self.stop_btn = self._make_btn(btn_row, "⏹  STOP",
                                       "#334455", "#aabbcc", self.stop_webcam)
        self.stop_btn.pack(side="left", padx=8)
        self.stop_btn.config(state="disabled")

        self.image_btn = self._make_btn(btn_row, "🖼  UPLOAD IMAGE",
                                        "#1a2a3a", "#00e5ff", self.open_image)
        self.image_btn.pack(side="left", padx=8)

        self.save_btn = self._make_btn(btn_row, "💾  SAVE RESULT",
                                       "#1a2a3a", "#aabbcc", self.save_result)
        self.save_btn.pack(side="left", padx=8)
        self.save_btn.config(state="disabled")

        # ── Footer ───────────────────────────────────────────────────────────
        tk.Label(self.root,
                 text="Lab MidTerm SP-2026  ·  Instructor: Maheen Gul  ·  Dept. of Computer Science",
                 font=("Courier", 8), fg="#2a3a4a", bg="#0d0d14").pack(pady=(8, 14))

        self.current_result = None   # stores last processed image for saving

    def _make_btn(self, parent, text, bg, fg, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         font=("Courier", 10, "bold"),
                         bg=bg, fg=fg,
                         activebackground="#00b8cc", activeforeground="#0d0d14",
                         relief="flat", padx=14, pady=8, cursor="hand2",
                         bd=0)

    # ── Canvas helpers ───────────────────────────────────────────────────────

    def _show_frame_on_canvas(self, frame_bgr):
        """Convert OpenCV BGR frame → Tkinter PhotoImage and display."""
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img = img.resize((640, 420), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=photo)
        self.canvas.image = photo   # keep reference so GC doesn't delete it

    # ── Webcam mode ──────────────────────────────────────────────────────────

    def start_webcam(self):
        if self.webcam_running:
            return
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.\nMake sure your camera is connected.")
            return

        self.webcam_running = True
        self.status_var.set("Webcam active…")
        self.webcam_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.image_btn.config(state="disabled")
        self.save_btn.config(state="disabled")

        self.webcam_thread = threading.Thread(target=self._webcam_loop, daemon=True)
        self.webcam_thread.start()

    def _webcam_loop(self):
        while self.webcam_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            processed, count = detect_faces(frame.copy(), mode="webcam")
            self.current_result = processed.copy()
            self.root.after(0, self._update_webcam_ui, processed, count)

        if self.cap:
            self.cap.release()

    def _update_webcam_ui(self, frame, count):
        self._show_frame_on_canvas(frame)
        self.count_var.set(str(count))

    def stop_webcam(self):
        self.webcam_running = False
        self.status_var.set("Stopped")
        self.webcam_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.image_btn.config(state="normal")
        if self.current_result is not None:
            self.save_btn.config(state="normal")

    # ── Image mode ───────────────────────────────────────────────────────────

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                       ("All Files", "*.*")]
        )
        if not path:
            return

        image = cv2.imread(path)
        if image is None:
            messagebox.showerror("Error", "Could not read the selected image.")
            return

        self.status_var.set(f"Processing: {os.path.basename(path)}")
        processed, count = detect_faces(image.copy(), mode="image")
        self.current_result = processed.copy()

        self._show_frame_on_canvas(processed)
        self.count_var.set(str(count))
        self.status_var.set(f"Done — {os.path.basename(path)}")
        self.save_btn.config(state="normal")

    # ── Save result ──────────────────────────────────────────────────────────

    def save_result(self):
        if self.current_result is None:
            return
        path = filedialog.asksaveasfilename(
            title="Save Result As",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        if path:
            cv2.imwrite(path, self.current_result)
            self.status_var.set(f"Saved → {os.path.basename(path)}")
            messagebox.showinfo("Saved", f"Result saved to:\n{path}")

    # ── Cleanup on close ─────────────────────────────────────────────────────

    def on_close(self):
        self.webcam_running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()