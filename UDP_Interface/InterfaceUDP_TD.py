import tkinter as tk
from tkinter import messagebox
import socket
import threading
import struct
from weartsdk import *
from weartsdk.WeArtCommon import HandSide, ActuationPoint, TextureType
import time
import logging

class UDPReceiverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("UDP Receiver")

        # Campo per la porta di ricezione
        self.label = tk.Label(master, text="Enter UDP Receive Port:")
        self.label.pack()

        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, "1234")  # Default receive port value
        self.port_entry.pack()

        # Campo per la porta di invio
        self.send_port_label = tk.Label(master, text="Enter UDP Send Port:")
        self.send_port_label.pack()

        self.send_port_entry = tk.Entry(master)
        self.send_port_entry.insert(0, "1235")  # Default send port value
        self.send_port_entry.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_receiving)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_receiving, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.message_list = tk.Listbox(master, width=100, height=30)
        self.message_list.pack()

        self.sock = None
        self.receiver_thread = None
        self.running = False
        self.client = None
        self.hapticObject = None

        # Ensure the application exits cleanly
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        message_display = f"To read the Analog Data Raw enable from the middleware 'ANALOG SENSOR'."
        self.master.after(0, self.update_message_list, message_display)
        message_display = f" [Show UI test pannel -> type 'debug' -> change Respone Pack]"
        self.master.after(0, self.update_message_list, message_display)

    def start_receiving(self):
        receive_port_str = self.port_entry.get()
        send_port_str = self.send_port_entry.get()

        if not receive_port_str.isdigit() or not send_port_str.isdigit():
            messagebox.showerror("Invalid Input", "Please enter valid port numbers.")
            return

        self.receive_port = int(receive_port_str)
        self.send_port = int(send_port_str)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind(('127.0.0.1', self.receive_port))
        except Exception as e:
            messagebox.showerror("Socket Error", f"Failed to bind socket: {e}")
            return

        self.client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT, log_level=logging.INFO)
        self.client.Run()
        self.client.Start()

        self.hapticObject = WeArtHapticObject(self.client)
        self.hapticObject.handSideFlag = HandSide.Right.value

        self.analogSensorData_Thumb = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Thumb)
        self.client.AddMessageListener(self.analogSensorData_Thumb)
        self.analogSensorData_Index = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Index)
        self.client.AddMessageListener(self.analogSensorData_Index)
        self.analogSensorData_Middle = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Middle)
        self.client.AddMessageListener(self.analogSensorData_Middle)

        self.touchEffect = TouchEffect(WeArtTemperature(), WeArtForce(), WeArtTexture())

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.DISABLED)
        self.send_port_entry.config(state=tk.DISABLED)

        self.running = True
        self.receiver_thread = threading.Thread(target=self.receive_messages)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

        message_display = f"WeArtClient: Connection to server: ('127.0.0.1', 13031) established"
        self.master.after(0, self.update_message_list, message_display)

    def receive_messages(self):


        while self.running:
            if self.sock is None:
                break  # Esci dal ciclo se il socket è stato chiuso o non è valido

            data, addr = self.sock.recvfrom (1024)
            if not data:
                continue
            header = data [ 0 ]

            if header == 1:
                print ("Data processed for header 1")
                message_display = f"TouchDiver Command Message"
                self.master.after (0, self.update_message_list, message_display)
                self.handle_haptic_message (data[1:])
            elif header == 2:
                print(len(data))
                print ("Data processed for header 2")
                message_display = f"Data request message"
                self.master.after (0, self.update_message_list, message_display)
                self.handle_sensor_message()

            else:
                message_display = f"Header not recognized"
                print (len (data))
                self.master.after (0, self.update_message_list, message_display)


    def handle_haptic_message(self, data):
        self.hapticObject.RemoveEffect (self.touchEffect)
        #self.hapticObject.RemoveEffect (self.touchEffect)
        try :
            unpacked_data = struct.unpack ('=BBfBfBiiB', data)
            hand_side, act_point, temp_value, temp_active, force_value, force_active, texture_type, texture_volume, texture_active = unpacked_data
        except Exception as e:
            message_display = f"Error on struct.unpack"
            self.master.after (0, self.update_message_list, message_display)

        temperature = WeArtTemperature ()
        temperature.value = round (temp_value, 3)
        temperature.active = bool (temp_active)

        force = WeArtForce ()
        force.value = round (force_value, 3)
        force.active = bool (force_active)

        texture = WeArtTexture ()
        texture.textureType = TextureType (texture_type)
        texture.textureVelocity = 0.5  # maximum value
        texture.textureVolume = texture_volume
        texture.active = bool (texture_active)

        self.touchEffect.Set (temperature, force, texture)

        # Adjust actuation point based on act_point value
        if act_point == 0:
            # If act_point is 0, remove the effect
            self.hapticObject.RemoveEffect (self.touchEffect)
        elif act_point == 1:
            # Set actuation point to Thumb
            self.hapticObject.actuationPointFlag = ActuationPoint.Thumb
            self.hapticObject.AddEffect (self.touchEffect)
        elif act_point == 2:
            # Set actuation point to Index
            self.hapticObject.actuationPointFlag = ActuationPoint.Index
            self.hapticObject.AddEffect (self.touchEffect)
        elif act_point == 3:
            # Set actuation point to Middle
            self.hapticObject.actuationPointFlag = ActuationPoint.Middle
            self.hapticObject.AddEffect (self.touchEffect)
        elif act_point == 4:
            # Set actuation point to Thumb, Index, and Middle
            self.hapticObject.actuationPointFlag = ActuationPoint.Thumb | ActuationPoint.Index | ActuationPoint.Middle
            self.hapticObject.AddEffect (self.touchEffect)


    def handle_sensor_message(self):
        sample_Thumb = self.analogSensorData_Thumb.GetLastSample ()
        print(sample_Thumb)
        sample_Index = self.analogSensorData_Index.GetLastSample ()
        print(sample_Index)
        sample_Middle = self.analogSensorData_Middle.GetLastSample ()
        print(sample_Middle)

        self.send_data(sample_Thumb, sample_Index, sample_Middle)

    def stop_receiving(self):
        self.running = False

        if self.sock:
            self.sock.close ()
        if self.client:
            self.client.Stop ()
            self.client.Close ()

        self.start_button.config (state=tk.NORMAL)
        self.stop_button.config (state=tk.DISABLED)
        self.port_entry.config (state=tk.NORMAL)
        self.send_port_entry.config (state=tk.NORMAL)

    def on_closing(self):
        # This method will be called when the window is closed
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.stop_receiving()
            self.master.destroy()

    def update_message_list(self, message):
        # Aggiorna la Listbox nel thread della GUI
        self.message_list.insert(tk.END, message)
        self.message_list.yview(tk.END)

    def send_data(self, sample_Thumb, sample_Index, sample_Middle):
        # Estrai i dati
        #timestamp = sample_Thumb.timestamp
        thumb_temp = sample_Thumb.data.ntcTemperatureConverted
        thumb_force = sample_Thumb.data.forceSensingConverted
        index_temp = sample_Index.data.ntcTemperatureConverted
        index_force = sample_Index.data.forceSensingConverted
        middle_temp = sample_Middle.data.ntcTemperatureConverted
        middle_force = sample_Middle.data.forceSensingConverted
        if not all(isinstance(v, float) for v in [thumb_temp, thumb_force, index_temp, index_force, middle_temp, middle_force]):
            print("Error: One or more values are not floats")
            return

        # Crea il pacchetto con un intero e 6 float
        packet_format = '=6f'  # 1 unsigned int, 6 float
        packet = struct.pack(packet_format,  thumb_temp, thumb_force, index_temp, index_force, middle_temp, middle_force)

        # Invia il pacchetto a un indirizzo IP e porta specifici

        self.sock.sendto(packet, ('127.0.0.1', self.send_port))
        print(len(packet))
        print(f"Sent packet: {packet}")

def main():
    root = tk.Tk()
    app = UDPReceiverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()