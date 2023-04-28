import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import re
from database_connection import *
import util as v

class HomeScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Form Filling App")
        self.master.geometry("400x400")
        self.master.resizable(False, False)
        self.configure(bg='white')
        logo_image = Image.open("icon.png")  # Replace with the path to your logo image
        logo_image = logo_image.resize((150, 150))  # Resize the image to desired dimensions
        self.logo = ImageTk.PhotoImage(logo_image)
        self.create_widgets()
        
    def create_widgets(self):
        # Create logo label
        logo_label = tk.Label(self, image=self.logo, bg='white')
        logo_label.pack(pady=20)

        # Create button to go to form
        form_button = tk.Button(self, text="Fill Form", command=self.go_to_form, font=("Helvetica", 14), width=20)
        form_button.pack(pady=10)

        # Create button to go to view details
        view_details_button = tk.Button(self, text="View Details", command=self.go_to_view_details, font=("Helvetica", 14), width=20)
        view_details_button.pack(pady=10)
        
        # Create button to ask user
        ask_user_button = tk.Button(self, text="Voice mode", command=self.ask_user_thread, font=("Helvetica", 14), width=20)
        ask_user_button.pack(pady=10)

    def go_to_form(self):
        self.master.switch_frame(FormScreen)

    def ask_user_id(self, message):
        v.speak(message)
        data = v.listen()
        return data
    
    def go_to_view_details(self):
        self.get_user()
    
    def get_user(self):
        self.ID = self.ask_user_id("Please say your ID")
        try:
            self.ID = int(self.ID)
            details = fetchRecords(getConnection(), self.ID)[0]
            message = "ID: " + str(details[0]) + "\nFirst Name: " + details[1] + "\nLast Name: " + details[2] + "\nPhone: " + details[3] + + "\nDate of Birth: " + details[4] + "\nGender: " + details[5]
            messagebox.showinfo("Details", message)
        except:
            messagebox.showerror("Error", "Invalid ID") 
    
    def ask_user_thread(self):
        thread = v.ThreadWithReturnValue(target=self.ask_user).start()
    
    def ask_user(self):
        v.speak("What would you like to do? Fill form or view details?")
        data = v.listen()
        data = data.lower()
        if data == "fill form":
            self.go_to_form()
            speakThread = v.ThreadWithReturnValue(target=v.speak, args=("Opening form",)).start()
        elif data == "view details":
            self.go_to_view_details()
        else:
            speakThread = v.ThreadWithReturnValue(target=v.speak, args=("Sorry, I didn't get that. Cancelling voice mode.",)).start()

class FormScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Form Screen")
        self.create_form()
        
    def create_form(self):
        WINDOW_WIDTH = 450
        WINDOW_HEIGHT = 450
        SCREEN_WIDTH = self.master.winfo_screenwidth()
        SCREEN_HEIGHT = self.master.winfo_screenheight()
        X_POS = (SCREEN_WIDTH // 2) - (WINDOW_WIDTH // 2)
        Y_POS = (SCREEN_HEIGHT // 2) - (WINDOW_HEIGHT // 2)
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{X_POS}+{Y_POS}")

        FONT_SIZE = 12

        rootFrame = tk.Frame(self, padx=30, pady=30)
        rootFrame.pack(expand=True, fill=tk.BOTH)

        # Create labels for form fields with larger font size
        label_firstname = tk.Label(rootFrame, text="First Name:", font=("Helvetica", FONT_SIZE))
        label_lastname = tk.Label(rootFrame, text="Last Name:", font=("Helvetica", FONT_SIZE))
        label_DOB = tk.Label(rootFrame, text="Date of Birth:", font=("Helvetica", FONT_SIZE))
        label_phone = tk.Label(rootFrame, text="Phone:", font=("Helvetica", FONT_SIZE))
        label_gender = tk.Label(rootFrame, text="Gender:", font=("Helvetica", FONT_SIZE))

        # Create entry fields for form data with larger font size
        self.entry_firstname = tk.Entry(rootFrame, font=("Helvetica", FONT_SIZE))
        self.entry_lastname = tk.Entry(rootFrame, font=("Helvetica", FONT_SIZE))
        self.entry_phone = tk.Entry(rootFrame, font=("Helvetica", FONT_SIZE))

        # Date picker for DOB
        self.dob_var = tk.StringVar()
        dob_picker = DateEntry(rootFrame, textvariable=self.dob_var, font=("Helvetica", FONT_SIZE), width=18, date_pattern="dd/mm/yyyy")

        # radio buttons for gender
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        radio_male = tk.Radiobutton(rootFrame, text="Male", variable=self.gender_var, value="Male", font=("Helvetica", FONT_SIZE))
        radio_female = tk.Radiobutton(rootFrame, text="Female", variable=self.gender_var, value="Female", font=("Helvetica", FONT_SIZE))
        radio_other = tk.Radiobutton(rootFrame, text="Other", variable=self.gender_var, value="Other", font=("Helvetica", FONT_SIZE))
        
        # button to submit, clear form and another to go back to home screen
        submit_button = tk.Button(rootFrame, text="Submit", font=("Helvetica", FONT_SIZE), width=20, command=self.submit_form)
        clear_button = tk.Button(rootFrame, text="Clear", font=("Helvetica", FONT_SIZE), width=20, command=self.clear_form)
        home_button = tk.Button(rootFrame, text="Home", font=("Helvetica", FONT_SIZE), width=20, command=self.go_to_home)
        voice_button = tk.Button(rootFrame, text="Voice mode", font=("Helvetica", FONT_SIZE), width=20, command=self.ask_user)
        
        # Set margins for form fields
        label_firstname.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_firstname.grid(row=0, column=1, padx=10, pady=10)
        label_lastname.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_lastname.grid(row=1, column=1, padx=10, pady=10)
        label_DOB.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        dob_picker.grid(row=2, column=1, padx=10, pady=10)
        label_phone.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_phone.grid(row=3, column=1, padx=10, pady=10)
        label_gender.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        radio_male.grid(row=4, column=1, sticky=tk.W, padx=10, pady=3)
        radio_female.grid(row=5, column=1, sticky=tk.W, padx=10, pady=3)
        radio_other.grid(row=6, column=1, sticky=tk.W, padx=10, pady=3)
        submit_button.grid(row=7, column=0)
        clear_button.grid(row=7, column=1)
        home_button.grid(row=8, column=0)
        voice_button.grid(row=8, column=1)
        rootFrame.pack(expand=True, fill=tk.BOTH)
    
    def submit_form(self):
        # fetch all the data from the form
        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()
        phone = self.entry_phone.get()
        dob = self.dob_var.get()
        gender = self.gender_var.get()
        phone_pattern = re.compile(r"^[0-9]{10}$")
        name_pattern = re.compile(r"^[a-zA-Z]+$")
        if phone_pattern.match(phone) and name_pattern.match(firstname) and name_pattern.match(lastname):
            conn = getConnection()
            user = {
                'firstname': firstname,
                'lastname': lastname,
                'phone': phone,
                'gender': gender,
                'dob': dob
            }
            ID = insert(conn, user)
            if not ID:
                messagebox.showerror("Error", "Error adding user") 
            else:    
                messagebox.showinfo("Success", "User added successfully, ID: " + str(ID))
                self.clear_form()
        else:
            messagebox.showerror("Error", "Invalid data")
        
    def clear_form(self):
        self.entry_firstname.delete(0, tk.END)
        self.entry_lastname.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_firstname.focus()
    
    def go_to_home(self):
        self.master.switch_frame(HomeScreen)

    def ask_user(self):
        thread = v.ThreadWithReturnValue(target=self.ask_user_thread)
        thread.start()
    
    def ask_user_thread(self):
        messagebox.showinfo("Voice mode", "1. Please speak clearly and slowly\n2. If you want to edit any field, say 'Edit fieldname' and then speak the new value\n3. If you want to submit the form, say 'Submit form'\n4. If you want to go back to home screen, say 'Exit'\n5. If you want to clear the form, say 'Clear form'")
        fields = ['first name', 'last name', 'date of birth', 'gender', 'phone']
        counter = 0
        while counter < len(fields):
            v.speak("Please say " + fields[counter])
            data = v.listen()
            if "edit" in data:
                data = data.split()
                edit_field = ' '.join(data[data.index("edit")+1:])
                counter = self.set_counter(counter, edit_field, fields)
                v.speak ("Please say your " + fields[counter])
                data = v.listen()
                self.setValues(counter, data)
            elif "submit" in data:
                self.submit_form()
                break
            elif "exit" in data or "home" in data or "back" in data:
                self.go_to_home()
                break
            elif "clear" in data:
                self.clear_form()
                break
            else:
                self.setValues(counter, data)
                print("Setting " + fields[counter] + " to " + data)
                counter += 1
        v.speak("Your form has been filled. To submit, say submit or use any other command.")
        moreThread = v.ThreadWithReturnValue(target=self.more_commands)
        moreThread.start()
                                   
    def set_counter(self, counter, field, fields):
        for i in range(len(fields)):
            if field == fields[i]:
                counter = i
                break
        return counter
    
    def setValues(self, counter, data):
        if counter == 0:
            self.entry_firstname.delete(0, tk.END)
            self.entry_firstname.insert(0, data.capitalize().replace(" ", ""))
        elif counter == 1:
            self.entry_lastname.delete(0, tk.END)
            self.entry_lastname.insert(0, data.capitalize().replace(" ", ""))
        elif counter == 2:
            date = data.split()
            date = date[0][0:2] + "/" + date[0][2:] + "/" + date[1]
            self.dob_var.set(date)
        elif counter == 3:
            if data[0] == 'm':
                self.gender_var.set("Male")
            elif data[0] == 'f':
                self.gender_var.set("Female")
            else:
                self.gender_var.set("Other")
        elif counter == 4:
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, data.replace(" ", ""))
    
    def more_commands(self):
        fields = ['first name', 'last name', 'date of birth', 'gender', 'phone']
        counter = 0
        while True:
            v.speak("What do you want to do?")
            data = v.listen()
            if "edit" in data:
                data = data.split()
                edit_field = ' '.join(data[data.index("edit")+1:])
                counter = self.set_counter(counter, edit_field, fields)
                v.speak ("Please say your " + fields[counter])
                data = v.listen()
                self.setValues(counter, data)
            elif "submit" in data:
                self.submit_form()
                break
            elif "exit" in data or "home" in data or "back" in data:
                self.go_to_home()
                break
            elif "clear" in data:
                self.clear_form()
    
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Form Filling App")
        self.geometry("400x400")
        self.switch_frame(HomeScreen)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()
        self.current_frame = new_frame
        self.current_frame.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    app = App()
    app.mainloop()