# Astronomia3D
#### Astronomy

**'Astronomia 3D'** provides animated 3-dimensional visualizations of planets' positions relative to the horizon for a particular location at current time. E.g.: it shows which planet is visible in what part of the sky, when the Sun, Moon are rising, etc.

Download executable file [Astronomia3D.exe](https://github.com/Drozdman-1/Astronomia3D/releases/download/v1/Astronomia3D_Popiel.exe).

![Astro3D](demo-images/Astronomia3D_animation.gif)

This program uses [Swiss Ephemeris](https://www.astro.com/swisseph/) (authors: Dieter Koch and Alois Treindl) and Python extension to the Swiss Ephemeris, [Pyswisseph](https://astrorigin.com/pyswisseph/) (author: Stanislas Marquis).

[github.com/astrorigin/pyswisseph](https://github.com/astrorigin/pyswisseph)  

*One can use a command line option to start the program with a chosen time, latitude and longitude.*

*To save animations, 'ffmpeg' must be installed and added to PATH.*

If there are problems with installing Pyswisseph, wheel (whl) installation may help.
Download a wheel from [Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyswisseph). Choose one for the right version of Python (32bit or 64bit).

