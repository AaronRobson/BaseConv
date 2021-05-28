#!/usr/bin/python

from string import ascii_letters, digits
import tkinter as tk

import baseconv

VALIDATION_CHOICE = 'all'
JUSTIFY_ENTRY = tk.RIGHT


def on_validate_given(to_validate, allowed_chars):
    return all(char in allowed_chars for char in to_validate)


class GUI(tk.Tk):

    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.title('BaseConv')

        self.resizable(width=True, height=False)

        # always on top (might be windows only)
        self.wm_attributes('-topmost', 1)

        format_tuple = ('%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        v_num_lett = (self.register(self.on_validate_number_letter),) + format_tuple
        v_num = (self.register(self.on_validate_number),) + format_tuple
        v_read_only = (self.register(self.on_validate_read_only),) + format_tuple

        self.v_in_num = tk.StringVar()

        tk.Label(self, text='Input Number').pack(anchor=tk.W)
        edt_in_num = tk.Entry(
            self,
            justify=JUSTIFY_ENTRY,
            textvariable=self.v_in_num,
            validate=VALIDATION_CHOICE,
            validatecommand=v_num_lett)
        edt_in_num.pack(fill=tk.X)
        edt_in_num.focus_set()

        self.v_in_base = tk.IntVar()
        self.v_in_base.set(baseconv.DEFAULT_BASE)

        tk.Label(self, text='Input Base').pack(anchor=tk.W)
        tk.Entry(
            self,
            justify=JUSTIFY_ENTRY,
            textvariable=self.v_in_base,
            validate=VALIDATION_CHOICE,
            validatecommand=v_num).pack(fill=tk.X)

        self.v_out_base = tk.IntVar()
        self.v_out_base.set(baseconv.DEFAULT_BASE)

        tk.Label(self, text='Output Base').pack(anchor=tk.W)
        tk.Entry(
            self,
            justify=JUSTIFY_ENTRY,
            textvariable=self.v_out_base,
            validate=VALIDATION_CHOICE,
            validatecommand=v_num).pack(fill=tk.X)

        f_cont = tk.Frame(self)
        tk.Button(
            f_cont,
            text='Calculate',
            command=self.calculate,
            underline=1).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        tk.Button(
            f_cont,
            text='Swap Bases',
            command=self.swap,
            underline=0).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        tk.Button(
            f_cont,
            text='Copy',
            command=self.copy,
            underline=0).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        f_cont.pack(fill=tk.X)

        self.v_out_num = tk.StringVar()

        tk.Label(self, text='Output Number').pack(anchor=tk.W)
        self.edt_out_num = tk.Entry(
            self,
            justify=JUSTIFY_ENTRY,
            textvariable=self.v_out_num,
            validate=VALIDATION_CHOICE,
            validatecommand=v_read_only)
        self.edt_out_num.pack(fill=tk.X)

        self.bind('<Return>', self.calculate)

        self.bind('<Shift-KeyRelease-Escape>', self.cancel_escape_event)
        self.bind('<KeyRelease-Escape>', self.escape_event)

        self.bind('<Alt-a>', self.calculate)
        self.bind('<Alt-s>', self.swap)
        self.bind('<Alt-c>', self.copy)

        # in case the caps lock is on (yes silly it works like this)
        self.bind('<Alt-A>', self.calculate)
        self.bind('<Alt-S>', self.swap)
        self.bind('<Alt-C>', self.copy)

        # draw all the controls like "Application.ProcessMessages" in delphi
        self.update_idletasks()
        # then set the newly generated window as the minimum size of the window
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def cancel_escape_event(self, event=None):
        pass

    def escape_event(self, event=None):
        self.destroy()

    def on_validate_number_letter(self, d, i, p_upper, s, s_upper, v, v_upper, w_upper):
        '''Valid percent substitutions (from the Tk entry man page)
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
        print('P=%r' % (p_upper))
        print('s=%r' % (s))
        print('S=%r' % (s_upper))
        print('v=%r' % (v))
        print('V=%r' % (v_upper))
        print('W=%r' % (w_upper))
        """
        return on_validate_given(p_upper, digits+ascii_letters)

    def on_validate_number(self, d, i, p_upper, s, s_upper, v, v_upper, w_upper):
        return on_validate_given(p_upper, digits)

    def on_validate_read_only(self, d, i, p_upper, s, s_upper, v, v_upper, w_upper):
        '''Regardless of input allow no user changes.
        '''
        return False

    def calculate(self, event=None):
        try:
            result = baseconv.bas_calc(
                self.v_in_num.get(),
                self.v_in_base.get(),
                self.v_out_base.get())
        except (baseconv.BaseConvError) as e:
            result = e
            print(result)
        else:
            # uses "result" variable instead of "v_out_num" tk variable as
            # otherwise this line would be temporally coupled to the setting
            # of that control's value, making coding awkward.
            print('%r in base %r = %r in base %r' % (self.v_in_num.get(),
                                                     self.v_in_base.get(),
                                                     result,
                                                     self.v_out_base.get()))

        self.v_out_num.set(result)

        # Telling it to validate again as programatically filling the box with
        # text means validation gets turned off which is used to
        # make it readonly.
        # http://coding.derkeiler.com/Archive/Tcl/comp.lang.tcl/2003-11/0618.html
        self.edt_out_num.config(validate=VALIDATION_CHOICE)

    def swap(self, event=None):
        v_in, v_out = self.v_in_base.get(), self.v_out_base.get()

        self.v_in_base.set(v_out)
        self.v_out_base.set(v_in)

    def copy(self, event=None):
        self.clipboard_clear()
        self.clipboard_append(self.v_out_num.get())


if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
