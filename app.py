import customtkinter as ctk
from connection import *  # Connection to database

# Set themes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FinFlowApp(ctk.CTk):
    TYPES = ["gain", "expense"]

    def __init__(self):
        super().__init__()

        self.title("Fin Flow")
        self.geometry("400x400")

        self.label_to_add = ctk.CTkLabel(self, text="Type the expense/gain:", font=("Helvetica", 20))
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
                                           command=self.print_message,
                                           font=("Helvetica", 15),
                                           corner_radius=40,
                                           border_width=2,
                                           border_color="#1b72b5",
                                           height=30,
                                           width=80)
        self.button_to_add.pack(pady=20)

    def print_message(self):
        pass


def main():
    fin_flow_app = FinFlowApp()
    fin_flow_app.mainloop()


if __name__ == "__main__":
    main()
