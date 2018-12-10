#!/usr/bin/python

from string import ascii_letters, digits

try:
    import tkinter as tk
except:
    import Tkinter as tk

import baseconv

VALIDATION_CHOICE = 'all'
JUSTIFY_ENTRY = tk.RIGHT

def OnValidateGiven(toValidate, allowedChars):
    return all(char in allowedChars for char in toValidate)

class GUI(tk.Tk):
    def __init__(self, parent=None):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.title('BaseConv')

        self.resizable(width=True, height=False)

        #always on top (might be windows only)
        self.wm_attributes('-topmost', 1)
        
        formatTuple = ('%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        #vNumLett = (self.register(self.OnValidateNumberLetter), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        vNumLett = (self.register(self.OnValidateNumberLetter),) + formatTuple
        vNum = (self.register(self.OnValidateNumber),) + formatTuple
        vReadOnly = (self.register(self.OnValidateReadOnly),) + formatTuple

        self.vInNum = tk.StringVar()

        tk.Label(self, text='Input Number').pack(anchor=tk.W)
        edtInNum = tk.Entry(self, justify=JUSTIFY_ENTRY, textvariable=self.vInNum, validate=VALIDATION_CHOICE, validatecommand=vNumLett)
        edtInNum.pack(fill=tk.X)
        #set this control to be the one in focus on startup
        edtInNum.focus_set()

        self.vInBase = tk.IntVar()
        self.vInBase.set(baseconv.DEFAULT_BASE)
        
        tk.Label(self, text='Input Base').pack(anchor=tk.W)
        tk.Entry(self, justify=JUSTIFY_ENTRY, textvariable=self.vInBase, validate=VALIDATION_CHOICE, validatecommand=vNum).pack(fill=tk.X)

        self.vOutBase = tk.IntVar()
        self.vOutBase.set(baseconv.DEFAULT_BASE)

        tk.Label(self, text='Output Base').pack(anchor=tk.W)
        tk.Entry(self, justify=JUSTIFY_ENTRY, textvariable=self.vOutBase, validate=VALIDATION_CHOICE, validatecommand=vNum).pack(fill=tk.X)

        fCont = tk.Frame(self)
        tk.Button(fCont, text='Calculate', command=self.Calculate, underline=1).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        tk.Button(fCont, text='Swap Bases', command=self.Swap, underline=0).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        tk.Button(fCont, text='Copy', command=self.Copy, underline=0).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        fCont.pack(fill=tk.X)

        self.vOutNum = tk.StringVar()

        tk.Label(self, text='Output Number').pack(anchor=tk.W)
        self.edtOutNum = tk.Entry(self, justify=JUSTIFY_ENTRY, textvariable=self.vOutNum, validate=VALIDATION_CHOICE, validatecommand=vReadOnly)
        self.edtOutNum.pack(fill=tk.X)

        self.bind('<Return>', self.Calculate)

        self.bind('<Shift-KeyRelease-Escape>', self.CancelEscapeEvent)
        self.bind('<KeyRelease-Escape>', self.EscapeEvent)

        self.bind('<Alt-a>', self.Calculate)
        self.bind('<Alt-s>', self.Swap)
        self.bind('<Alt-c>', self.Copy)
        
        #in case the caps lock is on (yes silly it works like this)
        self.bind('<Alt-A>', self.Calculate)
        self.bind('<Alt-S>', self.Swap)
        self.bind('<Alt-C>', self.Copy)

        #draw all the controls like "Application.ProcessMessages" in delphi
        self.update_idletasks()
        #then set the newly generated window as the minimum size of the window
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def CancelEscapeEvent(self, event=None):
        pass
        
    def EscapeEvent(self, event=None):
        self.destroy()

    def OnValidateNumberLetter(self, d, i, P, s, S, v, V, W):
        '''From: http://stackoverflow.com/questions/4140437/python-tkinter-interactively-validating-entry-widget-content
        
        Valid percent substitutions (from the Tk entry man page)
        %d = Type of action (1=insert, 0=delete, -1 for others)
        %i = index of char string to be inserted/deleted, or -1
        %P = value of the entry if the edit is allowed
        %s = value of entry prior to editing
        %S = the text string being inserted or deleted, if any
        %v = the type of validation that is currently set
        %V = the type of validation that triggered the callback
        (key, focusin, focusout, forced)
        %W = the tk name of the widget
        '''
        """
        print('OnValidate:')
        print('d=%r' % (d))
        print('i=%r' % (i))
        print('P=%r' % (P))
        print('s=%r' % (s))
        print('S=%r' % (S))
        print('v=%r' % (v))
        print('V=%r' % (V))
        print('W=%r' % (W))
        """

        return OnValidateGiven(P, digits+ascii_letters)

    def OnValidateNumber(self, d, i, P, s, S, v, V, W):
        return OnValidateGiven(P, digits)

    def OnValidateReadOnly(self, d, i, P, s, S, v, V, W):
        '''Regardless of input allow no user changes.
        '''
        return False

    def Calculate(self, event=None):
        try:
            result = baseconv.BasCalc(self.vInNum.get(), self.vInBase.get(), self.vOutBase.get())
        except (baseconv.BaseConvError) as e:
            result = e
            print(result)
        else:
            #uses "result" variable instead of "vOutNum" tk variable as otherwise this line would be temporally coupled to the setting of that control's value, making coding awkward.
            print('%r in base %r = %r in base %r' % (self.vInNum.get(), self.vInBase.get(), result, self.vOutBase.get()))

        self.vOutNum.set(result)

        #Telling it to validate again as programatically filling the box with text means validation gets turned off which is used to make it readonly.
        #http://coding.derkeiler.com/Archive/Tcl/comp.lang.tcl/2003-11/0618.html
        self.edtOutNum.config(validate=VALIDATION_CHOICE)

    def Swap(self, event=None):
        vIn, vOut = self.vInBase.get(), self.vOutBase.get()

        self.vInBase.set(vOut)
        self.vOutBase.set(vIn)

    def Copy(self, event=None):
        self.clipboard_clear()
        self.clipboard_append(self.vOutNum.get())

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
