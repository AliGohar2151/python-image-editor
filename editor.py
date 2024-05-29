# By Ali Gohar

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
from tkinter import filedialog, Frame, Button
from PIL import Image
from tkinter import messagebox
import numpy as np
import cv2
from PIL import ImageChops

img = None
label = None
orignalimage = None
image_name = None
initial_operation = 1
outputImage = None


# Upload Image
def uploadImage():
    global img, orignalimage, image_name
    imgname = filedialog.askopenfilename(title="Change Image")
    if imgname:
        img = Image.open(imgname)
        orignalimage = img.copy()
        image_name = imgname
        imageAdjestment(imgname)


# image Adjestment
def imageAdjestment(imgname):
    global img
    img = Image.open(imgname)
    img.thumbnail((600, 600))
    displayImage(img)


# Reset Image
def resetImage():
    global image_name, initial_operation, orignalimage
    imageAdjestment(image_name)


# Display Image
def displayImage(img):
    global photo
    global label
    if label:
        label.destroy()
    photo = ImageTk.PhotoImage(img)
    label = Label(mains, image=photo)
    label.image = photo
    label.place(x=10, y=100)


# Flip Image Horizontally
def flipImageH():
    global img, outputImage  # Update global variables
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    outputImage = (
        img if outputImage is None else outputImage.transpose(Image.FLIP_LEFT_RIGHT)
    )  # Update outputImage
    displayImage(outputImage if outputImage else img)


# Flip Image Vertically
def flipImageV():
    global img, outputImage  # Update global variables
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    outputImage = (
        img if outputImage is None else outputImage.transpose(Image.FLIP_TOP_BOTTOM)
    )  # Update outputImage
    displayImage(outputImage if outputImage else img)


# Rotate Image
def rotateImage():
    global img, outputImage  # Update global variables
    img = img.rotate(90)
    outputImage = (
        img if outputImage is None else outputImage.rotate(90)
    )  # Update outputImage
    displayImage(outputImage if outputImage else img)


# Emboss Image
def embossImage():
    global img, outputImage  # Update global variables
    img = img.filter(ImageFilter.EMBOSS)
    outputImage = (
        img if outputImage is None else outputImage.filter(ImageFilter.EMBOSS)
    )  # Update outputImage
    displayImage(outputImage if outputImage else img)


# Edge Enhance
def edgeEnhance():
    global img, outputImage  # Update global variables
    img = img.filter(ImageFilter.FIND_EDGES)
    outputImage = (
        img if outputImage is None else outputImage.filter(ImageFilter.FIND_EDGES)
    )  # Update outputImage
    displayImage(outputImage if outputImage else img)


# Blur Image
def blurBackground():
    global img, outputImage
    if img:
        img_array = np.array(outputImage)
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        mask = np.zeros(img_array.shape[:2], np.uint8)
        rect = (10, 10, img_array.shape[1] - 10, img_array.shape[0] - 10)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        cv2.grabCut(
            img_array, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT
        )
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
        img_array_fg = img_array * mask2[:, :, np.newaxis]
        blurred_img = cv2.GaussianBlur(img_array, (21, 21), 0)
        combined = img_array_fg + blurred_img * (1 - mask2[:, :, np.newaxis])
        combined_img = Image.fromarray(combined)
        displayImage(combined_img)


def resetSliderValues():
    brighten_slider.set(initial_operation)
    contrast_slider.set(initial_operation)
    sharpness_slider.set(initial_operation)
    color_slider.set(initial_operation)


# Brightness Control
def brightnessControl(brightness_pos):
    brightness_pos = float(brightness_pos)
    global outputImage
    enhancer = ImageEnhance.Brightness(img)
    outputImage = enhancer.enhance(brightness_pos)
    displayImage(outputImage)


# Contast Control
def contrastControl(contrasr_pos):
    contrasr_pos = float(contrasr_pos)
    global outputImage
    enhancer = ImageEnhance.Contrast(img)
    outputImage = enhancer.enhance(contrasr_pos)
    displayImage(outputImage)


# Sharpness Control
def sharpnessControl(sharpness_pos):
    sharpness_pos = float(sharpness_pos)
    global outputImage
    enhancer = ImageEnhance.Sharpness(img)
    outputImage = enhancer.enhance(sharpness_pos)
    displayImage(outputImage)


# Colors Control
def colorsControl(colors_pos):
    global outputImage
    colors_pos = float(colors_pos)
    enhancer = ImageEnhance.Color(img)
    outputImage = enhancer.enhance(colors_pos)
    displayImage(outputImage)


# Apply Grayscale Filter
def gayscaleFilter():
    global img, output_image
    if img:
        output_image = img.convert("L")  # Convert image to grayscale
        displayImage(output_image)


# Apply Spias Filter
def applySepia():
    global img, outputImage
    if img:
        img_sepia = np.array(
            img, dtype=np.float64
        )  # converting to float to prevent loss
        img_sepia = cv2.transform(
            img_sepia,
            np.matrix(
                [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
            ),
        )  # multipying image with special sepia matrix
        img_sepia[np.where(img_sepia > 255)] = (
            255  # normalizing values greater than 255 to 255
        )
        outputImage = np.array(img_sepia, dtype=np.uint8)
        outputImage = Image.fromarray(outputImage)  # Convert array to image
        displayImage(outputImage)
    else:
        print("No image to apply sepia to.")


# Vivid
def vividFilter(brightness=1, saturation=1.6, contrast=1.3):
    global img, outputImage
    if img:
        enhancer = ImageEnhance.Brightness(img)
        img_brightness = enhancer.enhance(brightness)

        enhancer = ImageEnhance.Color(img_brightness)
        img_saturation = enhancer.enhance(saturation)

        enhancer = ImageEnhance.Contrast(img_saturation)
        outputImage = enhancer.enhance(contrast)

        displayImage(outputImage)
    else:
        print("No image to apply filter to.")


# Custom filters
def customFilter(brightness=0.7, saturation=1.5, contrast=1.1):
    global img, outputImage
    if img:
        enhancer = ImageEnhance.Brightness(img)
        img_brightness = enhancer.enhance(brightness)

        enhancer = ImageEnhance.Color(img_brightness)
        img_saturation = enhancer.enhance(saturation)

        enhancer = ImageEnhance.Contrast(img_saturation)
        outputImage = enhancer.enhance(contrast)

        displayImage(outputImage)
    else:
        print("No image to apply filter to.")


def customFilter2():
    global img, outputImage
    if img:
        img_array = np.array(img)

        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 100, 200)

        mask = np.zeros(img_array.shape[:2], np.uint8)
        rect = (10, 10, img_array.shape[1] - 10, img_array.shape[0] - 10)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        cv2.grabCut(
            img_array, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT
        )

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
        img_array_fg = img_array * mask2[:, :, np.newaxis]
        blurred_img = cv2.GaussianBlur(img_array, (21, 21), 0)
        combined = img_array_fg + blurred_img * (1 - mask2[:, :, np.newaxis])
        combined_img = Image.fromarray(combined)
        outputImage = ImageEnhance.Color(combined_img).enhance(2.0)
        displayImage(outputImage)
    else:
        print("No image to process.")


# Save Image
def saveImage():
    global img
    if img:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ],
        )
        if save_path:
            img.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully.")
        else:
            messagebox.showinfo("Cancelled", "Save operation cancelled.")
    else:
        messagebox.showwarning("No Image", "There is no image to save.")


mains = Tk()

width = mains.winfo_screenwidth()
height = mains.winfo_screenheight()
mains.geometry("%dx%d" % (width, height))
mains.config(background="#092635")
mains.title("Image Editor")


button_x = ((width - 250) / 2) + 200

# Create a frame to hold the buttons
button_frame = Frame(
    mains, bg="#092635", highlightbackground="white", highlightthickness=2
)
button_frame.place(x=10, y=10, width=600, height=55)


# Upload Button
upload_button = Button(
    button_frame,
    text="Upload Image",
    height=1,
    width=25,
    background="#1B4242",
    activebackground="#5C8374",
    command=uploadImage,
)
upload_button.configure(font=("poppins", 11, "bold"), foreground="white")
upload_button.place(x=10, y=10)

# Reset Button
reset_button = Button(
    button_frame,
    text="Reset Operations",
    height=1,
    width=25,
    background="#F6B17A",
    activebackground="#5C8374",
    command=lambda: [resetImage(), resetSliderValues()],
)
reset_button.configure(font=("poppins", 11, "bold"), foreground="white")
reset_button.place(x=252, y=10)

# Save Image Button
save_button = Button(
    button_frame,
    text="Save Image",
    height=1,
    width=9,
    background="#FFB178",
    activebackground="#5C8374",
    command=saveImage,
)
save_button.configure(font=("poppins", 11, "bold"), foreground="white")
save_button.place(x=495, y=10)


label1 = Label(
    mains,
    text="Edit Image",
    bg="#092635",
    fg="white",
    font=("poppins", 12, "bold"),
)
label1.place(x=button_x, y=70)

# frame to hold the image editing buttons
edit_button_frame = Frame(
    mains, bg="#092635", highlightbackground="white", highlightthickness=2
)
edit_button_frame.place(x=button_x, y=100, width=260, height=280)


# Rotate Button
rotate_button = Button(
    edit_button_frame,
    text="Rotate Image",
    height=1,
    width=25,
    background="#2D3250",
    activebackground="#5C8374",
    command=rotateImage,
)
rotate_button.configure(font=("poppins", 11, "bold"), foreground="white")
rotate_button.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")

# Flip Button
flip_button_h = Button(
    edit_button_frame,
    text="Flip Image Horizontally",
    height=1,
    width=25,
    background="#2D3250",
    activebackground="#5C8374",
    command=flipImageH,
)
flip_button_h.configure(font=("poppins", 11, "bold"), foreground="white")
flip_button_h.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

# Flip Button Vertical
flip_button_v = Button(
    edit_button_frame,
    text="Flip Image Vertically",
    height=1,
    width=25,
    background="#2D3250",
    activebackground="#5C8374",
    command=flipImageV,
)
flip_button_v.configure(font=("poppins", 11, "bold"), foreground="white")
flip_button_v.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

# Enboss Button
emboss_button = Button(
    edit_button_frame,
    text="Emboss Image",
    height=1,
    width=25,
    background="#2D3250",
    activebackground="#5C8374",
    command=embossImage,
)
emboss_button.configure(font=("poppins", 11, "bold"), foreground="white")
emboss_button.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

# Edge Enhance Button
edge_enhance_button = Button(
    edit_button_frame,
    text="Edge Enhance",
    height=1,
    width=25,
    background="#2D3250",
    activebackground="#5C8374",
    command=edgeEnhance,
)
edge_enhance_button.configure(font=("poppins", 11, "bold"), foreground="white")
edge_enhance_button.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

# Blur Background Button
blur_button = Button(
    edit_button_frame,
    text="Blur Background",
    height=1,
    width=25,
    background="#2D3250",
    activebackground="#5C8374",
    command=blurBackground,
)
blur_button.configure(font=("poppins", 11, "bold"), foreground="white")
blur_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")


label2 = Label(
    mains,
    text="Image Adjestment",
    bg="#092635",
    fg="white",
    font=("poppins", 12, "bold"),
)
label2.place(x=button_x, y=400)

# frame to hold image adjestments controls
adjestment_frame = Frame(
    mains, bg="#092635", highlightbackground="white", highlightthickness=2
)
adjestment_frame.place(x=button_x, y=430, width=520, height=168)

# Brightness Slider
brighten_slider = Scale(
    adjestment_frame,
    label="Brightness",
    from_=-0,
    to=2,
    orient=HORIZONTAL,
    length=230,
    resolution=0.1,
    bg="#2D3250",
    command=brightnessControl,
)
brighten_slider.set(initial_operation)
brighten_slider.configure(font=("poppins", 11, "bold"), foreground="white")
brighten_slider.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")

# Contrast Slider
contrast_slider = Scale(
    adjestment_frame,
    label="Contrast",
    from_=-0,
    to=2,
    orient=HORIZONTAL,
    length=230,
    resolution=0.1,
    bg="#2D3250",
    command=contrastControl,
)
contrast_slider.set(initial_operation)
contrast_slider.configure(font=("poppins", 11, "bold"), foreground="white")
contrast_slider.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="ew")


# Sharpness Slider
sharpness_slider = Scale(
    adjestment_frame,
    label="Sharpness",
    from_=-0,
    to=2,
    orient=HORIZONTAL,
    length=230,
    resolution=0.1,
    bg="#2D3250",
    command=sharpnessControl,
)
sharpness_slider.set(initial_operation)
sharpness_slider.configure(font=("poppins", 11, "bold"), foreground="white")
sharpness_slider.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

# Color Slider
color_slider = Scale(
    adjestment_frame,
    label="Saturation",
    from_=-0,
    to=2,
    orient=HORIZONTAL,
    length=230,
    resolution=0.1,
    bg="#2D3250",
    command=colorsControl,
)
color_slider.set(initial_operation)
color_slider.configure(font=("poppins", 11, "bold"), foreground="white")
color_slider.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

label3 = Label(
    mains,
    text="Filters",
    bg="#092635",
    fg="white",
    font=("poppins", 12, "bold"),
)
label3.place(x=button_x + 270, y=70)

# frame to hold the image filters buttons
filters_frame = Frame(
    mains, bg="#092635", highlightbackground="white", highlightthickness=2
)
filters_frame.place(x=button_x + 270, y=100, width=250, height=280)


# GrayScale filter button

grayscale_button = Button(
    filters_frame,
    text="Grayscale",
    height=1,
    width=24,
    background="#2D3250",
    activebackground="#5C8374",
    command=gayscaleFilter,
)
grayscale_button.configure(font=("poppins", 11, "bold"), foreground="white")
grayscale_button.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")


# Spia filter button
sepia_button = Button(
    filters_frame,
    text="Sepia",
    height=1,
    width=24,
    background="#2D3250",
    activebackground="#5C8374",
    command=applySepia,
)
sepia_button.configure(font=("poppins", 11, "bold"), foreground="white")
sepia_button.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

# Custom Vivid Button
vivid_button = Button(
    filters_frame,
    text="vivid Filter",
    height=1,
    width=24,
    background="#2D3250",
    activebackground="#5C8374",
    command=vividFilter,
)
vivid_button.configure(font=("poppins", 11, "bold"), foreground="white")
vivid_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

# Custom Filter Button
custom1_button = Button(
    filters_frame,
    text="Custom Filter 1",
    height=1,
    width=24,
    background="#2D3250",
    activebackground="#5C8374",
    command=customFilter,
)
custom1_button.configure(font=("poppins", 11, "bold"), foreground="white")
custom1_button.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

# Custom 2 Filter Button
custom2_button = Button(
    filters_frame,
    text="Custom Filter 2",
    height=1,
    width=24,
    background="#2D3250",
    activebackground="#5C8374",
    command=customFilter2,
)
custom2_button.configure(font=("poppins", 11, "bold"), foreground="white")
custom2_button.grid(row=4, column=0, pady=5, padx=10, sticky="ew")


mains.mainloop()
