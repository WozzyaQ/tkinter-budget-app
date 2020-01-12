import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import budget

matplotlib.use("TkAgg")

password = ""


class GUI:
    def __init__(self, terminal):

        self.terminal = terminal
        self.filter = budget.Filter(terminal)
        root = self.root = tk.Tk()
        root.title("Budget")
        root.geometry("1200x800+100+100")
        root.resizable(False, False)
        root.withdraw()
        root.protocol("WM_DELETE_WINDOW", self.save_all)

        self.main_font = main_font = Font(family='Courier New', size=24, weight='normal')

        # canvas for buttons, bd=0 and highlightthickness=0 is for no border
        self.left_canvas = left_canvas = tk.Canvas(root,
                                                   width=300,
                                                   height=800,
                                                   bg="#e9e9e9",
                                                   bd=0,
                                                   highlightthickness=0)

        add_income_btn = tk.Button(left_canvas, text="ADD INCOME",
                                   font=main_font,
                                   command=self.add_income_btn_clicked,
                                   bd=0,
                                   highlightthickness=0)

        add_expense_btn = tk.Button(left_canvas, text="ADD EXPENSE",
                                    font=main_font,
                                    command=self.add_expense_btn_clicked,
                                    bd=0,
                                    highlightthickness=0)

        put_deposit_btn = tk.Button(left_canvas, text="PUT DEPOSIT",
                                    font=main_font,
                                    command=self.put_deposit_btn_clicked,
                                    bd=0,
                                    highlightthickness=0)

        get_credit_btn = tk.Button(left_canvas, text="GET CREDIT",
                                   font=main_font,
                                   command=self.get_credit_btn_clicked,
                                   bd=0,
                                   highlightthickness=0)
        app_titple = tk.Label(left_canvas, text="MyBudget",
                              font=Font(family="Courier New", size=35),
                              bd=0,
                              highlightthickness=0,
                              bg="#D9CECE")

        filter_button = tk.Button(left_canvas, text="FILTER",
                                  font=main_font,
                                  command=self.filter_btn_clicked,
                                  bd=0,
                                  highlightthickness=0)

        credits_button = tk.Button(left_canvas, text="Credits",
                                   font=Font(family="Courier New", size=20, weight="normal"),
                                   command=self.credits_btn_clicked,
                                   bd=0,
                                   highlightthickness=0)
        add_expense_btn.pack()
        add_income_btn.pack()
        put_deposit_btn.pack()
        get_credit_btn.pack()
        app_titple.pack()
        filter_button.pack()
        credits_button.pack()

        # Left styling line
        left_canvas.create_line(0, 0, 0, 800, fill="grey")

        # Buttons
        left_canvas.create_window((30, 110), anchor="nw", window=add_income_btn, width=240, height=60)
        left_canvas.create_window((30, 200), anchor="nw", window=add_expense_btn, width=240, height=60)
        left_canvas.create_window((30, 300), anchor="nw", window=put_deposit_btn, width=240, height=60)
        left_canvas.create_window((30, 400), anchor="nw", window=get_credit_btn, width=240, height=60)
        left_canvas.create_window((20, 20), anchor="nw", window=app_titple, width=260, height=60)
        left_canvas.create_window((30, 500), anchor="nw", window=filter_button, width=240, height=60)
        left_canvas.create_window((100, 768), anchor="nw", window=credits_button, width=100, height=30)
        left_canvas.place(x=900, y=0)

        self.information_canvas = information_canvas = tk.Canvas(root,
                                                                 width=900,
                                                                 height=600,
                                                                 bg="#f8f8f8",
                                                                 bd=0,
                                                                 highlightthickness=0)

        # Line below information canvas
        information_canvas.create_line(0, 599, 900, 599, fill="black")

        # Pie chart setup
        self.pie_chart, self.a = plt.subplots(figsize=(5.5,5.5))
        self.a.set_title("BALANCE PIE CHART")
        self.pie_chart.set_facecolor("#f8f8f8")
        self.a.pie([1], colors=["Brown"])
        canvas = FigureCanvasTkAgg(self.pie_chart, information_canvas)
        canvas.get_tk_widget().place(x=0, y=0)

        # Total, income, expense
        total_label = self.total_label = tk.Label(text="Total: ",
                                                  font=Font(family='Courier New', size=30, weight='normal'),
                                                  bg="#f8f8f8")

        income_label = self.income_label = tk.Label(text="Income: ",
                                                    font=self.main_font,
                                                    bg="#f8f8f8")
        expense_label = self.expense_label = tk.Label(text="Expense: ",
                                                      font=self.main_font,
                                                      bg="#f8f8f8")
        total_label.place(x=550, y=180)
        income_label.place(x=570, y=250)
        expense_label.place(x=570, y=300)

        information_canvas.place(x=0, y=0)

        self.last_transaction_canvas = last_transaction_canvas = tk.Canvas(root,
                                                                           width=900,
                                                                           height=200,
                                                                           bg="#f8f8f8",
                                                                           bd=0,
                                                                           highlightthickness=0)

        last_transaction_canvas.create_line(0, 20, 900, 20, fill="black")

        # transaction lines
        for i in range(1, 5):
            last_transaction_canvas.create_line(0, 20+i*36, 900, 20+i*36)

        last_transaction_canvas.create_text(360, 0, text="LAST TRANSACTIONS",
                                            anchor="nw",
                                            font=Font(family="Courier New", size=20, weight="normal"),
                                            fill="black")
        # last transaction text, each field has tag tr$, where $ -> 1-5
        for i in range(5):
            last_transaction_canvas.create_text(0, 20+i*36,
                                                anchor="nw",
                                                text="NONE",
                                                font=Font(family="Courier New", size=20, weight="normal"),
                                                justify="center",
                                                width=900,
                                                tag="tr"+str(i+1))

        last_transaction_canvas.place(x=0, y=600)

        self.digit_validation = (self.root.register(self.do_digits_validation), "%P")
        self.dot_and_digit_validation = (self.root.register(self.do_dot_digit_validation), "%P")

        # Костыль который помогает очищать и работать с новыми созданными окнами
        # radio_btn_state, date, total, percent, category, purpose
        self.dynamic_widgets = dict()
        self.fill_zeros_dynamic_widgets(self.dynamic_widgets)
        self.create_start_window()

    # костыль, который помогает не  столкнуться с KeyErroro'м когда пытаешся достать значение из словаря по
    # несуществующему ключу
    @staticmethod
    def fill_zeros_dynamic_widgets(dynamic_widgets):
        dynamic_widgets.update(current_popup=None,
                               total=None,
                               date=None,
                               purpose=None,
                               percent=None,
                               radio_btn_state=None,
                               periodic_type=None,
                               percent_label_popup=None)

    # обнуляет костыль
    def reset_dynamic_widgets(self):
        for key in self.dynamic_widgets.keys():
            self.dynamic_widgets[key] = None

    # кривая валидация на точки и цифры
    def do_dot_digit_validation(self, value):
        if value:
            try:
                if value[-1] == "." and value[-2] != "." or value[-1].isdigit():
                    return True
                else:
                    return self.do_digits_validation(value)
            except IndexError:
                if value == ".":
                    return False
        return True

    @staticmethod
    def do_digits_validation(value):
        if value:
            try:
                int(value)
                return True
            except ValueError:
                return False
        else:
            return True

    @staticmethod
    def do_date_validation(date):
        try:
            datetime.datetime.strptime(date, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    # создает и возвращает новое окно с заданым размером
    def create_basic_popup(self, width, height):
        popup = tk.Toplevel(self.root)
        popup.geometry(F"{width}x{height}+500+200")
        popup.grab_set()
        popup.resizable(False, False)

        self.dynamic_widgets["current_popup"] = popup
        return popup

    # настраивает нужные виджеты для окон кредитов и депозитов
    def configure_credit_deposit_popup(self, top):
        top_frame = tk.Frame(top)
        frame_for_button = tk.Frame(top)

        date_label = tk.Label(top_frame, text="Date",
                              font=self.main_font)

        date_input = tk.Entry(top_frame,
                              font=self.main_font,
                              width=10,
                              validate="key",
                              validatecommand=self.dot_and_digit_validation)

        total_label = tk.Label(top_frame,
                               text="Total",
                               font=self.main_font)

        total_input = tk.Entry(top_frame,
                               font=self.main_font,
                               width=10,
                               validate="key",
                               validatecommand=self.dot_and_digit_validation)

        percent_label = tk.Label(top_frame,
                                 text="Percent",
                                 font=self.main_font)

        percent_input = tk.Entry(top_frame,
                                 font=self.main_font,
                                 width=10,
                                 validate="key",
                                 validatecommand=self.dot_and_digit_validation)

        periodic_type = ttk.Combobox(top_frame,
                                     values=[
                                         "Day",
                                         "Week",
                                         "Month",
                                         "Quarter",
                                         "Year"
                                     ],
                                     font=Font(family="Courier New", size=15),
                                     width=10,
                                     state="readonly")

        submit_button = tk.Button(frame_for_button,
                                  font=self.main_font,
                                  text="Submit",
                                  command=self.load_transaction)

        purpose_label = tk.Label(top_frame,
                                 text="Purpose",
                                 font=self.main_font)

        purpose_input = tk.Entry(top_frame,
                                 font=self.main_font,
                                 width=10)

        date_label.grid(row=0, column=0)
        date_input.grid(row=0, column=1)
        total_label.grid(row=1, column=0)
        total_input.grid(row=1, column=1)
        percent_label.grid(row=2, column=0)
        percent_input.grid(row=2, column=1)
        periodic_type.grid(row=3, column=1)
        purpose_label.grid(row=4, column=0)
        purpose_input.grid(row=4, column=1)

        submit_button.pack()

        top_frame.pack()
        frame_for_button.pack()
        self.dynamic_widgets["total"] = total_input
        self.dynamic_widgets["date"] = date_input
        self.dynamic_widgets["purpose"] = purpose_input
        self.dynamic_widgets["percent"] = percent_input
        self.dynamic_widgets["periodic_type"] = periodic_type

    # настраивает нужные виджеты окнам растрат и доходов
    def configure_expense_income_popup(self, top):
        top_frame = tk.Frame(top)
        frame_for_button = tk.Frame(top)

        total_label = tk.Label(top_frame,
                               text="Total",
                               font=self.main_font)

        total_input = tk.Entry(top_frame,
                               font=self.main_font,
                               width=10,
                               validate="key",
                               validatecommand=self.dot_and_digit_validation)

        date_label = tk.Label(top_frame, text="Date",
                              font=self.main_font)

        date_input = tk.Entry(top_frame,
                              font=self.main_font,
                              width=10,
                              validate="key",
                              validatecommand=self.dot_and_digit_validation)

        periodic_label = tk.Label(top_frame, text="Periodic", font=self.main_font)

        r_var = tk.BooleanVar()
        r_var.set(0)
        self.dynamic_widgets["radio_btn_state"] = r_var.get()

        periodic_radio_btn_yes = tk.Radiobutton(top_frame,
                                                text="Yes",
                                                font=self.main_font,
                                                variable=r_var,
                                                value=True,
                                                command=lambda: self.show_periodic_settings(top_frame, r_var))

        periodic_radio_btn_no = tk.Radiobutton(top_frame,
                                               text="No",
                                               font=self.main_font,
                                               variable=r_var,
                                               value=False,
                                               command=lambda: self.show_periodic_settings(top_frame, r_var))

        purpose_label = tk.Label(top_frame,
                                 text="Purpose",
                                 font=self.main_font)

        purpose_input = tk.Entry(top_frame,
                                 font=self.main_font,
                                 width=10)

        submit_button = tk.Button(frame_for_button,
                                  font=self.main_font,
                                  text="Submit",
                                  command=self.load_transaction)

        date_label.grid(row=0, column=0)
        date_input.grid(row=0, column=1)

        total_label.grid(row=1, column=0)
        total_input.grid(row=1, column=1)

        periodic_label.grid(row=2, column=0)
        periodic_radio_btn_yes.grid(row=2, column=1)
        periodic_radio_btn_no.grid(row=2, column=2)

        purpose_label.grid(row=5, column=0)
        purpose_input.grid(row=5, column=1)

        submit_button.pack()

        top_frame.pack()
        frame_for_button.pack()

        self.dynamic_widgets["total"] = total_input
        self.dynamic_widgets["date"] = date_input
        self.dynamic_widgets["purpose"] = purpose_input

    # еще один костыль
    def show_periodic_settings(self, frame, state):
        if state.get():
            periodic_type = ttk.Combobox(frame,
                                         values=[
                                            "Day",
                                            "Week",
                                            "Month",
                                            "Quarter",
                                            "Year"
                                            ],
                                         font=Font(family="Courier New", size=15),
                                         width=10,
                                         state="readonly")

            percent_label = tk.Label(frame,
                                     text="Percent",
                                     font=self.main_font,
                                     width=10)

            percent_entry = tk.Entry(frame,
                                     font=self.main_font,
                                     width=10,
                                     validate="key",
                                     validatecommand=self.dot_and_digit_validation)

            periodic_type.grid(row=3, column=1)
            percent_label.grid(row=4, column=0)
            percent_entry.grid(row=4, column=1)
            self.dynamic_widgets.update(periodic_type=periodic_type,
                                        radio_btn_state=state.get(),
                                        percent_label_popup=percent_label,
                                        percent=percent_entry)
        else:
            self.dynamic_widgets["periodic_type"].destroy()
            self.dynamic_widgets["radio_btn_state"] = state.get()
            self.dynamic_widgets["percent_label_popup"].destroy()
            self.dynamic_widgets["percent"].destroy()

            self.dynamic_widgets["periodic_type"] = None
            self.dynamic_widgets["radio_btn_state"] = None
            self.dynamic_widgets["percent_label_popup"] = None
            self.dynamic_widgets["percent"] = None

    # закрывает текущее всплывающее меню
    def close_popup(self, popup=None, update_widgets=False):
        if popup:
            popup.destroy()
        else:
            self.dynamic_widgets["current_popup"].destroy()
        if update_widgets:
            self.update_total()
            self.update_pie_chart()
            self.update_expense()
            self.update_income()
        self.reset_dynamic_widgets()

    # обновляет полоску последних транзакций
    def update_last_transactions_box(self, last_transaction):
        for i in range(5, 1, -1):
            id = self.last_transaction_canvas.find_withtag(F"tr{i-1}")
            text = self.last_transaction_canvas.itemcget(*id, 'text')
            self.last_transaction_canvas.itemconfigure(F"tr{i}", text=text)

        self.last_transaction_canvas.itemconfigure(F"tr1", text=last_transaction)

    # загружает параметры в логику
    def load_transaction(self):

        date = self.dynamic_widgets["date"].get()
        total = self.dynamic_widgets["total"].get()
        purpose = self.dynamic_widgets["purpose"].get()
        type_of_transaction = self.dynamic_widgets["transaction"]
        if self.do_date_validation(date) and total:
            if self.dynamic_widgets["radio_btn_state"]:
                period = self.dynamic_widgets["periodic_type"].get()
                percent = self.dynamic_widgets["percent"].get()
                print(period)
                if not percent or not period:
                    messagebox.showinfo("Warning",
                                        "The percentage and period fields must be filled")
                    return
                # transaction_type  date 0 / total 1 / is periodic  2/ period 3 / percent  4/ / purpose  5
                print(period)
                self.terminal.create_and_load_transaction(_transaction_type=type_of_transaction,
                                                          _date=date,
                                                          _total=total,
                                                          _periodic=True,
                                                          _period=period,
                                                          _percent=percent,
                                                          _purpose=purpose)

                self.update_last_transactions_box(F"@{self.dynamic_widgets['transaction'].title()}|"
                                                  F"@Date:{date}|@Total:{total}|@Period:{period}|"
                                                  F"@Percent:{percent}")

                self.close_popup(update_widgets=False)
                return
            elif type_of_transaction == "deposit" or type_of_transaction == "credit":
                percent = self.dynamic_widgets["percent"].get()

                period = self.dynamic_widgets["periodic_type"].get()
                if not percent or not period:
                    messagebox.showinfo("Warning",
                                        "The percentage and period fields must be filled")
                    return
                self.terminal.create_and_load_transaction(_transaction_type=type_of_transaction,
                                                          _date=date,
                                                          _total=total,
                                                          _percent=percent,
                                                          _purpose=purpose,
                                                          _period=period)

                self.update_last_transactions_box(F"@{self.dynamic_widgets['transaction'].title()}|"
                                                  F"@Date:{date}|@Total:{total}|@Period:{period}|"
                                                  F"@Percent:{percent}")
                self.close_popup(update_widgets=True)
            else:
                self.terminal.create_and_load_transaction(_transaction_type=type_of_transaction,
                                                          _date=date,
                                                          _total=total,
                                                          _purpose=purpose)

                self.update_last_transactions_box(F"@{self.dynamic_widgets['transaction'].title()}|"
                                                  F"@Date:{date}|@Total:{total}")
                self.close_popup(update_widgets=True)
        else:
            messagebox.showinfo("Warning", "THE DATE SHOULD BE IN DD.MM.YYYY FORMAT AND ALL FIELDS MUST BE FILLED")

    def check_password(self, pas, top):
        if pas == password:
            self.root.deiconify()
            self.close_popup(top)
            self.update_on_start()
        else:
            messagebox.showinfo("Warning", "Incorrect password")
            top.winfo_children()[1].delete(0, "end")

    def create_start_window(self):
        top = tk.Toplevel(self.root)
        top.geometry("300x300+600+200")
        top.title("Enter a password")

        password_label = tk.Label(top,
                                  text="Enter a password",
                                  font=Font(family='Courier New', size=20, weight='normal'))

        password_entry = tk.Entry(top,
                                  show="*",
                                  justify="center")

        check_btn = tk.Button(top,
                              text="Enter",
                              font=Font(family='Courier New', size=20, weight='normal'),
                              command=lambda: self.check_password(password_entry.get(), top))

        password_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        password_entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        check_btn.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

    def add_income_btn_clicked(self):
        top = self.create_basic_popup(width=400, height=260)
        top.title("Add income")
        self.configure_expense_income_popup(top)

        self.dynamic_widgets["transaction"] = "income"

        top.mainloop()

    def add_expense_btn_clicked(self):
        top = self.create_basic_popup(width=400, height=260)
        top.title("Add expense")
        self.configure_expense_income_popup(top)

        self.dynamic_widgets["transaction"] = "expense"
        top.mainloop()

    def put_deposit_btn_clicked(self):
        top = self.create_basic_popup(width=400, height=220)
        top.title("Deposit")
        self.configure_credit_deposit_popup(top)

        self.dynamic_widgets["transaction"] = "deposit"
        top.mainloop()

    def get_credit_btn_clicked(self):
        top = self.create_basic_popup(width=400, height=220)
        top.title("Credit")
        self.configure_credit_deposit_popup(top)

        self.dynamic_widgets["transaction"] = "credit"
        top.mainloop()

    # todo credits and filter and MAIN CANVAS WITH GRAPHICS
    def credits_btn_clicked(self):
        top = self.create_basic_popup(width=400, height=260)

        top.mainloop()

    def filter_btn_clicked(self):
        top = self.create_basic_popup(width=400, height=400)
        top.title("Filter")

        # для корректного задания размеров кнопки, вообще я считаю это костыль
        # но увы другие способы очень долгие (по фрейму на каждую кнопку, нет спасибо)
        pixel = tk.PhotoImage(width=300, height=50)
        custom_font = Font(family='Courier New', size=20, weight='normal')

        incomes_for_period_btn = tk.Button(top, text="Show income for period",
                                           image=pixel,
                                           command=lambda: self.incomes_for_period_clicked(top),
                                           bd=0,
                                           highlightthickness=0,
                                           compound="center",
                                           font=custom_font)

        expenses_for_period_btn = tk.Button(top, text="Show expense for period",
                                            image=pixel,
                                            command=lambda: self.expenses_for_period_clicked(top),
                                            bd=0,
                                            highlightthickness=0,
                                            compound="center",
                                            font=custom_font)

        term_forecast_btn = tk.Button(top, text="Term forecast",
                                      image=pixel,
                                      command=lambda: self.term_forecast_clicked_handler(top),
                                      bd=0,
                                      highlightthickness=0,
                                      compound="center",
                                      font=custom_font)

        filter_by_sum_diapason_btn = tk.Button(top, text="Filter by sum diapason",
                                               image=pixel,
                                               command=lambda: self.filter_by_sum_diapason_clicked(top),
                                               bd=0,
                                               highlightthickness=0,
                                               compound="center",
                                               font=custom_font)

        show_all_transactions_btn = tk.Button(top, text="Show all transactions",
                                              image=pixel,
                                              command=lambda: self.show_all_transaction_clicked(top),
                                              bd=0,
                                              highlightthickness=0,
                                              compound="center",
                                              font=custom_font)

        incomes_for_period_btn.place(x=50, y=25)
        expenses_for_period_btn.place(x=50, y=95)
        term_forecast_btn.place(x=50, y=165)
        filter_by_sum_diapason_btn.place(x=50, y=235)
        show_all_transactions_btn.place(x=50, y=305)

        top.mainloop()

    @staticmethod
    def create_tree_view_popup(parent):
        tree_view_popup = tk.Toplevel(parent)
        tree_view_popup.resizable(False, False)

        tree_view_popup.geometry("870x600+200+200")
        tree_view_frame = tk.Frame(tree_view_popup,
                                   height=600,
                                   width=870)
        tree = ttk.Treeview(tree_view_frame, height=600)
        # date / total / is_periodic / period / percent / purpose
        tree["columns"] = ("total", "is_periodic", "period", "percent", "purpose")

        tree.heading("#0", text="Date")
        tree.heading("total", text="Total")
        tree.heading("is_periodic", text="Is periodic?")
        tree.heading("period", text="Period")
        tree.heading("percent", text="Percent")
        tree.heading("purpose", text="Purpose")

        tree.column("#0",
                    width="120",
                    minwidth="120",
                    anchor="center")
        for item in tree["columns"]:
            tree.column(F"{item}",
                        width="120",
                        minwidth="120",
                        anchor="center")
        tree.column("purpose",
                    width="250",
                    minwidth="200",
                    anchor="center")

        tree_view_frame.pack(expand=False)
        tree.place(x=0, y=0, width=850, height=600)

        scrollbar = ttk.Scrollbar(tree_view_frame, orient="vertical", command=tree.yview)
        scrollbar.place(x=850, y=0, height=600)
        tree.configure(yscrollcommand=scrollbar.set)

        return tree_view_popup

    def get_data_by_date(self, type_, begin, end, parent):
        fetch_by_type = {
            "income": self.filter.get_incomes_for_period,
            "expense": self.filter.get_expenses_for_period
        }
        if self.do_date_validation(begin) and self.do_date_validation(end):

            data = fetch_by_type[type_](begin, end)
            if data:
                tree_view_popup = self.create_tree_view_popup(parent)
                tree = tree_view_popup.winfo_children()[0].winfo_children()[0]

                for date in data:
                    for params in date[1]:
                        payload = (
                            params["total"],
                            params["is_periodic"],
                            params["period"],
                            params["percent"],
                            params["purpose"]
                        )
                        tree.insert("",
                                    "end",
                                    text=date[0],
                                    values=payload)
                tree_view_popup.mainloop()
            else:
                messagebox.showinfo("Nothing to show", "No transactions found")

        else:
            messagebox.showinfo("Incorrect date format",
                                "THE DATE SHOULD BE IN DD.MM.YYYY FORMAT AND ALL FIELDS MUST BE FILLED")

    def get_data_by_sum(self, lower_bound, upper_bound, parent):
        print(type(lower_bound))
        if self.do_digits_validation(lower_bound) and self.do_digits_validation(upper_bound):
            data = self.filter.filter_by_sum_diapason(lower_bound, upper_bound)
            if data:
                tree_view_popup = self.create_tree_view_popup(parent)
                tree = tree_view_popup.winfo_children()[0].winfo_children()[0]
                print(data)
                for date in data:
                    for params in date[1]:
                        payload = (
                            params["total"],
                            params["is_periodic"],
                            params["period"],
                            params["percent"],
                            params["purpose"]
                        )
                        tree.insert("",
                                    "end",
                                    text=F"{params['type']} | {date[0]}",
                                    values=payload)
                tree_view_popup.mainloop()
            else:
                messagebox.showinfo("Nothing to show", "No transactions found")
        else:
            messagebox.showinfo("Incorrect sum format", "The amount must be in float format, e.g. '175.35'")

    def create_select_date_window(self, parent, type_):
        top = tk.Toplevel(parent)
        top.geometry("337x150+500+200")
        custom_font = Font(family='Courier New', size=20, weight='normal')

        begin_label = tk.Label(top,
                               text="START DATE",
                               font=custom_font)
        begin_entry = tk.Entry(top,
                               font=custom_font,
                               validate="key",
                               validatecommand=self.dot_and_digit_validation,
                               width=12,
                               justify="center")

        end_label = tk.Label(top,
                             text="END DATE",
                             font=custom_font)

        end_entry = tk.Entry(top,
                             font=custom_font,
                             validate="key",
                             validatecommand=self.dot_and_digit_validation,
                             width=12,
                             justify="center")

        show_btn = tk.Button(top,
                             text="Show",
                             font=custom_font,
                             command=lambda: self.get_data_by_date(F"{type_}", begin_entry.get(), end_entry.get(), top),
                             width=10,
                             height=2)

        begin_label.place(relx=0.05, rely=0.05)
        begin_entry.place(relx=0, rely=0.2)

        end_label.place(relx=0.6, rely=0.05)
        end_entry.place(relx=0.5, rely=0.2)

        show_btn.place(relx=0.3, rely=0.5)
        return top

    def create_select_sum_window(self, parent):
        top = tk.Toplevel(parent)
        top.geometry("337x150+500+200")
        custom_font = Font(family='Courier New', size=20, weight='normal')

        begin_label = tk.Label(top,
                               text="LOWER BOUND",
                               font=custom_font)
        begin_entry = tk.Entry(top,
                               font=custom_font,
                               validate="key",
                               validatecommand=self.dot_and_digit_validation,
                               width=12,
                               justify="center")

        end_label = tk.Label(top,
                             text="UPPER BOUND",
                             font=custom_font)

        end_entry = tk.Entry(top,
                             font=custom_font,
                             validate="key",
                             validatecommand=self.dot_and_digit_validation,
                             width=12,
                             justify="center")

        show_btn = tk.Button(top,
                             text="Show",
                             font=custom_font,
                             command=lambda: self.get_data_by_sum(float(begin_entry.get()), float(end_entry.get()), top),
                             width=10,
                             height=2)

        begin_label.place(relx=0.05, rely=0.05)
        begin_entry.place(relx=0, rely=0.2)

        end_label.place(relx=0.55, rely=0.05)
        end_entry.place(relx=0.5, rely=0.2)

        show_btn.place(relx=0.3, rely=0.5)
        return top

    def create_forecast_window(self, parent, forecast_date):
        if self.do_date_validation(forecast_date):
            top = tk.Toplevel(parent)
            top.resizable(False, False)
            top.title("Forecast")
            top.geometry("1200x600+50+200")
            # get forecast data
            forecast = list(self.filter.term_forecast(forecast_date))

            # bar graph setup
            labels = ["Income", "Expense"]
            width = 0.75
            x = np.arange(len(labels))
            bar, ax = plt.subplots(figsize=(6, 6))
            ax.set_title(F"Forecast for {forecast_date}")
            ax.set_ylabel("Total")

            rect_income = ax.bar(0, forecast[0], width, label="Income")
            rect_expense = ax.bar(1, forecast[1], width, label="Expense")



            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            canvas = FigureCanvasTkAgg(bar, top)

            total_label = tk.Label(top,
                                   text=F"Expected total: {forecast[0]-forecast[1]}",
                                   font=self.main_font)

            current_total_label = tk.Label(top,
                                           text=F"Current total: {self.terminal.get_total_income()}",
                                           font=self.main_font)

            income_label = tk.Label(top,
                                    text=F"Expected income: {forecast[0]}",
                                    font=self.main_font)

            expence_label = tk.Label(top,
                                     text=F"Expected expense: {forecast[1]}",
                                     font=self.main_font)

            canvas.get_tk_widget().place(x=0, y=0)
            total_label.place(x=580, y=150)
            current_total_label.place(x=580, y=200)
            income_label.place(x=580, y=250)
            expence_label.place(x=580, y=300)

        else:
            messagebox.showerror("Incorrect date", "The date should be entered in dd.mm.YYYY format")

    def incomes_for_period_clicked(self, parent):
        top = self.create_select_date_window(parent, "income")
        top.title("Expense for period")

        top.mainloop()

    def expenses_for_period_clicked(self, parent):
        top = self.create_select_date_window(parent, "expense")
        top.title("Expense for period")

        top.mainloop()

    def term_forecast_clicked_handler(self, parent):
        top = tk.Toplevel(parent)
        top.resizable(False, False)
        top.geometry("200x100+600+300")
        top.title("Forecast")

        date_label = tk.Label(top,
                              text="Forecast date",
                              font=self.main_font)

        date_entry = tk.Entry(top,
                              font=self.main_font,
                              validate="key",
                              validatecommand=self.dot_and_digit_validation,
                              width=12,
                              justify="center")

        forecast_btn = tk.Button(top,
                                 text="Forecast",
                                 font=self.main_font,
                                 width=12,
                                 justify="center",
                                 command=lambda: self.create_forecast_window(top, date_entry.get()))

        date_label.pack(anchor="center")
        date_entry.pack(anchor="center")
        forecast_btn.pack(anchor="center")
        top.mainloop()

    def filter_by_sum_diapason_clicked(self, parent):
        top = self.create_select_sum_window(parent)
        top.title("Get by sum diapason")

        top.mainloop()

    def show_all_transaction_clicked(self, parent):
        tree_view_popup = self.create_tree_view_popup(parent)
        tree_view_popup.title("All transactions")
        tree = tree_view_popup.winfo_children()[0].winfo_children()[0]
        data = self.filter.get_all_transactions()
        for date in data:
            print(date[1])
            for params in date[1]:
                payload = (
                    params["total"],
                    params["is_periodic"],
                    params["period"],
                    params["percent"],
                    params["purpose"]
                )
                tree.insert("",
                            "end",
                            text=F"{params['type']} | {date[0]}",
                            values=payload)

        tree_view_popup.mainloop()

    def update_on_start(self):
        self.update_pie_chart()
        self.update_income()
        self.update_expense()
        self.update_total()

    def update_pie_chart(self):
        self.a.clear()
        self.a.pie([self.terminal.get_total_income(), self.terminal.get_total_expense()],
                   labels=["Income", "Expenses"],
                   autopct='%1.1f%%',
                   colors=["#d6f5d6", "#ffcccc"])
        self.pie_chart.canvas.draw_idle()

    def update_total(self):
        self.total_label["text"] = F"Total:{self.terminal.get_total_overall()}$"

    def update_income(self):
        self.income_label["text"] = F"Income:{self.terminal.get_total_income()}$"

    def update_expense(self):
        self.expense_label["text"] = F"Expense:{self.terminal.get_total_expense()}$"

    def save_all(self):
        self.terminal.save_all()
        self.root.quit()


gui = GUI(budget.Terminal())
gui.root.mainloop()



