#Coding:utf-8
# Todo: setup, actual help docs
#sorted(list(set(dir())-{'Tk','Toplevel','Button','Checkbutton','Entry','Frame','Label','LabelFrame','Menu','Scrollbar','Spinbox','Text','BooleanVar','IntVar','StringVar','Variable','Pack','Grid','Place','PhotoImage','_QueryDialog','font','sub','_QuerySave','asksavenocancel','FullText','ToggleButton','ButtonMenu','OptionMenu','LabelOption','EntryOption','SpinboxOption','popup','locale','actions','events','keys','__annotations__','__builtins__','__doc__','__file__','__loader__','__name__','__package__','__spec__'}))
'''
Design philosophy of FixNotepad:

Don't make things leaky!
Hide everything in local variables of a single function _ui_make_<something>.
Only unless you need to provide it to something else

For example, in FixNotepad itself only following are available in global space:
UI elements (tk, TOPBAR, text, STATUSBAR), menus (MENU, FILE, EDIT, VIEW, HELP), locale (actions, keys, locale, images),
tkinter (tkinter, tkinter.font, tkinter.filedialog, tkinter.simpledialog), sys.platform (platform),
custom widgets (FullText, ToggleButton, OptionMenu, ButtonOption, LabelOption, EntryOption, SpinboxOption)
'''
import tkinter
import tkinter.font
import tkinter.filedialog
from tkinter.simpledialog import _QueryDialog
import language as locale
from sys import platform
if platform=='darwin':
    actions={
        'new':'⌘N',
        'open':'⌘O',
        'save':'⌘S',
        'saveas':'⌘⇧S',
        'export':'',
        'settings':'⌘,',
        'help':'⌘?',
        'license':'',
        'about':'',
        'exit':'⌘W',
        'undo':'⌘Z',
        'redo':'⌘⇧Z',
        'cut':'⌘X',
        'copy':'⌘C',
        'paste':'⌘V',
        'replace':'⌥⌘F',
        'symbol':'',
        'case':'',
        'delete':'⌫',
        'select':'⌘A',
        'font':'⌘T'
        }
    keys={
        'new':['<Command-n>','<Command-N>'],
        'open':['<Command-o>','<Command-O>'],
        'save':['<Command-s>','<Command-S>'],
        'saveas':['<Command-Shift-S>','<Command-Shift-s>'],
        'export':[],
        'settings':[],
        'help':['<Command-question>','<Command-Shift-question>'],
        'license':[],
        'about':[],
        'exit':['<Command-w>','<Command-W>'],
        'undo':['<Command-z>','<Command-Z>'],
        'redo':['<Command-y>','<Command-Y>'],
        'cut':[],
        'copy':[],
        'paste':[],
        'replace':['<Option-Command-f>','<Option-Command-f>'],
        'symbol':[],
        'case':[],
        'delete':[],
        'select':[],
        'font':['<Command-t>','<Command-T>'],
        }
    events={
        'cut':'<Command-x>',
        'copy':'<Command-c>',
        'paste':'<Command-v>',
        'delete':'<KeyPress-Backspace>',
        'select':'<Command-a>'
        }
else:
    actions={
        'new':'(Ctrl+N)',
        'open':'(Ctrl+O)',
        'save':'(Сtrl+S)',
        'saveas':'(Сtrl+Shift+S)',
        'export':'',
        'settings':'',
        'help':'(F1)',
        'license':'',
        'about':'',
        'exit':'(Alt+F4)',
        'undo':'(Ctrl+Z)',
        'redo':'(Ctrl+Y)',
        'cut':'(Ctrl+X)',
        'copy':'(Ctrl+C)',
        'paste':'(Ctrl+V)',
        'replace':'(Ctrl+H)',
        'symbol':'',
        'case':'',
        'delete':'(Del)',
        'select':'(Ctrl+A)',
        'font':'',
        }
    keys={
        'new':['<Control-n>','<Control-N>'],
        'open':['<Control-o>','<Control-O>'],
        'save':['<Control-s>','<Control-S>'],
        'saveas':['<Control-Shift-S>','<Control-Shift-s>'],
        'export':[],
        'settings':[],
        'help':['<F1>'],
        'license':[],
        'about':[],
        'exit':[],
        'undo':['<Control-z>','<Control-Z>'],
        'redo':['<Control-y>','<Control-Y>'],
        'cut':[],
        'copy':[],
        'paste':[],
        'replace':['<Control-h>','<Control-H>'],
        'symbol':[],
        'case':[],
        'delete':[],
        'select':[],
        'font':[],
        }
    events={
        'cut':'<Control-x>',
        'copy':'<Control-c>',
        'paste':'<Control-v>',
        'delete':'<KeyPress-Delete>',
        'select':'<Control-a>',
        }
class FullText(tkinter.Text):#2-way scrolling
    def __init__(self, master=None, **kw):
        self.frame=tkinter.Frame(master);self.vbar=tkinter.Scrollbar(self.frame);self.vbar.pack(side='right',fill='y');kw.update({'yscrollcommand':self.vbar.set})
        self.hbar=tkinter.Scrollbar(self.frame,orient='horizontal');self.hbar.pack(side='bottom',fill='x');kw.update({'xscrollcommand':self.hbar.set})
        tkinter.Text.__init__(self,self.frame,**kw);self.pack(side='left',fill='both',expand=True);self.vbar['command']=self.yview;self.hbar['command']=self.xview
        text_meths=vars(tkinter.Text).keys();methods=vars(tkinter.Pack).keys()|vars(tkinter.Grid).keys()|vars(tkinter.Place).keys();methods=methods.difference(text_meths)
        for m in methods:setattr(self,m,getattr(self.frame,m))if m[0]!='_'and m not in['config','configure']else None
    def __str__(self):return str(self.frame)
class _QuerySave(_QueryDialog):
    def body(self, master):tkinter.Label(master, text=self.prompt, justify='left').grid(row=0, padx=5, columnspan=3,sticky='we')
    def buttonbox(self):
        box = tkinter.Frame(self)
        self.initial_focus=b1=tkinter.Button(box, text='Save',command=lambda*e:(self.setresult(True),self.ok()))
        b1.grid(row=1,column=0,padx=5);b1.bind('<Return>',b1['command'])
        b2 = tkinter.Button(box, text='Don\'t save',command=lambda:(self.setresult(False),self.ok()))
        b2.grid(row=1, column=1, padx=5);b2.bind('<Return>',b2['command'])
        b3 = tkinter.Button(box, text='Cancel',command=lambda:(self.setresult(None),self.cancel()))
        b3.grid(row=1, column=2, padx=5);b3.bind('<Return>',b3['command'])
        self.bind("<Escape>", self.cancel)
        box.pack()
    def validate(self):return 1
    def setresult(self,result):self.result=result
def asksavenocancel(title, prompt, **kw):d = _QuerySave(title, prompt, **kw);return d.result
class ToggleButton(tkinter.Button):
    def __init__(self, master=None, value=False, **kw):
        kw['command']=self.flip
        kw['relief']='sunken'if value else'raised'
        tkinter.Button.__init__(self,master,**kw)
        self.value=tkinter.BooleanVar(self,value=value)
        self.get,self.set,self.trace_add=self.value.get,self.value.set,self.value.trace_add
    def flip(self):
        self.set(not self.get())
        self.config(relief='sunken'if self.get()else'raised')
class ButtonMenu(tkinter.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        '''ButtonMenu which opens a popup menu.'''
        cnf=cnf.copy()
        if'relief'not in cnf:cnf['relief']='flat'
        for i in 'text','image','compound','command','textvariable':
            if i in kw:cnf[i]=kw[i];del kw[i]
        label=None
        if'label'in kw:label=kw['label'];del kw['label']
        tkinter.Frame.__init__(self,master=master,**kw)
        if label:self.label=tkinter.Label(self,text=label);self.label.pack(side='left',fill='both',expand=True)
        if'textvariable'in cnf:self.value=cnf['textvariable']
        self.ui=self.ui_make(**cnf)
        self.button = tkinter.Button(self, text='▼',command=self.open,relief=cnf['relief']);self.button.pack(side='right',fill='both',expand=True)
        self.menu = tkinter.Menu(self,tearoff=0)
        for i in ['add_cascade', 'add_checkbutton', 'add_command', 'add_radiobutton', 'add_separator', 'insert_cascade', 'insert_checkbutton', 'insert_command', 'insert_radiobutton', 'insert_separator']:setattr(self,i,getattr(self.menu,i))
    def open(self):self.menu.tk_popup(self.winfo_rootx(),self.winfo_rooty())
    def ui_make(self,**kw):
        if'command'not in kw:kw['command']=self.open
        ui=tkinter.Button(self,**kw);ui.pack(side='left',pady=0,fill='both',expand=True);return ui
class OptionMenu(ButtonMenu):
    '''OptionMenu base class'''
    variable=tkinter.StringVar
    def __init__(self, master=None, values=None, default=None, cnf={}, **kw):
        kw['relief']='ridge';kw['border']=4
        ButtonMenu.__init__(self,master=master,cnf=cnf,textvariable=self.variable(),**kw)
        self.values=values;self.fill_menu()
        for i in ['trace','trace_add','trace_info','trace_remove','trace_variable','trace_vdelete','trace_vinfo','get','set']:setattr(self,i,getattr(self.value,i))
        self.trace_add('write',lambda*a:self.ui_update(self.get()))
        if default!=None:self.set(default)
    def ui_make(self,**kw):pass
    def ui_update(self,value,**kw):pass
    def fill_menu(self):
        for i in range(len(self.values)):self.menu.add_command(label=str(self.values[i]),command=(lambda e:lambda:self.set(self.values[e]))(i))
class LabelOption(OptionMenu):
    '''LabelOption which allows the user to select a value from a menu.'''
    def ui_make(self,**kw):ui=tkinter.Label(self,justify='right',**kw);ui.pack(side='left',pady=0,fill='x');return ui
    def ui_update(self,value):self.ui.config(text=str(value))
class EntryOption(OptionMenu):
    '''LabelOption which allows the user to select a value from a menu
or enter it manually.'''
    def ui_make(self,**kw):ui=tkinter.Entry(self,justify='right',**kw);ui.pack(side='left',pady=0,fill='x');ui.bind('<Key>',self.validate);return ui
    def ui_update(self,value):self.ui.delete(0,'end');self.ui.insert(0,str(value))
    def validate(self,key):
        if (key.keysym in['BackSpace','Delete','\x7f']):return ""
        if key.keysym=='Return':
            if(t:=self.ui.get())in self.values:self.set(t)
            else:self.ui.bell();self.ui.delete(0,'end');self.ui.insert(0,self.value.get());return"break"
class SpinboxOption(EntryOption):
    '''SpiboxOption which allows the user to select a value from a menu
and increment/decrement it'''
    def ui_make(self,**kw):ui=tkinter.Spinbox(self,justify='right',**kw);ui.pack(side='left',pady=0,fill='both');return ui
class _QueryOption(_QueryDialog):
    def body(self, master):
        dialog=LabelOption(master,label=self.prompt,values=self.initialvalue,default=self.minvalue);
        dialog.pack(fill='both',expand=True)
        dialog.trace_add('write',self.setresult)
        self.result=self.initialvalue
        return dialog
    def setresult(self,*a):
        self.result=self.initial_focus.get()
    def validate(self):return 1
def askoption(title, prompt, **kw):d = _QueryOption(title, prompt, **kw);return d.result
def popup(cls):
    class Popup(cls):
        def __init__(self,master,cnf={},**kw):
            from tkinter import Label as l
            self.master=master; self.tk=master.tk
            if 'popup_text'in kw and bool(kw['popup_text']):PT,PF=kw['popup_text'],(kw['popup_font']if'popup_font'in kw else None);self.__oops=0#Инициализация
            else:self.__oops=1
            if 'popup_text' in kw:del kw['popup_text']
            if 'popup_font' in kw:del kw['popup_font']
            super().__init__(master=master,cnf=cnf,**kw)
            while master.master:master=master.master #get the MOST master widget
            self.master=master
            if not self.__oops:
                self.POPUP=l(master,text=PT,font=PF);
            self.POPUP.bind('<Enter>',self.__OFF);self.POPUP.bind('<Motion>',self.__OFF)
            self.bind('<Enter>',self.__ON);self.bind('<Motion>',self.__ON);self.bind('<Leave>',self.__OFF)
        def config(self,**kw):
            if 'popup_text' in kw:self.POPUP.config(text=kw['popup_text']);del kw['popup_text']
            if 'popup_font' in kw:self.POPUP.config(font=kw['popup_font']);del kw['popup_font']
            super().config(**kw)
        configure=config
        def __ON(self,e):self.POPUP.place(x=self.winfo_x()+e.x+1,y=self.winfo_y()+e.y+1,anchor='nw');self.POPUP.lift()
        def __OFF(self,e):self.POPUP.place_forget()
    return Popup
##### GUI Window #################################################################
_on_exit=lambda:areyousure(lambda:(_new(),exit()),end=True)
tk=tkinter.Tk();tk.title(locale.title);tk.wm_protocol('WM_DELETE_WINDOW',_on_exit)
TOPBAR=tkinter.Frame(tk);TOPBAR.pack(fill='x',side='top')
text=FullText(tk,height=24);text.pack(fill='both',expand=True)
[text.bind(i,lambda*e:[warning.grid(row=1,column=0,columnspan=15),tk.after(5000,warning.grid_forget)])for i in['<Control-a>','<Control-A>','<Command-a>','<Command-A>']]
warning=tkinter.Label(TOPBAR,text=locale.warning)# Warn User of ctrl-a
def flip_panel(I):
    for i in Panels:i.grid_forget()
    Panels[I].grid(row=0,column=0,sticky='nsew')
MENU=tkinter.Menu(tk,tearoff=0);tk.config(menu=MENU)
REPLACE_PANEL,SYMBOL_PANEL=Panels=tkinter.Frame(TOPBAR,relief='groove',border=2),tkinter.Frame(TOPBAR,relief='groove',border=2)
STATUSBAR=tkinter.Frame(tk);STATUSBAR.pack(fill='x',expand=True)
STATUSBAR.c=tkinter.Label(STATUSBAR,text=locale.col%0);STATUSBAR.c.pack(side='right')
STATUSBAR.l=tkinter.Label(STATUSBAR,text=locale.line%1);STATUSBAR.l.pack(side='right')
######################################################################

##### Icons #################################################################
prefix=b'R0lGODlhEAAQAPcAAAAAAP///w'+b'A'*1015+b'CwAAAAAEAAQAAAI'
images={
    'undo':tkinter.PhotoImage(data=prefix+    b'QgADCBxIsKDBgwUBACCosGHChQIbSmQI0WFEhQMxWsyIMYBEiA8vdjTY8eNGjxVNgkSJkOTKlicRxuT4EWbNljgDAgA7'),
    'redo':tkinter.PhotoImage(data=prefix+    b'QgADCBxIsKDBgwgBKFRIkOHAhRAfApA4UeBCixUvNmTo0GFBiBkrGowYwGNJkB1FnkSJEeFIky5XxtwIMibLmTEDAgA7'),
    'new':tkinter.PhotoImage(data=prefix+     b'QgADCBxIsKBAAAgTKjQIwGCAhAUbMnwo8aBDiQgHViRYMePDiwoxOoxocaTGkiY/qkwpMqXKjSNbsjwYsqZHlwQDAgA7'),
    'open':tkinter.PhotoImage(data=prefix+    b'QgADCBxIsKDBgwgTEgTAsKFCAAsfLmxIcSBEiQIvUtzoUKNEiBcRegx5UCNJgyEZYgxwsiBJjhwVJgwIADs='),
    'save':tkinter.PhotoImage(data=prefix+    b'QgADCBxIsKBAAAgTKkRIMKHBgwAGOmwYceJEiRUZBrgIcaNGjhQjelxIUmTJkhBPKkyp8mNLiyNRmoxJciPLlg9zCgwIADs='),
    'saveas':tkinter.PhotoImage(data=prefix+  b'SAADCBxIsKBAAAgTKkRIMKHBgwAGOmwYceJEiRUZBrgIcaNGjhQjelxIUmTJhxkXSlx58iBLkiMZVowpciNLmitdtixYk2fJgAA7'),
    'settings':tkinter.PhotoImage(data=prefix+b'RwADCBwYAAAAgggNCjSosODBhQwdKmT4kKJFiwMvXkwYUeJDiB1BTqSI0ONGjhExZiS5siHLlhobmoxZMaVNmS47yiy5c2BAADs='),
    'help':tkinter.PhotoImage(data=prefix+    b'RgADCBQIoKDBgQgDHBy4kCGAhA4jKjRYkOBDhRYpVsS4caPFjBAlTgxJUaRDjyMTogSJcGXFiyEZfjTpsSZMlygbqtSYMCAAOw=='),
    'license':tkinter.PhotoImage(data=prefix+ b'TAADCBxIsKBAAAACJFw4EGFChQwZHkR4sKJEhRgzRmyo0WJGjA9DguQYcuNDiCVHnnRYUSXJlhs9drwoUSRNjQspsqyZs+dIg0AHBgQAOw=='),
    'about':tkinter.PhotoImage(data=prefix+   b'RgADCBQIoKDBgQgDHBy4kCGAhA4jKjRYkOBDhRYpVsS4caPFjBAlTgxJUaRDjyMTogSJcGXFiyEZfjTpsSZMlygbqtSYMCAAOw=='),
    'font':tkinter.PhotoImage(data=prefix+    b'OgADCBxIsOBAAAgTKkRYcKFDgwwbAoA4ESJFgxgDRMxI0GFFjB45buQocCRJkyI/nkxIUuPCljADBAQAOw=='),
    'cut':tkinter.PhotoImage(data=prefix+     b'RAADCBxIsGBBAAYRGgygkGDDgw8BPHQYcSJFgRIXDszI0CJEjhoxSvT4keTGkSApjhS5EuNGhy8ZxnRJs2HEmS1VCgwIADs='),
    'copy':tkinter.PhotoImage(data=prefix+    b'PwADCBxIsKBAAAgTAjA4cGHDAA4NRoR4kOFEhRYzSiSoMCHHjw8jXgTpsONFjxtTFpz4UCXIlRpXmkTIsKbAgAA7'),
    'paste':tkinter.PhotoImage(data=prefix+   b'RAADCBxIsKBAAAgTJjQYAGFDhw4NRhw4kaDCiwwvKsyoESNFjwcbftxIMeRDkgcXnlRZEEBKlBZfsowpMSPHjgxzCgwIADs='),
    'delete':tkinter.PhotoImage(data=prefix+  b'PwADCBxIsKBAAAAMEkR4kKFChAkbRlzocCBEihMxSlQo8SLHjh8tevwIcaRBjyZFZkyZMsDIlhtdZjw5M6TAgAA7'),
    'exit':tkinter.PhotoImage(data=prefix+    b'SAABCBxIsKDBgwcDKFzI0CDDhQIDOIQIQGLFiRIVVtRY8OFFjgQ9guzYsCFJjRlHRhwIUeVGkRZDPkzpkKVHmS0jxnxJ0SSAgAA7'),
    'wrap':tkinter.PhotoImage(data=prefix+    b'OgADCBxIsKDBgwIBIDQIQGGAhhAjKoSYUGLEhw0XFsyokaDDjiAXfgTJkWRGixcxTkTJsWTHkSFDBgQAOw'),
    'export':tkinter.PhotoImage(data=prefix+  b'RQADCBxIsKBAAAgTKgRQkKHBgQ4PPiQYMeLEABYvUjyoECJGiR8ZIsQokuPIkihBppSYUOPDjC9BanQI0yDNhThHuiwYEAA7'),
    'select':tkinter.PhotoImage(data=prefix+  b'QQADCBxIsGBBAAgFIgRgUGHCAAsbEnx4cGHCixYzYoSoMSNHjh0jYgy5kaRIhiZLpvyosSFFiRFBwnwYU6LNAAEBADs='),
    'replace':tkinter.PhotoImage(data=prefix+ b'RQADCBxIsCBBAAAGIkRoMABDgQsfKoRoUKJDigUlRrToMCHGjx05Nux40ONIhQszRkRZ8aJJkSBJNjSJcmVMiDZTnhwZEAA7'),
    'symbol':tkinter.PhotoImage(data=prefix+  b'RgADCBxIsCBBAAAMJlS4UOFBgQ0hSpy4sCJCixcTZiwYMaLBjyADaBQJMSNCiSMfPkw50ONIjAw3ljz5sWFFkBpNegw5MCAAOw=='),
    'case':tkinter.PhotoImage(data=prefix+    b'QwADCBxIsGBBAAYTCkSo8GAAhg0XPow4ECHEiBYJAth4ESLDjhVDGvTI8aLIiRIrckwp0iNLiSBRhiT5EuVKkxQDBAQAOw=='),
    }
del prefix
##### File operations #################################################################
attachedFile=None
def _new():
    global attachedFile
    if attachedFile:attachedFile.close();attachedFile=None
    _erase_history(all=True);text.delete(1.0,'end');tk.title(locale.title)
def _openfile():
    if name:=tkinter.filedialog.askopenfilename(defaultextension='txt',filetypes=((locale.types['txt'],'txt'),(locale.types['*'],'*'))):_open(name);_erase_history(all=True)
def _open(name):global attachedFile;attachedFile=open(name,'r');text.delete(1.0,'end');text.insert(0.0,attachedFile.read());tk.title('%s - [%s]'%(locale.title,name))
def areyousure(func,*,end=False):
    '''Calls <func> function.
If user has unsaved changes,
ask to save first.
If <end=True>, exit after saving (used internally)'''
    if len(undo_list)>1:
        if(a:=asksavenocancel(locale.misc['title'],((locale.misc['prompt-file']%attachedFile.name)if attachedFile else locale.misc['prompt']))):_savefile(end=end);func()
        elif a==False:func()
        elif a==None:return None
        else:raise RuntimeError('This cannot happen!')
    else:func()
def _savefile(*, saveas=False, format='txt', end=False):
    if attachedFile and not saveas:name=attachedFile.name;attachedFile.close();_save(name,end=end)
    elif name:=tkinter.filedialog.asksaveasfilename(defaultextension=format,filetypes=((locale.types[format],format),(locale.types['*'],'*'))):_save(name,format=format,end=end);_open(name)
def _save(name, *, format='txt', end=False):
    global attachedFile
    if format=='txt':content=text.get(1.0,'end')
    elif format=='html':content='<HTML><HEAD><TITLE>%s</TITLE></HEAD><BODY>%s</BODY></HTML>'%(locale.htmltitle,text.get(1.0,'end').replace('\n','<br />\n'))
    attachedFile=open(name,'w');attachedFile.write(content);attachedFile=attachedFile.close()
    if end:exit()
    else:_open(name)
##### Undo/Redo System #################################################################
undo_list=[];redo_list=[];modified=None
def _erase_history(all=False):
    global modified,countdown
    if all:undo_list.clear()
    undo_list.append(modified if modified else text.get(1.0,'end'));modified=None;redo_list.clear();countdown=None
def _shift(a,b):
    if a:b.append(text.get(1.0,'end'));text.replace(1.0,'end',a.pop(-1))
    else:tk.bell()
    return"break"
def flip_status():
    '''If you add anything to the STATUSBAR,
add a way to update it here'''
    lc=text.index('insert').split('.')
    STATUSBAR.l.config(text=locale.line%lc[0])
    STATUSBAR.c.config(text=locale.col%lc[1])
def _trace(event=None):
    global countdown,modified
    tk.after(1,flip_status)
    if(event.char in['\x18','\x16'])or(event.char and event.state==0)or(event==None):#(event.char in'\x18\x03\x16'):
        if countdown:tk.after_cancel(countdown)
        modified=text.get(1.0,'end');countdown=tk.after(1000,_erase_history)
undo,redo=lambda*e:_shift(undo_list,redo_list),lambda*e:_shift(redo_list,undo_list)
text.bind('<Key>',_trace)
about='\nv. 0.5.5 (beta)\n\nAntoniy Elias Sverdrup\n\n(c) Anthony&Co.Media Production, 2017-2024\n\n'
class _QueryFont(_QueryDialog):
    def body(self, master):
        class FontMenu(EntryOption):
            def __init__(self, master=None, label=' ', default=None,**kw):
                a=[i for i in tkinter.font.families()if not i.startswith('@')]
                for i in a:
                    for j in[' Baltic',' CYR',' Greek',' TUR',' Cyr']:
                        if(i+j)in a:del a[a.index(i+j)]
                EntryOption.__init__(self,master,sorted(a),default,cnf={'width':15},label=label)
                self.before(['Fixedsys','System','Symbol','Terminal','Webdings','Wingdings','Wingdings 2','Wingdings 3'])
                self.before(['Arial','Courier','Courier New','Helvetica','MS Sans Serif','Tahoma','Times','Times New Roman','Trebuchet MS','Verdana'])
            def ui_update(self,value):self.ui.config(width=len(value)+1);EntryOption.ui_update(self,value)
            def before(self,list):
                self.menu.insert_separator(0)
                for i in reversed(list):
                    if i in self.values:self.menu.insert_command(0,label=str(i),command=(lambda e:lambda:self.set(e))(i))
        class FontSizeMenu(SpinboxOption):
            variable=tkinter.IntVar
            def __init__(self, master=None, label=' ',values=None, default=None, cnf={'width':3},**kw):
                self.min,self.max=cnf['from'],cnf['to'];
                SpinboxOption.__init__(self,master,values,default,cnf=cnf,label=label,**kw)
                self.ui.bind('<Key>',self.validate)
            def validate(self,key):
                if (key.keysym in['BackSpace','Delete','\x7f']):return ""
                if self.ui.get()==''or(t:=int(self.ui.get()))<self.max:
                    if key.keysym=='Return' and self.min<t:self.set(t)
                    elif(key.keysym in list('0123456789')):return""
                    else:self.ui.bell();return"break"
                else:self.ui.bell();return"break"
                return""if(key.keysym in list('0123456789'))or(key.keysym in['Return','BackSpace','Delete','\x7f'])else"break"
            def plus(self):self.set(self.value.get()+1)if self.min<self.value.get()+1<self.max else None
            def minus(self):self.set(self.value.get()-1)if self.min<self.value.get()-1<self.max else None
        f='Courier';s=12;t=''
        from re import match
        if m:=match(r"({.+}|\w+) +(-?[0-9]+) *(.*)",self.prompt):f,s=m.group(1).strip("{}"),int(m.group(2));t=m.group(3)
        dialog=tkinter.LabelFrame(master,text=locale.font['font']);
        self.FONT=FontMenu(dialog,label=locale.font['font'],default=f)
        self.FONTSIZE=FontSizeMenu(dialog,None,[8,9,10,11,12,14,16,18,20,22,24,26,28,32,36,48,72],s,{'width':3,'from':8,'to':72})
        self.B=ToggleButton(dialog,text=locale.font['bold'],font=(None,12,'bold'),value='bold'in t);
        self.I=ToggleButton(dialog,text=locale.font['italic'],font=(None,12,'italic'),value='italic'in t);
        self.U=ToggleButton(dialog,text=locale.font['underline'],font=(None,12,'underline'),value='underline'in t);
        dialog.pack(fill='x',expand=True)
        for i in(self.FONT,self.FONTSIZE,self.B,self.I,self.U):
            i.pack(side='left',fill='both',expand=True)
            i.trace_add('write',self.setresult)
        test=tkinter.LabelFrame(master,text=locale.font['example']);
        self.TEST=tkinter.Label(test,text=locale.font['lorem'],font=(f,s,' '.join([i for i in['bold','italic','underline']if i in t])))
        self.TEST.pack(fill='both',expand=True)
        test.pack(fill='both',expand=True)
        self.result=None
        return self.FONT
    def setresult(self,*a):
        self.result=(self.FONT.get(),self.FONTSIZE.get(),' '.join([i for i in['bold'if self.B.get()else'normal','italic'if self.I.get()else'','underline'if self.U.get()else'']if i]))
        self.TEST.config(font=self.result)
    def validate(self):return 1
def askfont(title, prompt, **kw):d = _QueryFont(title, prompt, **kw);return d.result
def set_font(font=None):
    '''Set text font if <font> provided, otherwise ask user'''
    if not font:font=askfont(locale.font['font'],text['font'])
    if font:text.config(font=font,height=320//int(font[1]))
def Helper(text):
    '''Create a Toplevel with a scrollable Text which contains <text>.'''
    top=tkinter.Toplevel(tk);a=FullText(top);a.insert(0.0,text);a.pack(fill='both',expand=True)
    tkinter.Button(top,text=locale.misc['ok'],command=top.destroy).pack();top.title(locale.MENU['help'])
######################################################################

##### Menus #################################################################
def _make_ui_menus(name,funclist):
    '''
Fill menus and bind keys automatically from funclist (which is actually a dict)
using locale, actions and keys:

<key>:lambda*e:<func>()

    Adds "locale[key]%actions[key]" menu command that does <func> and binds keys[key] to it.

    Example: funclist={'copy':lambda*e:text.event_generate(events['copy'])} -> 

        locale['copy'] == 'Copy %s'
        actions['copy'] == '(Ctrl+C)'
        keys['copy'] == ['Control-c','Control-C']

    -> results in "Copy (Ctrl+C)" menu command, which executes text.event_generate(events['copy'])
    and key combination Control-c or Control-C (case insensitive), wich also executes text.event_generate(events['copy'])

<key>:None

    Adds separator. <key> can be any arbitrary value
'''
    menu=tkinter.Menu(tk,tearoff=0)
    for i in funclist:
        if funclist[i]:
            menu.add_command(label=locale.actions[i]+' '+actions[i],image=images[i],compound='left',command=funclist[i])
            for j in keys[i]:tk.bind_all(j,funclist[i])
        else:menu.add_separator()
    MENU.add_cascade(label=name,menu=menu)
    return menu
FILE=_make_ui_menus(locale.MENU['file'],
               {
                'new':lambda*e:areyousure(_new),
                'open':lambda*e:areyousure(_openfile),
                'save':lambda*e:_savefile(),
                'saveas':lambda*e:_savefile(saveas=True),
                'export':lambda:_savefile(format='html',saveas=True),
                '1':None,
                'settings':lambda:print(askoption('Параметры',{'text':'Язык','image':images['help']},initialvalue=['Русский','English'],minvalue=locale.language)),
                '2':None,
                'exit':_on_exit,
                })

EDIT=_make_ui_menus(locale.MENU['edit'],
               {
                'undo':undo,
                'redo':redo,
                '1':None,
                'cut':lambda*e:text.event_generate(events['cut']),
                'copy':lambda*e:text.event_generate(events['copy']),
                'paste':lambda*e:text.event_generate(events['paste']),
                'delete':lambda*e:text.event_generate(events['delete']),
                '2':None,
                '3':None,
                'select':lambda*e:text.event_generate(events['select']),
                })
def _make_ui_case():
    CASE=tkinter.Menu(tk,tearoff=0)
    def make_case(i):
        try:a=text.get('sel.first','sel.last');text.replace('sel.first','sel.last',[a.lower(),a.upper(),a.title(),a.capitalize(),a.swapcase()][i])
        except:a=text.get(1.0,'end');text.replace(1.0,'end',[a.lower(),a.upper(),a.title(),a.capitalize(),a.swapcase()][i])
    for(i,x)in zip(locale.case, range(5)):CASE.add_command(label=locale.case[i],command=(lambda e:lambda:make_case(e))(x))
    return CASE
EDIT.insert_cascade(8,label=locale.actions['case'],image=images['case'],compound='left',menu=_make_ui_case())
text.bind('<Button-2>',lambda e:EDIT.tk_popup(x=e.x,y=e.y));text.bind('<Button-3>',lambda e:EDIT.tk_popup(x=e.x,y=e.y))
VIEW=_make_ui_menus(locale.MENU['view'],
               {
                'replace':lambda*e:flip_panel(1),
                'symbol':lambda*e:flip_panel(0),
                '1':None,
                'font':lambda*e:set_font()
                })
VIEW.delete(0,1)
VIEW.p=tkinter.IntVar(value=0)
VIEW.insert_radiobutton(0,label=locale.actions['replace'],image=images['replace'],compound='left',value=0,variable=VIEW.p,command=lambda:flip_panel(0))
VIEW.insert_radiobutton(1,label=locale.actions['symbol'],image=images['symbol'],compound='left',value=1,variable=VIEW.p,command=lambda:flip_panel(1))
#VIEW.add_command(label=locale.font['font'],image=images['font'],compound='left',command=set_font)
WRAP=tkinter.Menu(tk,tearoff=0)
WRAP.p=tkinter.StringVar(value='char')
for i in locale.wrap:WRAP.add_radiobutton(label=locale.wrap[i],value=i,variable=WRAP.p,command=(lambda e:lambda:text.config(wrap=e))(i))
del i
VIEW.add_cascade(label=locale.font['wrap'],image=images['wrap'],compound='left',menu=WRAP)
HELP=_make_ui_menus(locale.MENU['help'],
               {
               'help':lambda*e:Helper(locale.help),
               '1':None,
               'license':lambda*e:Helper(locale.license),
               'about':lambda:Helper(locale.about%about),
                })
######################################################################

##### Insert box #################################################################
def _make_ui_sym(master, all):
    def flip_symmenu(I):
        for i in SymMenus:i.grid_forget()
        for i in SymButtons:i.config(relief='raised')
        SymMenus[I].grid(row=2,column=1,rowspan=3,columnspan=9,sticky='nsw')
        SymButtons[I].config(relief='sunken')
    def _make_ui_symbuttons(menu,symbols,letters=None):
        if not symbols:
            symbol=lambda*e:eval('"\\%s%s"'%(' xu'[len(a)//2],uni.get()))if((a:=CODE.get())and len(a)%2==0)else'' 
            tkinter.Label(menu,text=locale.symbol['unicode']).grid(row=0,column=0,columnspan=9,sticky='nsew');
            uni=tkinter.Entry(menu,width=6,textvariable=(CODE:=tkinter.StringVar()));uni.grid(row=1,column=0)
            uni.bind('<Key>',lambda e:(""if(e.keysym in list('0123456789ABCDEFabcdef')and len(uni.get())<4)or(e.keysym in['Return','BackSpace','Delete','\x7f','Up','Left','Right','Down'])else"break"));
            CODE.trace_add('write',lambda*e:preview.config(text=(a if(a:=symbol()).isprintable()else'\ufffd')))
            preview=tkinter.Label(menu,text='',relief='sunken');preview.grid(row=1,column=1,sticky='nsew')
            tkinter.Button(menu,text=locale.symbol['insert'],command=lambda:text.insert('insert',symbol())).grid(row=1,column=2,sticky='nsew')
        else:
            class CapsButton(tkinter.Button):
                def __init__(self, master, *, symbol, command, **kw):self.command=command;self.symbol=symbol;tkinter.Button.__init__(self, master=master,text=self.symbol,command=lambda:self.command(self.symbol),**kw)
                def swapcase(self):self.symbol=self.symbol.swapcase();self.config(text=self.symbol)
            x=1;y=0
            for i in (letters if letters else symbols):
                if i==' ':tkinter.Label(menu,text=' ').grid(row=y,column=x)
                elif i=='\n':x=0;y+=1
                elif i in symbols:tkinter.Button(menu,text=(('\u25cc%s'%i)if i in'\u0300\u0301\u0304\u0308'else i),command=(lambda s:lambda:text.insert('insert',s))(i)).grid(row=y,column=x,sticky='nsew')
                else:a=CapsButton(menu,symbol=(('\u25cc%s'%i)if i in'\u0300\u0301\u0304\u0308'else i),command=lambda s:text.insert('insert',s));a.grid(row=y,column=x,sticky='nsew');LetBut.append(a)
                x+=1
    def flip_caps():
        for i in LetBut:i.swapcase()
        caps['text']=caps['text'].swapcase()
    SymMenus=[tkinter.Frame(master)for i in range(len(all)+1)];SymButtons=[];LetBut=[]
    HoverButton=popup(tkinter.Button)
    for b,i in zip(all,range(len(all))):
        a=HoverButton(master,text=locale.symbol[b],command=(lambda i:lambda:flip_symmenu(i))(i),popup_text=locale.symbol_popup[b])
        SymButtons.append(a);a.grid(row=1,column=2+i,sticky='nsew')
        _make_ui_symbuttons(SymMenus[i],*all[b])
    flip_symmenu(1)
    tkinter.Button(master,text='Nbsp',command=lambda:text.insert('insert','\xa0')).grid(row=4,column=0,sticky='nsew')
    tkinter.Button(master,text='Tab',command=lambda:text.insert('insert','\t')).grid(row=2,column=0,sticky='nsew')
    caps=tkinter.Button(master,text='caps',command=flip_caps);caps.grid(row=3,column=0,sticky='nsew')
_make_ui_sym(SYMBOL_PANEL,
             {'SYM_UNICODE':(None,),
              'SYM_SYM':('§¡¿‽ «"» `´¨¯ ·×÷∞√ ¹²³\n¶-–— ‘\'’ \u0300\u0301\u0304\u0308 ≈≠≡≤≥ ¼½¾\n№©®™ °±¬ #¦ªº ∂∆∏∑∫',),
              'SYM_LAT':('ßıİ','ßàáâãäāăåąæĉċçčðèéêëēĕėęěƒʃ\nĝğġģǧžƕĥìíîĩïīĭįĵłñňŋȝɂʒþıİ\nòóôõöőōŏøœřśŝşšùúûũüűūŭůųýÿ'),
              'SYM_CYR':('','јџўүќқњѓґғђѕ\nѳыѵѧԥѫљћэєӭ\nӏѩѯїіѣѭәҗңһ',),
              'SYM_GREEK':('ςϐϑϒϕϖϱϵϰ',';ςερτυθιοπ   ϐϵϑϰϖϱϒϕϲ\nασδφγηξκλ΅΄  ϳϸϻϗϙϛϝϟϡ\n ζχψωβνμ',),
              'SYM_BLOCK':('─│┌┐└┘├┤┬┴┼ ╒╕╘╛╞╡╤╧╪ ░▒▓█\n═║╔╗╚╝╠╣╦╩╬ ╓╖╙╜╟╢╥╨╫ ▀▄▌▐ ',),
              'SYM_ARROW':(' ▲   ↑  ♠♣♥♦♪♫☺☻♂♀†‡ $¤¢£\n◄▼► ←↓→ ↔↕☼◊○●□■•◘◙◌ ¥€₪₽',),
             })
##### Replace & Regexp box #################################################################
def _make_ui_re(master,rlist,strings):
    def _tags(s):return s.replace('<Enter>','\n').replace('<Tab>','\t').replace('<Nbsp>','\xa0')
    from re import sub
    refunc=lambda a,b,c,d:(sub(b,_tags(c),a)if d else a.replace(_tags(b),_tags(c)))
    def make_(i,s='sel.first',S='sel.last'):
        try:a=text.get(s,S);text.replace(s,S,refunc(a,rlist[i][1].get(),rlist[i][3].get(),re.get()))
        except:a=text.get(1.0,'end');text.replace(1.0,'end',refunc(a,rlist[i][1].get(),rlist[i][3].get(),re.get()))
    def _all():a=text.tag_ranges('sel');[make_(i,*[i.string for i in a]if a else[])for i in rlist]
    def del_(i):[j.destroy()for j in rlist[i]];del rlist[i]
    def add_():
        i=len(rlist)+5
        while i in rlist:i+=1
        l=[tkinter.Button(master,text=strings['left'],command=lambda:make_(i)),tkinter.Entry(master),tkinter.Label(master,text=strings['mid']),tkinter.Entry(master),
           tkinter.Button(master,text=strings['add'],command=add_),tkinter.Button(master,text=strings['del'],command=lambda:del_(i))]
        rlist[i]=l
        for j in range(len(l)):l[j].grid(row=i,column=j,sticky='nsew')
    tkinter.Button(master,text=strings['all'],command=_all).grid(row=4,column=0,sticky='nsew')
    re=tkinter.BooleanVar()
    popup(tkinter.Label)(master,image=images['help'],compound='left',text=strings['top'],popup_text=strings['tags'],relief='groove').grid(row=4,column=3,sticky='nsew')
    popup(tkinter.Checkbutton)(master,text=strings['regexp'],variable=re,popup_text=strings['help']).grid(row=4,column=1,columnspan=2,sticky='nsew')
    tkinter.Button(master,text=strings['add'],command=add_).grid(row=4,column=4,columnspan=2,sticky='nsew')
    add_()
_make_ui_re(REPLACE_PANEL,{},locale.replace)
######################################################################
MENU.add_command(label='dev exit',command=tk.destroy)
_erase_history(all=True);set_font(('Courier',12));flip_panel(0);tk.mainloop()
