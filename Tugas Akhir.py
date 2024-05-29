import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class LoginApp:
    def __init__(self, master, on_login_success):
        self.master = master
        self.master.title("Login")
        self.master.geometry("500x250")

        self.on_login_success = on_login_success

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.pack(pady=7)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=7)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.pack(pady=7)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=7)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack(pady=15)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack(pady=7)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_credentials(username, password):
            self.master.destroy()
            self.on_login_success()
        else:
            self.status_label.config(text="Login failed. Please try again.")

    def validate_credentials(self, username, password):
        return username == "admin" and password == "1234"

class FileManagerApp:
    def __init__(self, master, on_logout):
        self.master = master
        self.master.title("Pengelola File")

        self._current_path = os.getcwd()
        self.on_logout = on_logout

        self.path_label = tk.Label(self.master, text="Path: " + self._current_path)
        self.path_label.pack(pady=10)

        self.file_listbox = tk.Listbox(self.master, width=75, height=25)
        self.file_listbox.pack()

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.open_button = tk.Button(self.button_frame, text="Buka", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Hapus", command=self.delete_file)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.move_button = tk.Button(self.button_frame, text="Pindahkan", command=self.move_file)
        self.move_button.grid(row=0, column=2, padx=5)

        self.change_dir_button = tk.Button(self.button_frame, text="Pindah Folder", command=self.change_directory)
        self.change_dir_button.grid(row=0, column=3, padx=5)

        self.back_button = tk.Button(self.button_frame, text="Kembali", command=self.back_directory)
        self.back_button.grid(row=0, column=4, padx=5)

        self.logout_button = tk.Button(self.button_frame, text="Log Out", command=self.logout)
        self.logout_button.grid(row=0, column=5, padx=5)

        self.update_file_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self._current_path):
            self.file_listbox.insert(tk.END, item)
        self.path_label.config(text="Path: " + self._current_path)

    def open_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            file_path = os.path.join(self._current_path, selected_item)
            if os.path.isdir(file_path):
                self.set_current_path(file_path)
            else:
                os.startfile(file_path)
        else:
            messagebox.showwarning("Peringatan", "Silakan pilih berkas yang ingin dibuka!")

    def delete_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            file_path = os.path.join(self._current_path, selected_item)
            if os.path.isdir(file_path):
                try:
                    os.rmdir(file_path)
                except OSError as e:
                    messagebox.showerror("Error", f"Gagal menghapus direktori: {e}")
            else:
                try:
                    os.remove(file_path)
                except OSError as e:
                    messagebox.showerror("Error", f"Gagal menghapus berkas: {e}")
            self.update_file_list()
        else:
            messagebox.showwarning("Peringatan", "Silakan pilih berkas yang ingin dihapus!")

    def move_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            file_path = os.path.join(self._current_path, selected_item)
            destination_path = filedialog.askdirectory()
            if destination_path:
                try:
                    shutil.move(file_path, os.path.join(destination_path, selected_item))
                    self.update_file_list()
                except shutil.Error as e:
                    messagebox.showerror("Error", f"Gagal memindahkan berkas: {e}")
        else:
            messagebox.showwarning("Peringatan", "Silakan pilih berkas yang ingin dipindahkan!")

    def change_directory(self):
        new_path = filedialog.askdirectory()
        if new_path:
            self.set_current_path(new_path)

    def back_directory(self):
        new_path = os.path.dirname(self._current_path)
        if new_path != self._current_path:  
            self.set_current_path(new_path)
        else:
            messagebox.showwarning("Peringatan", "Tidak ada direktori sebelumnya.")

    def get_current_path(self):
        return self._current_path

    def set_current_path(self, new_path):
        self._current_path = new_path
        self.update_file_list()

    def logout(self):
        self.master.destroy()
        self.on_logout()

def main():
    def on_login_success():
        root = tk.Tk()
        FileManagerApp(root, on_logout=show_login)
        root.mainloop()

    def show_login():
        login_root = tk.Tk()
        LoginApp(login_root, on_login_success)
        login_root.mainloop()

    show_login()

if __name__ == "__main__":
    main()
