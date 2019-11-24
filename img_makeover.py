
# Standard libraries
from os import chdir
from glob import glob
from copy import deepcopy
from tkinter import Tk, Button, Label, Entry, Checkbutton, StringVar, IntVar, W, E, NORMAL, DISABLED
from tkinter.filedialog import askdirectory
from os.path import splitext

# 3rd-party libraries
import numpy as np
from PIL import Image

# Local libraries
from gentools import scale, rgb_to_hsl, hsl_to_rgb, HOLDER_PATH


class NamingWindow:
    def __init__(self, master):
        # Widgets
        self.master = master
        self.preStr = StringVar()
        self.sufStr = StringVar()
        self.sufStr.set("_rescaled")
        self.preLabel = Label(master, text="Prefix:")
        self.sufLabel = Label(master, text="Suffix:")
        self.preEntry = Entry(master, textvariable=self.preStr, width=70)
        self.sufEntry = Entry(master, textvariable=self.sufStr, width=70)
        self.xTLLabel = Label(master, text="xTL-crop (%):")
        self.yTLLabel = Label(master, text="yTL-crop (%):")
        self.xTRLabel = Label(master, text="xTR-crop (%):")
        self.yTRLabel = Label(master, text="yTR-crop (%):")
        self.xBLLabel = Label(master, text="xBL-crop (%):")
        self.yBLLabel = Label(master, text="yBL-crop (%):")
        self.xBRLabel = Label(master, text="xBR-crop (%):")
        self.yBRLabel = Label(master, text="yBR-crop (%):")
        self.lLabel = Label(master, text="L-crop (%):")
        self.tLabel = Label(master, text="T-crop (%):")
        self.rLabel = Label(master, text="R-crop (%):")
        self.bLabel = Label(master, text="B-crop (%):")
        self.xCropTL = StringVar()
        self.yCropTL = StringVar()
        self.xCropTR = StringVar()
        self.yCropTR = StringVar()
        self.xCropBL = StringVar()
        self.yCropBL = StringVar()
        self.xCropBR = StringVar()
        self.yCropBR = StringVar()
        self.lCrop = StringVar()
        self.tCrop = StringVar()
        self.rCrop = StringVar()
        self.bCrop = StringVar()
        self.xCropTL.set('0')
        self.yCropTL.set('0')
        self.xCropTR.set('0')
        self.yCropTR.set('0')
        self.xCropBL.set('0')
        self.yCropBL.set('0')
        self.xCropBR.set('25')
        self.yCropBR.set('20')
        self.lCrop.set('0')
        self.tCrop.set('0')
        self.rCrop.set('0')
        self.bCrop.set('0')
        self.xEntryTL = Entry(master, textvariable=self.xCropTL, width=3)
        self.yEntryTL = Entry(master, textvariable=self.yCropTL, width=3)
        self.xEntryTR = Entry(master, textvariable=self.xCropTR, width=3)
        self.yEntryTR = Entry(master, textvariable=self.yCropTR, width=3)
        self.xEntryBL = Entry(master, textvariable=self.xCropBL, width=3)
        self.yEntryBL = Entry(master, textvariable=self.yCropBL, width=3)
        self.xEntryBR = Entry(master, textvariable=self.xCropBR, width=3)
        self.yEntryBR = Entry(master, textvariable=self.yCropBR, width=3)
        self.lEntry = Entry(master, textvariable=self.lCrop, width=3)
        self.tEntry = Entry(master, textvariable=self.tCrop, width=3)
        self.rEntry = Entry(master, textvariable=self.rCrop, width=3)
        self.bEntry = Entry(master, textvariable=self.bCrop, width=3)
        self.satToggle = IntVar()
        self.satToggle.set(1)
        self.satCheckbutton = Checkbutton(master, text="Saturation", command=self.check_lock, variable=self.satToggle)
        self.ligToggle = IntVar()
        self.ligToggle.set(1)
        self.ligCheckbutton = Checkbutton(master, text="Lightness", command=self.check_lock, variable=self.ligToggle)
        self.okButton = Button(master, text="OK", command=self.master.destroy)

        # Layout
        self.preLabel.grid()
        self.sufLabel.grid()
        self.preEntry.grid(row=0, column=1, columnspan=5)
        self.sufEntry.grid(row=1, column=1, columnspan=5)

        e = E
        w = W
        self.xTLLabel.grid(row=2, column=0, stick=e)
        self.xEntryTL.grid(row=2, column=1, stick=w)
        self.yTLLabel.grid(row=3, column=0, stick=e)
        self.yEntryTL.grid(row=3, column=1, stick=w)
        self.xTRLabel.grid(row=2, column=4, stick=e)
        self.xEntryTR.grid(row=2, column=5, stick=w)
        self.yTRLabel.grid(row=3, column=4, stick=e)
        self.yEntryTR.grid(row=3, column=5, stick=w)
        self.xBLLabel.grid(row=5, column=0, stick=e)
        self.xEntryBL.grid(row=5, column=1, stick=w)
        self.yBLLabel.grid(row=6, column=0, stick=e)
        self.yEntryBL.grid(row=6, column=1, stick=w)
        self.xBRLabel.grid(row=5, column=4, stick=e)
        self.xEntryBR.grid(row=5, column=5, stick=w)
        self.yBRLabel.grid(row=6, column=4, stick=e)
        self.yEntryBR.grid(row=6, column=5, stick=w)

        self.lLabel.grid(row=4, column=0)
        self.lEntry.grid(row=4, column=1, stick=w)
        self.tLabel.grid(row=2, column=2, stick=e)
        self.tEntry.grid(row=2, column=3, stick=w)
        self.rLabel.grid(row=4, column=4, stick=e)
        self.rEntry.grid(row=4, column=5, stick=w)
        self.bLabel.grid(row=6, column=2, stick=e)
        self.bEntry.grid(row=6, column=3, stick=w)

        self.satCheckbutton.grid()
        self.ligCheckbutton.grid()
        self.okButton.grid(columnspan=6)

    def check_lock(self):
        """Locks the OK button if neither channel checkbutton is on."""
        if self.satToggle.get() or self.ligToggle.get():
            self.okButton['state'] = NORMAL
        else:
            self.okButton['state'] = DISABLED


def expand_lightness_chroma():
    """Maximizes the lightness and chroma for a batch of image files."""

    # Prompt with dialog box for modifying prefix & suffix
    master = Tk()
    nw = NamingWindow(master)
    master.wait_window(master)

    # Pull values from closed dialog
    prefix = nw.preStr.get()
    suffix = nw.sufStr.get()
    xtl = int(nw.xCropTL.get())/100
    ytl = int(nw.yCropTL.get())/100
    xtr = 1 - int(nw.xCropTR.get())/100
    ytr = int(nw.yCropTR.get())/100
    xbl = int(nw.xCropBL.get())/100
    ybl = 1 - int(nw.yCropBL.get())/100
    xbr = 1 - int(nw.xCropBR.get())/100
    ybr = 1 - int(nw.yCropBR.get())/100
    l = int(nw.lCrop.get())/100
    t = int(nw.tCrop.get())/100
    r = 1 - int(nw.rCrop.get())/100
    b = 1 - int(nw.bCrop.get())/100
    satBool = nw.satToggle.get()
    ligBool = nw.ligToggle.get()

    # TODO Figure out why askdirectory must come AFTER the tkinter dialog and how to fix it

    # Prompt user to select input & output directories
    jpgPath = askdirectory(title="Select directory of JPGs to adjust.", initialdir=HOLDER_PATH) + '\\'
    chdir(jpgPath)
    jpgList = glob('*.jpg')
    outPath = askdirectory(title="Select directory whither to export adjusted images.", initialdir=HOLDER_PATH) + '\\'

    for e in jpgList:
        print(f"Rescaling {e}. . .")
        fn, ext = splitext(e)
        im = np.array(Image.open(e))
        hsl = rgb_to_hsl(im)
        h = im.shape[0]
        w = im.shape[1]
        if satBool:
            sat = deepcopy(hsl[:,:,1])
            sat[:int(ytl*h), :int(xtl*w)] = np.nan
            sat[:int(ytr*h), int(xtr*w):] = np.nan
            sat[int(ybl*h):, :int(xbl*w)] = np.nan
            sat[int(ybr*h):, int(xbr*w):] = np.nan
            sat[:int(t*h), :] = np.nan
            sat[int(b*h):, :] = np.nan
            sat[:, :int(l*w)] = np.nan
            sat[:, int(r*w):] = np.nan
            hsl[:,:,1] = scale(hsl[:,:,1], optIMin=np.nanmin(sat), optIMax=np.nanmax(sat))
        if ligBool:
            lig = deepcopy(hsl[:,:,2])
            lig[:int(ytl*h), :int(xtl*w)] = np.nan
            lig[:int(ytr*h), int(xtr*w):] = np.nan
            lig[int(ybl*h):, :int(xbl*w)] = np.nan
            lig[int(ybr*h):, int(xbr*w):] = np.nan
            lig[:int(t*h), :] = np.nan
            lig[int(b*h):, :] = np.nan
            lig[:, :int(l*w)] = np.nan
            lig[:, int(r*w):] = np.nan
            hsl[:,:,2] = scale(hsl[:,:,2], optIMin=np.nanmin(lig), optIMax=np.nanmax(lig))
        im = hsl_to_rgb(hsl)
        im = Image.fromarray(im)
        im.save(outPath + prefix + fn + suffix + ext)

if __name__ == '__main__':
    expand_lightness_chroma()

# TODO Provide scaling levels feedback and manual control to even out images that scale different amounts
# TODO Provide thresholds option to supersaturate SL dimensions.
