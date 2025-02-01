import customtkinter as ctk
import psycopg2 # Connection to database
from tkinter import messagebox
from string import capwords


def get_connection():
    return  psycopg2.connect(
    dbname="fin_flow_db",
    user="postgres",
    password="Ps1029384756,.",
    host="localhost",
    port="5432"
    )

# Set themes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FinFlowApp(ctk.CTk):
    TYPES = ["income", "expense"]

    def __init__(self):
        super().__init__()

        self.title("Fin Flow")
        self.geometry("400x400")

        self.label_to_add = ctk.CTkLabel(self, text="Type the income/expense:", font=("Helvetica", 20))
        self.label_to_add.pack(pady=20)

        # Amount:
        self.label_for_instruction_amount = ctk.CTkLabel(self, text="Type amount:") # Label to let the user know what to type
        self.label_for_instruction_amount.pack()

        self.entry_for_amount= ctk.CTkEntry(self)
        self.entry_for_amount.pack(pady=10)

        # Reason
        self.label_for_reason = ctk.CTkLabel(self, text="Type reason:")  # Label to let the user know what to type
        self.label_for_reason.pack()

        self.entry_for_reason = ctk.CTkEntry(self, width=150)
        self.entry_for_reason.pack(pady=10)

        self.combo_box_for_options = ctk.CTkComboBox(self,
                                                     values=self.TYPES,
                                                     width=100,
                                                     border_width=2,
                                                     button_hover_color="#81878c",
                                                     justify="center")
        self.combo_box_for_options.pack(pady=20)

        self.button_to_add = ctk.CTkButton(self,
                                           text="Add",
                                           command=self.add_record,
                                           font=("Helvetica", 15),
                                           corner_radius=40,
                                           border_width=2,
                                           border_color="#1b72b5",
                                           height=30,
                                           width=80)
        self.button_to_add.pack(pady=20)

    def add_record(self):
        amount = float(self.entry_for_amount.get())
        reason = str(self.entry_for_reason.get())
        type_of_action = self.combo_box_for_options.get()

        cursor = None
        connection_to_db = None

        try:
            connection_to_db = get_connection()
            if connection_to_db is None:
                print("Failed to connect to the database.")
                return

            cursor = connection_to_db.cursor()

            query = "INSERT INTO transactions(amount, reason, type) VALUES (%s, %s, %s)"
            cursor.execute(query, (amount, reason, type_of_action))

            connection_to_db.commit()

            messagebox.showinfo("Success!", f"{capwords(type_of_action)} added successfully!")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error occured while adding {type_of_action}")
            if connection_to_db:
                connection_to_db.rollback()

        finally:
            if cursor:
                cursor.close()

            if connection_to_db:
                connection_to_db.close()


def main():
    fin_flow_app = FinFlowApp()
    fin_flow_app.mainloop()


if __name__ == "__main__":
    main()
