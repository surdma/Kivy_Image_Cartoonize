# Cartoonize Image using opencv and kivy

These project use the **kivymd** GUI framework as a mobile solution and desktop solution to automated realtime cartoon software.
The opencv libray is used as the image processing library

Their are two main classes in this project the first class manage the cartoon processing while the second class manage the GUI part of the project.


## STEPS

* The camera was initiated inside the class constructor
* I use the clock class from kivy to schedule to a function call for the future then pass in a callback function call **Frame** taking two parameters.
* Inside the frame class I flip the image captured from the camera then converts it to bytes
* Kivy cannot display the opencv output directly so I canverted it to a texture class 
* I created a button to cartoonify then bind it to a function cartoon

### Cartoonify Process

1. I convert the frame from bgr2rgb 
2. I converted the rgb frames to gray for easy processing
3. to smooth the image I Icall the medianBlur which takes the gray and kernel_size as an arguments
4. I threshold and remove the noise from the frame
5. Then using the bitwise_and function i cartoonify the image.
