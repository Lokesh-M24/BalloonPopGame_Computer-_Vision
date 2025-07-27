@echo off
echo Installing required libraries for BalloonPop game...
echo.

python -m pip install --upgrade pip
echo.

echo Installing pygame...
python -m pip install pygame
echo.

echo Installing opencv-python...
python -m pip install opencv-python
echo.

echo Installing cvzone...
python -m pip install cvzone
echo.

echo Installing mediapipe...
python -m pip install mediapipe
echo.

echo Installing numpy...
python -m pip install numpy
echo.

echo.
echo Installation complete!
echo.
echo To run the game, use the command: py -3.10 BalloonPop.py
echo.
pause