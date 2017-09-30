# simon_kivy: CS50 Final Project

This is my final project for the CS50 course by HardardX/edX. I made an Android game using Python 3 and decided to leave some step by step helping guide for anyone who decides to do the same.

## Acknowledgments

* The inspiration for this guide came from the [JavaScript with Exponent and React Native](https://www.youtube.com/watch?v=rw1-lPlVH4Q) seminar. It was greatly informative, and it prompted me to search if it was possible to do something similar, but with Python instead of Javascript.

* Big thanks to everybody who made the CS50x course possible. It really is one of the best courses I've ever taken, and I'm really happy to join all those who wrote only the most positive reviews about it. 

* This was CS50! <:)~

# About this guide

I want this guide to be simple and easy to follow, so I'll basically outline the steps I took to get this to work on my machine. This hopefully will save you a few hours of researching on your own.

With that in mind this is a guide for building your [APK](https://www.google.bg/search?q=apk+file) file using **Python 3** code. The Python 2.7 process is not very different, and is more extensively documented, so we will not cover it.

To make your Python app run on Android we will make use of a library called [Kivy](https://kivy.org/). An awesome guide on Kivy can be found [here](https://www.youtube.com/watch?v=B79miUFD_ss). Another nice thing about Kivy is that it's cross platform, and the same Python/Kivy code you create once should run in platforms other than Android.

*Want to just quickly test this guide?* I've included a copy of my Python/Kivy code in this repo's "main" folder. It's heavily commented and you are welcome to use it. Once you see how this works, you can start building your own apps.

The final apk is also included as [Simon.apk]().

## Getting Started

Once you have your Python/Kivy code ready, the packaging process will takes 4 easy steps, although your computer may need a little time to finish 3 of them. Don't worry though, you will only have to do the slow steps once!

The steps are:

* Setup some virtual machine on your computer. (Easy, but may take a while to download)
* Update/add some components (Easy, but may take a while to download/unpack)
* Setup the packager configuration (Easy, and fast)
* Run the packager (Easy, but may take a while to package the first time)

### **STEP 1:** Setting up the virtual machine

Head over to [Oracle VirtualBox](https://www.virtualbox.org/), find the proper version for your system and install it. 

On Kivy's [Download](https://kivy.org/#download) page, download the "Virtual Machine (for Android/buildozer)".

Run the downloaded file on your Oracle VirtualBox. If you are asked about the system, let it know it's Linux-Ubuntu. Also, don't give too little RAM or CPU when setting up your machine, or things may start taking longer.

Fire it up and let the system boot.

When the system has booted, we will need to setup some "Shared Folders" between your virtual machine and actual machine. To do this, on top of your running virtual machine screen go to Devices > Shared Folders, click on the folder+ icon on the top right side of newly opened window. Select the folder you wish to use and mark the checkboxes "Auto-mount" and "Make Permanent". 

Reboot your virtual machine.

### **STEP 2:** Updating components

So your virtual machine is ready, let's now make sure Buildozer is up to date. Buildozer is the tool that will make this whole process easy. To make sure you have the latest version just open a terminal window and run:

```
sudo pip install -U buildozer
```

After that, let's make it possible for buildozer to work with Python 3. For that let's download the dependency called CrystaX from their [Download](https://www.crystax.net/en/download) page. I got the (latest) version 10.3.2 for linux x86_64 because my system is 64bits. [Find out about your system](https://www.google.bg/search?q=how+to+know+if+my+system+is+32+or+64+bit) and get the x86 if it's 32bits. Save your file on the Desktop.

When your file has finished downloading, right click > extract here. After it's done extracting, rename the newly created folder to crystax.

### **STEP 3:** Setup your packager configuration file

Now we are almost ready to create our apk. Go ahead and create a folder called "simon" on your desktop.

Now let's get the code inside this folder. To do that we will need to use that "Shared Folder" that we created when setting up the virtual machine (it's not possible to simply drag and drop into a virtual machine). 

So go ahead and put your "main.py" and "simongame.kv" inside your designated shared folder on your main machine. On your virtual machine, double click the "File System" icon that you have on your Desktop, and in the new window under "Devices" click on your sf_shared folder. Copy and paste your code files into the "Desktop/simon" folder.

Open a terminal window and 
```
cd ~/Desktop/simon
buildozer init
ls
```

You should now have a buildozer.spec file on your folder. You should edit that folder and make sure that the following settings are as follows:
```
requirements = python3crystax,kivy
```
```
android.ndk_path = /home/kivy/Desktop/crystax
```
*(See tips at the end of file)*

### **Final step**

Everything up to here you only needed to do this once. Congratz! From here on now, to build your apps, you only need to the following:

On that same buildozer.spec file, give your app a title, package.name, and package.domain. *(See tips at the end of file)*

After that run:

```
buildozer -v android debug deploy run logcat
```

Wait for it to package and your apk will be in the simon/bin folder.

### **Run on your device**

Download/transfer your apk into your Android device and open it. Make sure to check the box "Unknown sources" in your general "Settings > Security" before installing, but uncheck it as soon as the installation is over.
Have Fun! :)

## Personal tips for avoiding errors and issues

* Avoid special characters on your .spec file. I keep it alphanumeric for sanity.
* If you are trying to build inside the shared folder and having errors, try building it elsewhere.
* If you used extra libraries in your code, you may new to include them in the requirements on your .spec file
* You can handle some errors by cleaning the cache on your app's folder by running:
```
rm -rf .buildozer/android/app
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details