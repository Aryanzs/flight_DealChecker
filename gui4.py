from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv
import pandas as pd
import subprocess

conversion_rate = 0.0095

def convert_rupees_to_pounds():
    try:
        rupees_amount = float(rupees_entry.get())
        pounds_amount = rupees_amount * conversion_rate
        result_var.set(f"{rupees_amount} Rupees is approximately {pounds_amount:.2f} Pounds.")
        
        # Automatically populate the minimum price entry with the converted value
        min_price_var.set(f"{pounds_amount:.2f}")

    except ValueError:
        result_var.set("Please enter a valid numeric value for Rupees.")




root = Tk()
root.configure(bg="#AED6F1")

def Submit1():
    username = username_var.get()
    email = email_var.get()

    confirmation_message = f"Username: {username}\n Email: {email}\nAre Provided Details Correct"
    messagebox.askokcancel(title="Confirm details", message=confirmation_message)

    print(f"Username: {username}")
    print(f"Email: {email}")

    csv_data = [
        ["Username", "Email"],
        [username, email]
    ]
    csv_file_path = "user_data.csv"
    with open(csv_file_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)

    print(f"Data written to {csv_file_path}")
    # Hide the current window
    root.withdraw()

    # Open a new window for the next set of inputs
    destination_window.deiconify()

def submit_form():

    departure_city = departure_var.get()
    destination_city = destination_var.get()
    min_price = min_price_var.get()
    username = username_var.get()
    email = email_var.get()

    confirmation_message = f"Destination: {destination_city}\nPrize: {min_price}\nSource: {departure_city}\nThanks for your submission. When the deal is low, we will notify you."
    messagebox.askokcancel(title="Confirm details", message=confirmation_message)

    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Departure City: {departure_city}")
    print(f"Destination City: {destination_city}")
    print(f"Minimum Price: {min_price}")

    csv_data = [
        ["Username", "Email", "Departure City", "Destination City", "Minimum Price"],
        [username, email, departure_city, destination_city, min_price]
    ]

    csv_file_path = "user_data.csv"
    with open(csv_file_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)

    print(f"Data written to {csv_file_path}")
    try:
        subprocess.run(["python", "main2.py"])
    except Exception as e:
        print(f"Error executing main2.py: {e}")


    

    

def display_flight_info():
    # Read the flight data CSV file
    flight_data = pd.read_csv('flight_data_sorted.csv')

    # Filter flight data based on user input
    departure_city = departure_var.get()
    destination_city = destination_var.get()

    filtered_flight_data = flight_data[(flight_data['cityCodeFrom'] == departure_city) & (flight_data['cityCodeTo'] == destination_city)]

    if filtered_flight_data.empty:
        messagebox.showinfo("No Flights", "No flights available for the selected route.")
        return

    # Create a new window for displaying flight information
    flight_info_window = Toplevel(root)
    flight_info_window.title("Flight Information")
    flight_info_window.config(bg="#000080")

    # Create a Treeview widget to display flight information in a table
    tree = ttk.Treeview(flight_info_window, columns=list(filtered_flight_data.columns), show="headings")

    # Set column headings
    for col in filtered_flight_data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # Insert data into the Treeview
    for _, row in filtered_flight_data.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(pady=20, padx=20)
    

def animate_logo(x, y, step=5):
    canvas.move(logo, step, 0)
    if canvas.coords(logo)[0] > root.winfo_width():
        canvas.coords(logo, -400, 100)
    root.after(20, animate_logo, x + step, y)

canvas = Canvas(height=200, width=200, bg="#AED6F1", highlightthickness=0)
logo_img = PhotoImage(file="aeroplane.png")
logo_img = logo_img.subsample(3, 3)
logo = canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, columnspan=2)
# Create the main window
root.title("Flight Information Form")

# Create StringVar and IntVar to store entry values
username_var = StringVar()
email_var = StringVar()
departure_var = StringVar()
destination_var = StringVar()
min_price_var = IntVar()

Label(root, text="Username:", bg="#AED6F1").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=username_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Email ID:", bg="#AED6F1").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=email_var).grid(row=2, column=1, padx=10, pady=5)

# Create a submit button for the first window
Button(root, text="Submit",  bg="#000080", fg="white", command=Submit1).grid(row=3, column=0, columnspan=2, pady=10)


# Create a new window for the second set of inputs
destination_window = Toplevel(root)
destination_window.title("Flight Details")
destination_window.config(bg="#AED6F1")

# Hide the destination window initially
destination_window.withdraw()



# Create a button to display flight information


# Create labels and entry widgets for the second window
Label(destination_window, text="Departure City Code:", bg="#AED6F1").grid(row=1, column=0, padx=10, pady=5)
Entry(destination_window, textvariable=departure_var).grid(row=1, column=1, padx=10, pady=5)

Label(destination_window, text="Destination City Code:", bg="#AED6F1").grid(row=2, column=0, padx=10, pady=5)
Entry(destination_window, textvariable=destination_var).grid(row=2, column=1, padx=10, pady=5)

Label(destination_window, text="Minimum Price in Pounds:", bg="#AED6F1").grid(row=3, column=0, padx=10, pady=5)
Entry(destination_window, textvariable=min_price_var).grid(row=3, column=1, padx=10, pady=5)

# Create a conversion frame for the second window
conversion_frame = Frame(destination_window, bg="#AED6F1")
conversion_frame.grid(row=1, column=2, padx=20, rowspan=4)

rupees_label = Label(conversion_frame, text="Enter Rupees Amount:", bg="#AED6F1")
rupees_label.grid(row=0, column=0, padx=10, pady=10)

rupees_entry = Entry(conversion_frame, width=20)
rupees_entry.grid(row=0, column=1, padx=10, pady=10)

result_var = StringVar()
result_label = Label(conversion_frame, textvariable=result_var, font=("Arial", 12, "bold"), bg="#AED6F1")
result_label.grid(row=1, column=0, columnspan=2, pady=10)

convert_button = Button(conversion_frame, text="Convert to Pounds", bg="#000080", fg="white", command=convert_rupees_to_pounds)
convert_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a submit button for the second window
Button(destination_window, text="Submit", bg="#003366", fg="white", command=submit_form).grid(row=4, column=0, columnspan=2, pady=10)
Button(destination_window, text="Display Flight Info", bg="#003366", fg="white", command=display_flight_info).grid(row=5, column=0, columnspan=2, pady=10)

# Start the main loop
animate_logo(100, 100)
root.mainloop()
