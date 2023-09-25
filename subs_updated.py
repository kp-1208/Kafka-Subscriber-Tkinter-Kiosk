'''
Author: Kshitij Parashar
Date: September 21, 2023
'''

import tkinter as tk
from tkinter import scrolledtext
from confluent_kafka import Consumer, KafkaError

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': '192.168.12.1:9092',  # Replace with your Kafka broker address
    'group.id': 'face_recognition_consumer_group6',  # Replace with your group ID
    'auto.offset.reset': 'latest'
}

# Create persons list for displaying
msgs = []
msgs_size = 5 # Number of messages to be printed at once

# Kafka topic for messages
kafka_topic = 'face_recognition_feedback_messages_topic_0'

# Create Kafka consumer
consumer = Consumer(kafka_conf)
consumer.subscribe([kafka_topic])

# Create the Tkinter window
root = tk.Tk()
root.title("Kafka Message Viewer")

# Maximize the window
root.attributes('-fullscreen', True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()
root.focus_force()

# Function to exit the application (you can customize this)
def exit_kiosk():
    root.quit()

# Create a button to exit the kiosk
exit_button = tk.Button(root, text="Exit Kiosk", command=exit_kiosk, bg='black', fg='red')
exit_button.pack()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create the label
text_widget = scrolledtext.ScrolledText(root, wrap='word', font=("Verdana", 18), bg='black', fg='red')
text_widget.pack(expand=True, fill='both')

# Center the ScrolledText widget both vertically and horizontally
text_widget.place(relx=0.5, rely=0.5, anchor='center')

# Calculate the x and y position to center the label
x = (screen_width - text_widget.winfo_reqwidth()) / 2
y = (screen_height - text_widget.winfo_reqheight()) / 2

# Set the window size and position
root.geometry(f"{int(screen_width/2)}x{int(screen_height/2)}+{int(x)}+{int(y)}")

# Function to update the Tkinter text widget with Kafka messages
def update_messages():
    global msgs, msgs_size
    none_count = 0
    message = ""
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            none_count += 1
            if none_count == 10:
                msgs.clear()
                none_count = 0
                continue
        else:
            message = msg.value().decode('utf-8')
            if message not in msgs:
                if len(msgs) == msgs_size:
                    del msgs[0]
                msgs.append(message)
                
        print(msgs)                            
        text_widget.delete('1.0', tk.END)  # Clear the text widget
        for m in msgs:
            text_widget.insert(tk.END, f"Recognized: {m}\n")

            
# Start a separate thread to update messages
import threading
update_thread = threading.Thread(target=update_messages)
update_thread.daemon = True
update_thread.start()

# Start the Tkinter main loop
root.mainloop()
