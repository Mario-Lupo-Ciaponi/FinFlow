import customtkinter as ctk
import psycopg2 # Connection to database
from tkinter import messagebox
from string import capwords


def get_connection():
    """
        This function returns a connection to the database of the app.
    """
    try:
        return  psycopg2.connect(
        dbname="fin_flow_db",
        user="postgres",
        password="Ps1029384756,.",
        host="localhost",
        port="5432"
        )
    except psycopg2.Error:
        return None


class FinFlowApp(ctk.CTk):
    TYPES = ["income", "expense"]
    TABLE_NAME = "transactions"

    def __init__(self):
        super().__init__()

        # Set themes
        self.theme = "dark"
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme("blue")

        self.bind("<Escape>", self.close_window)

        self.resizable(False, False)

        self.title("Fin Flow")
        self.geometry("400x530")

        self.label_to_add = ctk.CTkLabel(self, text="Type the income/expense:", font=("Helvetica", 20, "bold"))
        self.label_to_add.pack(pady=25)

        # Amount:
        self.label_for_instruction_amount = ctk.CTkLabel(self, text="Type amount:") # Label to let the user know what to type
        self.label_for_instruction_amount.pack()

        self.entry_for_amount= ctk.CTkEntry(self)
        self.entry_for_amount.pack(pady=10)
        self.entry_for_amount.bind("<Return>", self.on_enter)
        self.entry_for_amount.bind("<Down>", self.focus_on_next_widget)

        # Reason
        self.label_for_reason = ctk.CTkLabel(self, text="Type reason:")  # Label to let the user know what to type
        self.label_for_reason.pack()

        self.entry_for_reason = ctk.CTkEntry(self, width=150)
        self.entry_for_reason.pack(pady=10)
        self.entry_for_reason.bind("<Return>", self.on_enter)
        self.entry_for_reason.bind("<Up>", self.focus_on_previous_widget)

        self.option_menu_for_options = ctk.CTkOptionMenu(self,
                                                     values=self.TYPES,
                                                     width=100,
                                                     button_hover_color="#81878c")


        self.option_menu_for_options.pack(pady=20)

        self.button_to_add = ctk.CTkButton(self,
                                           text="+Add",
                                           command=self.add_record,
                                           font=("Helvetica", 15),
                                           corner_radius=40,
                                           fg_color="#1E88E5",
                                           hover_color="#007BFF",
                                           border_width=2,
                                           border_color="#1b72b5",
                                           height=30,
                                           width=80)
        self.button_to_add.pack(pady=30)

        self.button_for_records = ctk.CTkButton(self,
                                                text="Show transactions",
                                                command=self.show_records,
                                                font=("Helvetica", 10),
                                                width=90,
                                                corner_radius=20,
                                                fg_color="#0e5c23",
                                                hover_color="#0a3315")
        self.button_for_records.pack(pady=20)

        self.change_theme_button = ctk.CTkButton(self,
                                                 text="☀️",
                                                 command=self.change_theme,
                                                 font=("Helvetica", 10),
                                                 width=20,
                                                 corner_radius=60)
        self.change_theme_button.pack(pady=20)

    def on_enter(self, event=None):
        self.add_record()

    @staticmethod
    def focus_on_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    @staticmethod
    def focus_on_previous_widget(event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def close_window(self, event=None):
        self.destroy()

    def change_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        ctk.set_appearance_mode(self.theme)
        self.change_theme_button.configure(text=f"{"🌙" if self.theme == "light" else "☀️"}")


    def add_record(self):
        conn = None
        cursor = None

        try:
            amount_of_money = float(self.entry_for_amount.get())
            reason_for_transaction = self.entry_for_reason.get()
            type_of_transaction = self.option_menu_for_options.get()

            if reason_for_transaction == "":
                messagebox.showerror("Error", "'Reason' field is empty!")
                return


            conn = get_connection()
            cursor = conn.cursor()

            insert_into_transactions_query = f"INSERT INTO {self.TABLE_NAME} (amount, reason, type) VALUES(%s, %s, %s);"

            cursor.execute(insert_into_transactions_query, (amount_of_money,
                                                            reason_for_transaction,
                                                            type_of_transaction))

            conn.commit() # If everything is successful, the changes will be commited to the table.
        except ValueError:
            messagebox.showerror("Error", "'Amount' must be of float type!")
        except psycopg2.Error:
            messagebox.showerror("Error", f"There was a problem with the transaction.")

            if conn:
                conn.rollback() # To rollback and the transaction won't be made.
        else:
            # Message to let the user know that the record is registered.
            messagebox.showinfo("Success",
                                f"{capwords(type_of_transaction)} added successfully!")
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()

    def does_query_exist(self, cursor, id):
        select_query = f"SELECT id FROM {self.TABLE_NAME} WHERE id = %s;"
        cursor.execute(select_query, (id,))  # Pass id as a tuple
        result = cursor.fetchone()  # Fetch only one row

        return result is not None  # Return True if a row is found, otherwise False

    def show_records(self):
        def sum_transactions():
            type_wanted = selected_value.get().lower()

            conn = get_connection()
            cursor = conn.cursor()

            select_query = f"SELECT SUM(amount) FROM {self.TABLE_NAME}"
            date_filter = ""
            filter_date = False

            if date_entry.get() != "":
                date_filter = date_entry.get()
                filter_date = True

            if type_wanted in ["income", "expense"]:
                select_query += " WHERE type = %s"

                if filter_date:
                    select_query += " AND date::DATE = %s"
                    cursor.execute(select_query, (type_wanted, date_filter))
                else:
                    cursor.execute(select_query, (type_wanted,))
            else:
                if filter_date:
                    select_query += " WHERE date::DATE = %s"
                    cursor.execute(select_query, (date_filter,))
                else:
                    cursor.execute(select_query)

            sum_of_transactions = cursor.fetchone()[0]

            if sum_of_transactions is None:
                messagebox.showerror("Error", f"There are no {type_wanted}s!")
            else:
                messagebox.showinfo("Sum", f"The sum is {sum_of_transactions}")


        def refresh_transactions():
            """Function to refresh transaction list based on filter selection."""
            type_wanted = selected_value.get().lower()

            conn = get_connection()
            cursor = conn.cursor()

            # Clear previous transaction labels
            for widget in scroll_frame_for_transaction.winfo_children():
                widget.destroy()

            select_query = f"SELECT id, amount, reason, type, TO_CHAR(date, 'YYYY.MM.DD - HH24:MI:SS') FROM {self.TABLE_NAME}"

            if type_wanted in ["income", "expense"]:
                select_query += " WHERE type = %s"
                cursor.execute(select_query, (type_wanted,))
            else:
                cursor.execute(select_query)  # If "All" is selected, show everything

            transactions = cursor.fetchall()

            if transactions:
                for id, amount, reason, type_of_transaction, date in transactions:
                    label_info = ctk.CTkLabel(scroll_frame_for_transaction, text=f"ID: {id}; "
                                                                                 f"Amount: {amount}; "
                                                                                 f"Reason: {reason}; "
                                                                                 f"Type: {type_of_transaction}; "
                                                                                 f"Date: {date}")
                    label_info.pack(pady=10)
            else:
                label_info = ctk.CTkLabel(scroll_frame_for_transaction, text="No transactions found.",
                                          font=("Helvetica", 20))
                label_info.pack(pady=10)

            cursor.close()
            conn.close()

        def delete_transaction():
            conn_to_db = None
            cursor_to_db = None

            try:
                conn_to_db = get_connection()
                cursor_to_db = conn_to_db.cursor()

                id = entry_for_delete.get()

                if not self.does_query_exist(cursor_to_db, id):
                    raise ValueError

                answer_for_measure = messagebox.askyesno("Are you sure?", "Are you sure you want to delete?")

                if answer_for_measure:
                    delete_query = f"DELETE FROM {self.TABLE_NAME} WHERE id = %s;"

                    cursor_to_db.execute(delete_query, (id,))
                    conn_to_db.commit()
                else:
                    messagebox.showinfo("Denied", f"Transactions was not deleted.")
                    return
            except psycopg2.Error:
                messagebox.showerror("Error", "There was an error with the transactions.")
                conn_to_db.rollback()
            except ValueError:
                messagebox.showerror("Error", "Transaction does not exist!")
            else:
                messagebox.showinfo("Success", "Transaction deleted successfully!")
                refresh_transactions()
            finally:
                if conn_to_db:
                    conn_to_db.close()
                if cursor_to_db:
                    cursor_to_db.close()

        def close_record_window(event=None):
            records_window.destroy()

        # Create a new window for transactions
        records_window = ctk.CTkToplevel(self)
        records_window.title("Transactions")
        records_window.geometry("730x900")
        records_window.resizable(False, False)
        records_window.bind("<Escape>", close_record_window)

        label_transactions = ctk.CTkLabel(records_window, text="Transactions:", font=("Helvetica", 35, "bold"))
        label_transactions.pack(pady=30)

        filter_options = ["All", "Income", "Expense"]
        selected_value = ctk.StringVar(value="All")

        label_filter = ctk.CTkLabel(records_window, text="Filter by Type:")
        label_filter.pack()

        combo_box_for_filter = ctk.CTkComboBox(records_window, values=filter_options, variable=selected_value)
        combo_box_for_filter.pack(pady=20)

        label_date_filter = ctk.CTkLabel(records_window, text="Filter by Date:")
        label_date_filter.pack()

        date_entry = ctk.CTkEntry(records_window, placeholder_text="YYYY-MM-DD")
        date_entry.pack(pady=20)

        # Attach event to combo box to refresh transactions on change
        selected_value.trace_add("write", lambda *args: refresh_transactions())

        scroll_frame_for_transaction = ctk.CTkScrollableFrame(records_window, width=630, height=280)
        scroll_frame_for_transaction.pack(pady=15)

        label_delete_by_id = ctk.CTkLabel(records_window, text="Delete transaction by entering id:",
                                          text_color="#d90902")
        label_delete_by_id.pack(pady=10)

        entry_for_delete = ctk.CTkEntry(records_window, width=40)
        entry_for_delete.pack()

        button_to_delete = ctk.CTkButton(records_window, text="🗑️ DELETE", fg_color="#D32F2F", corner_radius=20, width=20,
                                         hover_color="#B71C1C", command=delete_transaction)
        button_to_delete.pack(pady=20)

        get_sum_button = ctk.CTkButton(records_window, text="Get sum", fg_color="Blue", corner_radius=20, width=30,
                                         hover_color="#0e096e", command=sum_transactions)
        get_sum_button.pack(pady=27)

        # Initial load of transactions
        refresh_transactions()


def main():
    fin_flow_app = FinFlowApp()
    fin_flow_app.mainloop()


if __name__ == "__main__":
    main()
