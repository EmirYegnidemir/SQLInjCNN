import Tkinter as tk
import subprocess
import socket
import subprocess  # Import subprocess for executing the machine learning scriptnt import
from scapy.all import Ether, sendp, IP, ICMP, conf, Raw

# Define the available script choices
script_choices = ["sql_injection.py", "spoofing.py", "ddos.py"]
inspector_ip = ''  
inspector_port = 54321  # Use the same port number as in listener.py (Host 2)

def execute_ml_script(script_name):
    try:
        # Execute the machine learning script and capture its output
        process = subprocess.Popen(["python2.7", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        return stdout.strip()
    except Exception as e:
        print("Error executing machine learning script:", str(e))
        return "Error"

def run_script():
    selected_script = script_var.get()
    result = execute_ml_script(selected_script)
    result_text.delete(1.0, tk.END)  # Clear previous result
    result_text.insert(tk.END, result)

    inspector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inspector_socket.bind((inspector_ip, inspector_port))
    inspector_socket.listen(5)  # Specify the maximum number of queued connections

    print("Inspector is ready to receive and inspect messages...")

    while True:
        connection, address = inspector_socket.accept()
        message = connection.recv(1024).decode()
        print("Message received from Host 1:", message)

        # Execute the machine learning script on the received message
        ml_result = execute_ml_script(message)
        print(ml_result)
        print("Machine Learning Result:", ml_result)
        connection.close()
    
        # Send the "block" or "unblock" message based on your requirement
        if ml_result == "ALERT :::: This can be SQL injection":     
            custom_packet = Ether(src="00:00:00:00:00:03", dst="00:00:00:00:00:05") / IP(dst="10.0.0.1") / ICMP() / "block"
            sendp(custom_packet, iface="h3-eth0")  
            print("Packet sent to controller with output action OFPP_CONTROLLER")

        else:
            #custom_packet = Ether(src="00:00:00:00:00:03", dst="00:00:00:00:00:01") / IP(dst="10.0.0.1") / ICMP() / 'unblock'
            print("No packet sent to controller")   

        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, result)

# Create the main application window
root = tk.Tk()
root.title("IBN Manager")

# Create a label for script selection
script_label = tk.Label(root, text="Select the attack type to defend against:")
script_label.pack()

# Create a variable to hold the selected script
script_var = tk.StringVar(root)
script_var.set(script_choices[0])

# Create a menu with script choices
script_menu = tk.OptionMenu(root, script_var, *script_choices)
script_menu.pack()

# Create a button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack()

# Create a text widget to display the result
result_text = tk.Text(root, height=10, width=40)
result_text.pack()

root.mainloop()