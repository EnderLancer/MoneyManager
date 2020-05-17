import tkinter as tk
from tkinter import ttk
import tkinter as Tk
from urllib import request, parse
import json
import hashlib
import datetime as datetime
import webbrowser

SITE_URL = "https://kursova-shadey.000webhostapp.com"
REQUEST_URL = SITE_URL + "/requests/"
PATH_IMG = "images/"
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Окей", command=leavemini)
    B1.pack()
    popup.mainloop()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(False, False)

        tk.Tk.wm_title(self, "Менеджер капитала")
        self.user = User()
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.defines = self.user.getDefinitions()
        for F in (AuthorizationPage, WalletsPage, CreateWalletPage, Main):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(AuthorizationPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == WalletsPage:
            if len(self.user.getWallets()) == 0:
                frame = self.frames[CreateWalletPage]
            else:
                self.after(1, frame.showWallets)
        elif cont == Main:
            self.after(1, frame.view_records)
        frame.tkraise()




class AuthorizationPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        authFrame = tk.LabelFrame(self, text="Авторизация", bg='#d7d8e0')

        loginLine = tk.Frame(authFrame, bg='#d7d8e0')
        label = tk.Label(loginLine, text="Логин:", bg='#d7d8e0')
        label.config(anchor=tk.CENTER)
        label.pack(side="left", fill="x", pady=5)
        loginEntry = ttk.Entry(loginLine)
#        loginEntry.insert(0, 'stormRak')
        loginEntry.pack(side="right")
        loginLine.pack(fill="x", pady=5)

        passLine = tk.Frame(authFrame, bg='#d7d8e0')
        label2 = tk.Label(passLine, text="Пароль:", bg='#d7d8e0')
        label2.config(anchor=tk.CENTER)
        label2.pack(side="left", fill="x", pady=5)
        password = ttk.Entry(passLine, show="*")
#        password.insert(0, 'storm')
        password.pack(pady=5)
        passLine.pack(fill="x", pady=5)

        def login():
            controller.user.log_in(loginEntry.get(), password.get())
#            controller.user.log_in('storm@rak.pak', 'storm')
            if controller.user.isUserLogin():
                controller.show_frame(WalletsPage)
            else:
                popupmsg(":(")
        button1 = tk.Button(authFrame, text="Войти", bg='LightGreen',
                             command=lambda: login())
        button1.pack(fill="x", pady=10)
        button1.focus_set()

        def callback(event):
            webbrowser.open_new(SITE_URL)
        lbl = tk.Label(authFrame, text="Нету аккаунта? тыкни сюда", fg="blue", cursor="hand2")
        lbl.pack()
        lbl.bind("<Button-1>", callback)
#        authFrame.config(anchor=tk.CENTER)
        authFrame.place(anchor="c", relx=.5, rely=.5)


class WalletsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.me = self
        self.controller = controller
        self.user = controller.user
        self.allWallets = tk.Frame(self)
        self.delete_wallet_img = tk.PhotoImage(file=PATH_IMG+'delete_wallet.png')
        self.add_wallet_img = tk.PhotoImage(file=PATH_IMG+'add_wallet.png')
        button2 = tk.Button(self, text="Создать кошелёк!", bd=0, image=self.add_wallet_img,
                             compound=tk.TOP, command=lambda: controller.show_frame(CreateWalletPage))
        button2.place(anchor="nw")

        self.exit_img = tk.PhotoImage(file=PATH_IMG+'exit.png')
        button2 = tk.Button(self, text="Выйти", bd=0, image=self.exit_img,
                             compound=tk.TOP, command=lambda: controller.show_frame(AuthorizationPage))
        button2.pack(side=tk.BOTTOM)


    def showWallets(self):
        self.allWallets.destroy()
        self.allWallets = tk.Frame(self, width=200)
        ttk.Label(self.allWallets, text='Доступные кошельки:').pack()
        def openWallet(walletId):
            self.user.chooseWallet(walletId)
            self.controller.show_frame(Main)
        def deleteWallet(walletId):
            self.user.deleteWallet(walletId)
            self.user.updateAvailableWallets()
            self.controller.show_frame(WalletsPage)
        def guess(wallet):
            walletId, walletName = list(wallet)
            guessUp = tk.Toplevel()

            def leavemini(isTrue):
                if isTrue:
                    deleteWallet(walletId)
                guessUp.destroy()

            guessUp.wm_title("!")
            ttk.Label(guessUp, text="Уверен что хочешь удалить кошелёк {}?".format(walletName)).pack(pady=5)
            ttk.Button(guessUp, text="Да", command=lambda isTrue=True: leavemini(isTrue)).pack(side=tk.LEFT)
            ttk.Button(guessUp, text="Нет", command=lambda isTrue=False: leavemini(isTrue)).pack(side=tk.RIGHT)
            guessUp.mainloop()

        for wallet in self.controller.user.getWallets():
            walletForm = tk.LabelFrame(self.allWallets, text=wallet['wallet_name'])
            ttk.Label(walletForm, text=str(wallet['currency_symbol'])).pack(side="left")
            ttk.Button(walletForm, text="Открыть!",
                       command=lambda i=wallet["wallet_id"]: openWallet(i)).pack(side="left")
            tk.Button(walletForm, text="Удалить!", bd=0, image=self.delete_wallet_img, compound=tk.TOP,
                       command=lambda i=(wallet["wallet_id"], wallet["wallet_name"],): guess(i)).pack(side="right", padx=15, pady=5)
            walletForm.pack(fill="x", expand=True, pady=2)
        self.allWallets.place(anchor="n", relx=.5)



class CreateWalletPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        createFrame = ttk.LabelFrame(self, text="Создание кошелька:")

        walletName = ttk.Entry(createFrame)
        walletName.pack(side="left")

        currencyVar = tk.StringVar(createFrame)
        currencyVar.set(controller.defines["currency"][0]["symbol"])
        currenciesSymbol = [currency["symbol"] for currency in controller.defines["currency"]]
        chooseCurrency = tk.OptionMenu(createFrame, currencyVar, *currenciesSymbol)
        chooseCurrency.pack(side="left")


        def createWallet():
            if (0 < len(walletName.get()) < 20
                    and '&' not in walletName.get()):

                walletCurrencyId = 0
                for currency in controller.defines["currency"]:
                    if currency["symbol"] == currencyVar.get():
                        walletCurrencyId = currency["id"]
                controller.user.createWallet(walletName.get(), walletCurrencyId)
                controller.show_frame(WalletsPage)


        button1 = ttk.Button(createFrame, text="Создать!",
                             command=lambda: createWallet())
        button1.pack()

        createFrame.place(anchor="c", relx=.5, rely=.5)

class Main(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_main()


    def init_main(self):
        toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == 'volume':
                l.sort(key=lambda t: float(t[0]), reverse=reverse)
            else:
                l.sort(key=lambda t: t[0], reverse=reverse)

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            tv.heading(col,
                       command=lambda: treeview_sort_column(tv, col, not reverse))

        self.back_img = tk.PhotoImage(file=PATH_IMG+'back.png')
        btn_choose_wallet = tk.Button(toolbar, text='Выбрать кошелёк', bg='#d7d8e0', bd=0, image=self.back_img,
                                    compound=tk.TOP, command=lambda: self.controller.show_frame(WalletsPage))
        btn_choose_wallet.pack(side=tk.LEFT)
        ttk.Separator(toolbar).pack(side="left", fill="y", padx=2)
        self.add_img = tk.PhotoImage(file=PATH_IMG+'add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', bg='#d7d8e0', bd=0, image=self.add_img,
                                    compound=tk.TOP, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file=PATH_IMG+'update.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file=PATH_IMG+'delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.add_user_img = tk.PhotoImage(file=PATH_IMG+'add_user.png')
        btn_add_user = tk.Button(toolbar, text='Предоставить доступ', bg='#d7d8e0', bd=0, image=self.add_user_img,
                               compound=tk.TOP, command=self.sharePermission)
        btn_add_user.pack(side=tk.RIGHT)
        ttk.Separator(toolbar).pack(side="right", fill="y", padx=2)
        self.analysis_img = tk.PhotoImage(file=PATH_IMG+'analysis.png')
        btn_analysis = tk.Button(toolbar, text='Анализ кошелька', bg='#d7d8e0', bd=0, image=self.analysis_img,
                               compound=tk.TOP, command=self.sharePermission)
        btn_analysis.pack(side=tk.RIGHT)

        treeColumns = {'id': "ID",
                       'description': "Наименование",
                       'datetime': "Добавленно",
                       'action': "Тип",
                       'volume': "Сумма"}
        self.tree = ttk.Treeview(self, columns=list(treeColumns.keys()), height=15, show='headings')
        self.tree["displaycolumns"] = ('volume', 'action', 'description', 'datetime')
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('datetime', width=150, anchor=tk.CENTER)
        self.tree.column('action', width=100, anchor=tk.CENTER)
        self.tree.column('volume', width=150, anchor=tk.CENTER)
        self.tree.heading('description', text='Наименование')
        self.tree.heading('datetime', text='Добавленно')
        self.tree.heading('action', text='Тип')
        self.tree.heading('volume', text='Сумма')
        self.tree.pack()

        for col in list(treeColumns.keys()):
            self.tree.heading(col, text=treeColumns[col],
                             command=lambda c=col: treeview_sort_column(self.tree, c, False))

        self.balaneBar = tk.Frame(self)
        ttk.Label(self.balaneBar, text='Счёт: ').pack(side=tk.LEFT)
        self.balance = tk.Label(self.balaneBar, text='0')
        self.balance.pack(side=tk.LEFT)
        self.balance_currency = tk.Label(self.balaneBar, text='')
        self.balance_currency.pack(side=tk.LEFT)
        self.status = tk.Label(self.balaneBar, text='')
        self.status.pack(side=tk.RIGHT)
        self.walletNameLabel = ttk.Label(self.balaneBar, text=self.controller.user)
        self.walletNameLabel.place(anchor="c", relx=.5, rely=.45)
        ttk.Label(self.balaneBar, text='Ваш статус: ').pack(side=tk.RIGHT)
        self.balaneBar.pack(side=tk.BOTTOM, fill='x', expand=True)

    def records(self, description, actionName, volume):
        actions = self.controller.defines["action"]
        actionId = 0
        for actionInd in list(actions.keys()):
            if actionName == actions[actionInd]:
                actionId = actionInd
        self.controller.user.addRecord(volume, actionId, description)
        self.view_records()

    def update_record(self, recordId, description, actionName, volume):
        actions = self.controller.defines["action"]
        actId = 0
        for actionInd in list(actions.keys()):
            if actionName == actions[actionInd]:
                actId = actionInd
        self.controller.user.rewriteRecord(recordId, volume, actId, description)
        self.view_records()

    def view_records(self):
        self.balance_currency['text'] = self.controller.user.getCurrentWallet()["currency"]
        self.status['text'] = self.controller.user.getCurrentWallet()["access_level"]
        self.walletNameLabel['text'] = self.controller.user.getCurrentWallet()["name"]
        self.controller.user.updateRecords()
        [self.tree.delete(i) for i in self.tree.get_children()]
        volumeSum = 0
        for row in self.controller.user.getCurrentWallet()["records"]:
            if row["actionId"] == '1':
                volumeSum += float(row["volume"])
            else:
                volumeSum -= float(row["volume"])
            rowValues = [row["id"], row["description"], row["datetime"], row["action"], row["volume"]]
            self.tree.insert('', 'end', values=rowValues)
        self.balance['text'] = str(volumeSum)

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.controller.user.deleteRecord(self.tree.set(selection_item, 'id'))
        self.view_records()

    def sharePermission(self):
        Permissions(self.controller, self)

    def open_dialog(self):
        Child(self.controller, self)

    def open_update_dialog(self):
        values = self.tree.set(self.tree.selection()[0])
        Update(self.controller, values, self)



class Permissions(tk.Toplevel):
    def __init__(self, controller, parent):
        super().__init__(app)
        self.controller = controller
        self.parent = parent
        self.view = app
        self.usersList = list()
        self.title('Предоставить доступ')
        self.geometry('300x620+400+300')
        self.searchLine = tk.Frame(self)
        self.entryLogin = tk.Entry(self.searchLine)
        self.entryLogin.pack(side="left")

        def selectPermission(userId, accessLvl):
            accessLvlId = 0
            for accessKey in self.controller.defines["accessLvl"].keys():
                if accessLvl == self.controller.defines["accessLvl"][accessKey]:
                    accessLvlId = accessKey
            login = self.controller.user.sharePermission(userId, accessLvlId)
            if len(login) > 0:
                popupmsg("Now "+login["login"]+" have permission "+accessLvl+" to this wallet.")
            self.destroy()

        def search():
            self.resultField.destroy()
            self.resultField = tk.Frame(self)
            self.usersList = self.controller.user.findUsers(self.entryLogin.get())
            for user in self.usersList:
                userLine = tk.LabelFrame(self.resultField, text=user["login"])
                ttk.Label(userLine, text=user["last_name"]+' '+user["first_name"]).pack(side="left")
                ttk.Button(userLine, text='Дать доступ',
                           command=lambda: selectPermission(user["user_id"], access.get())).pack(side="right", padx=1)
                access = ttk.Combobox(userLine, values=list(self.controller.defines["accessLvl"].values()))
                access.current(0)
                access.pack(side="right", padx=1)
                userLine.pack(pady=2)
            self.resultField.pack()

        self.searchButton = tk.Button(self.searchLine, text='Искать', command=search)
        self.searchButton.pack(side="right")
        self.searchLine.pack(side=tk.TOP)

        self.resultField = tk.Frame(self)
        self.resultField.pack()



class Child(tk.Toplevel):
    def __init__(self, controller, parent):
        super().__init__(app)
        self.controller = controller
        self.parent = parent
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья дохода/расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=list(self.controller.defines["action"].values()))
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        def add():
            self.parent.records(self.entry_description.get(), self.combobox.get(), self.entry_money.get())
            self.destroy()

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: add())
        self.grab_set()
        self.focus_set()


class Update(tk.Toplevel):
    def __init__(self, controller, pastValues, parent):
        super().__init__(app)
        self.controller = controller
        self.parent = parent
        self.view = app
        print('past values ',pastValues)
        self.pastValues = pastValues
        self.init_edit()

    def callback(self, P):
        try:
            float(P)
            return True
        except ValueError:
            return False

    def init_edit(self):
        self.title('Редактировать позицию')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.insert(0, self.pastValues["description"])
        self.entry_description.place(x=200, y=50)

        vcmd = (self.register(self.callback))
        self.entry_money = ttk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        print(float(self.pastValues["volume"]))
        self.entry_money.insert(0, float(self.pastValues["volume"]))
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=list(self.controller.defines["action"].values()))
        self.combobox.insert(0, self.pastValues["action"])
        self.combobox.place(x=200, y=80)

        def rewrite():
            self.parent.update_record(self.pastValues["id"], self.entry_description.get(),
                                    self.combobox.get(), self.entry_money.get())
            self.destroy()

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: rewrite())

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)


class User:

    def __init__(self):
        self.isLogin = False
        self.id = 0
        self.passMD5 = ""
        self.wallets = []
        self.curentWallet = {}

    def isUserLogin(self):
        return self.isLogin

    def getId(self):
        return self.id

    def getPassMD5(self):
        return self.passMD5

    def getWallets(self):
        return self.wallets

    def getCurrentWallet(self):
        return self.curentWallet

    def sendReq(self, requestURL, reqValues, autoLogin=True):
        try:
            if autoLogin:
                reqValues["userId"] = self.getId()
                reqValues["pass"] = self.passMD5
            reqAddiction = parse.urlencode(reqValues, encoding='utf-8')
            sendURL = REQUEST_URL + requestURL + reqAddiction
            print(requestURL + reqAddiction)
            req = request.Request(sendURL)
            answer = request.urlopen(req).read().decode("utf-8")
            print('req answer', answer)
            return answer

        except Exception as e:
            popupmsg('ERROR<sendReq>: '+str(e))

    def getDefinitions(self):
        requestPHPFile = "receive_definitions.php"
        reqValues = {}
        answer = self.sendReq(requestPHPFile, reqValues, autoLogin=False)
        answerJSON = json.loads(answer)
        accessLvlDict = {}
        for accessLvl in answerJSON["accessLvl"]:
            accessLvlDict[accessLvl["access_level_id"]] = accessLvl["access_level_name"]
        answerJSON["accessLvl"] = accessLvlDict
        actionDict = {}
        for action in answerJSON["action"]:
            actionDict[action["action_id"]] = action["action_name"]
        answerJSON["action"] = actionDict
        statusDict = {}
        for status in answerJSON["status"]:
            statusDict[status["status_id"]] = status["status_name"]
        answerJSON["status"] = statusDict
        currencyDict = []
        for currency in answerJSON["currency"]:
            currencyNamesDict = {}
            currencyNamesDict["id"] = currency["currency_id"]
            currencyNamesDict["name"] = currency["currency_name"]
            currencyNamesDict["symbol"] = currency["currency_symbol"]
            currencyDict.append(currencyNamesDict)
        answerJSON["currency"] = currencyDict
        return answerJSON

    def log_in(self, login, password):
        try:
            requestPHPFile = "log_in.php?"
            passMD5 = hashlib.md5(str(password).encode()).hexdigest()
            reqValues = {"login": login,
                        "pass": passMD5}
            answer = self.sendReq(requestPHPFile, reqValues, autoLogin=False)
            answerJSON = json.loads(answer)
            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            else:
                self.id = answerJSON["userId"]
                self.passMD5 = passMD5
                self.isLogin = True
                self.updateAvailableWallets()
        except Exception as e:
            popupmsg('ERROR<log_in>: '+str(e))

    def updateAvailableWallets(self):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "available_wallets.php?"
            reqValues = {}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)

            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            else:
                answerJSON = json.loads(answer)
                self.wallets = answerJSON
        except Exception as e:
            popupmsg('ERROR<updateAvailableWallets>: '+str(e))

    def chooseWallet(self, walletId):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "choose_wallet.php?"
            reqValues = {"walletId": walletId}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)

            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            else:
                answerJSON = json.loads(answer)
                records = [{"id":           record["records_id"],
                            "description":  record["record_name"],
                            "datetime":     record["datetime"],
                            "volume":       record["volume"],
                            "actionId":     record["action_id"],
                            "action":       record["action_name"]
                            } for record in answerJSON["records"]]

                wallet = {"id":             answerJSON["wallet_id"],
                          "name":           answerJSON["wallet_name"],
                          "access_level":   answerJSON["access_level_name"],
                          "currency":       answerJSON["currency_symbol"],
                          "records":        records}
                self.curentWallet = wallet
        except Exception as e:
            popupmsg('ERROR<chooseWallet>: '+str(e))

    def createWallet(self, walletName, walletCurrencyId):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "create_wallet.php?"
            reqValues = {"currId": walletCurrencyId,
                        "name": walletName}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)
            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            else:
                answerJSON = json.loads(answer)
                self.updateAvailableWallets()
        except Exception as e:
            popupmsg('ERROR<createWallet>: '+str(e))

    def deleteWallet(self, walletId):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "delete_wallet.php?"
            reqValues = {"walletId": walletId}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)
            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            else:
                answerJSON = json.loads(answer)
                self.updateAvailableWallets()
        except Exception as e:
            popupmsg('ERROR<deleteWallet>: '+str(e))

    def addRecord(self, volume, actId, description=''):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "add_record.php?"
            if len(self.getCurrentWallet()) > 0:
                walletId = self.getCurrentWallet()["id"]
                reqValues = {"walletId":    walletId,
                             "recordName":  description,
                             "volume":      volume,
                             "actId":       actId}
                answer = self.sendReq(requestPHPFile, reqValues)
                answerJSON = json.loads(answer)

                if 'code' in answerJSON:
                    popupmsg(answerJSON["msg"])
                else:
                    answerJSON = json.loads(answer)
            else:
                popupmsg("take me on the other side")
        except Exception as e:
            popupmsg('ERROR<addRecord>: '+str(e))

    def updateRecords(self):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "update_records.php?"
            reqValues = {"walletId": self.getCurrentWallet()["id"]}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)

            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            else:
                answerJSON = json.loads(answer)
                wallet = self.curentWallet
                records = [{"id":           record["records_id"],
                            "description":  record["record_name"],
                            "datetime":     record["datetime"],
                            "volume":       record["volume"],
                            "actionId":     record["action_id"],
                            "action":       record["action_name"]
                            } for record in answerJSON]
                wallet["records"] = records
                self.curentWallet = wallet
        except Exception as e:
            popupmsg('ERROR<updateRecords>: '+str(e))

    def deleteRecord(self, recordId):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "delete_record.php?"
            reqValues = {"walletId": self.getCurrentWallet()["id"],
                         "recordId": recordId}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)
            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
        except Exception as e:
            popupmsg('ERROR<deleteRecords>: '+str(e))

    def findUsers(self, guess):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "find_user.php?"
            reqValues = {"findUser": guess}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)
            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            return answerJSON
        except Exception as e:
            popupmsg('ERROR<findUsers>: '+str(e))

    def sharePermission(self, addUserId, addUserAccessId):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "share_permission.php?"
            reqValues = {"walletId": self.getCurrentWallet()["id"],
                         "addUserId": addUserId,
                         "addUserAccessId": addUserAccessId}
            answer = self.sendReq(requestPHPFile, reqValues)
            answerJSON = json.loads(answer)
            if 'code' in answerJSON:
                popupmsg(answerJSON["msg"])
            return answerJSON[0]
        except Exception as e:
            popupmsg('ERROR<sharePermission>: '+str(e))

    def rewriteRecord(self, recordId, volume, actId, description=''):
        try:
            if not self.isUserLogin():
                popupmsg("You not log in.")
            requestPHPFile = "rewrite_record.php?"
            if len(self.getCurrentWallet()) > 0:
                reqValues = {"recordId":    recordId,
                             "walletId":    self.getCurrentWallet()["id"],
                             "recordName":  description,
                             "volume":      volume,
                             "actId":       actId}
                answer = self.sendReq(requestPHPFile, reqValues)
                answerJSON = json.loads(answer)

                if 'code' in answerJSON:
                    popupmsg(answerJSON["msg"])
                else:
                    answerJSON = json.loads(answer)
            else:
                popupmsg("take me on the other side")
        except Exception as e:
            popupmsg('ERROR<rewriteRecord>: '+str(e))



if __name__ == "__main__":
    app = App()
    app.mainloop()

#    user = User()
#    user.log_in('storm@rak.pak', 'storm')


