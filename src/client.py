import socket
import threading
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class loginPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("Login")

        self.mainFrame = ctk.CTkFrame(master=self, width=760, height=540)
        self.mainFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.loginLabel = ctk.CTkLabel(master=self.mainFrame, text="Login:", font=('Calibri', 20))
        self.loginLabel.place(relx=0.335, rely=0.315, anchor=tk.CENTER)

        self.loginEntryUser = ctk.CTkEntry(master=self.mainFrame, placeholder_text="Username:", width=324, height=50,
                                           corner_radius=15)
        self.loginEntryUser.place(relx=0.5, rely=0.41, anchor=tk.CENTER)

        self.loginEntryPassword = ctk.CTkEntry(master=self.mainFrame, placeholder_text="Password:", width=324, height=50
                                               ,corner_radius=15)
        self.loginEntryPassword.place(relx=0.5, rely=0.51, anchor=tk.CENTER)

        self.loginButton = ctk.CTkButton(master=self.mainFrame, text="Login", width=108, height=40, corner_radius=15,
                                         command=self.confirm_credentials_to_db)
        self.loginButton.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

        self.signupButton = ctk.CTkButton(master=self.mainFrame, text="Signup", width=108, height=40, corner_radius=15,
                                          command=lambda: self.to_signup_page())
        self.signupButton.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

        self.exitButton = ctk.CTkButton(master=self.mainFrame, text="Exit app", width=108, height=40, corner_radius=15
                                          , fg_color='red', command=self.exit_app)
        self.exitButton.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.bind("<Configure>", self.on_maximize)

    def confirm_credentials_to_db(self):
        username = self.loginEntryUser.get()
        password = self.loginEntryPassword.get()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(("localhost", 9999))

            # Send username and password to the server
            message = f"CHECK_CREDENTIALS {username} {password}"
            client_socket.send(message.encode('utf-8'))

            # Receive response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(response)

    def to_signup_page(self, event):
        self.destroy()
        signUp = signupPage()
        signUp.mainloop()

    def exit_app(self):
        self.destroy()

    def on_maximize(self, event):
        # Prevent the window from being maximized
        event.widget.state('normal')

class signupPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("Sign Up")

        self.mainFrame = ctk.CTkFrame(master=self, width=760, height=540)
        self.mainFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.signupLabel = ctk.CTkLabel(master=self.mainFrame, text="Sign Up:", font=('Calibri', 20))
        self.signupLabel.place(relx=0.335, rely=0.315, anchor=tk.CENTER)

        self.signEntryUser = ctk.CTkEntry(master=self.mainFrame, placeholder_text="Username:", width=324, height=50,
                                           corner_radius=15)
        self.signEntryUser.place(relx=0.5, rely=0.41, anchor=tk.CENTER)

        self.signEntryPassword = ctk.CTkEntry(master=self.mainFrame, placeholder_text="Password:", width=324, height=50
                                               , corner_radius=15)
        self.signEntryPassword.place(relx=0.5, rely=0.51, anchor=tk.CENTER)

        self.loginButton = ctk.CTkButton(master=self.mainFrame, text="Login", width=108, height=40, corner_radius=15,
                                         command=self.confirm_credentials_to_db)
        self.loginButton.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

        self.signupButton = ctk.CTkButton(master=self.mainFrame, text="Signup", width=108, height=40, corner_radius=15)
        self.signupButton.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

        self.exitButton = ctk.CTkButton(master=self.mainFrame, text="Exit app", width=108, height=40, corner_radius=15
                                          , fg_color='red', command=self.exit_app)
        self.exitButton.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = loginPage()
    app.mainloop()
