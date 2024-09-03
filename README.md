# TouchDiver_UDP_Interface

TouchDiver UDP Interface Application
Overview:
This application allows users to interface with TouchDiver devices through a middleware using UDP communication. The application enables the user to control the device by sending and receiving data packets, starting streaming sessions, and requesting analog data such as temperature and force from the connected devices.

Features:
-UDP Communication Setup: Set the receiving and sending ports for UDP communication.
-Start Streaming: Automatically start streaming data from the middleware when the "Start" button is clicked.
-Send and Remove Effects: Send commands to apply or remove haptic effects on the TouchDiver device.
-Request Analog Data: Request analog data (temperature and force) from the connected device.

Getting Started
Prerequisites:
-Ensure that the TouchDiver middleware is running.
-Connect your TouchDiver device to the middleware.

SETUP

Configure UDP Ports:

-Receiving Port: Set the port where the application will receive data from the middleware.
-Sending Port: Set the port where the application will send data to the middleware.

Connect to Middleware:

-Open the middleware and ensure the TouchDiver device is connected.
-Set the UDP ports as described above.
-Start Streaming:

Click the "Start" button of UDP Interface Application

The middleware will begin streaming data automatically.
Sending and Removing Effects
To send or remove an effect, the application uses the following message structure:
ATTENTION: for remove effect set the "actPoint" to 0

Example message on matlab

% Define the data to send
header = uint8(1); % (1- Command message, 2- Request to remove effect or analogRawData)
handSide = uint8(1); % (1-Right hand)
actPoint = uint8(0); % Example: Middle actuation point (0 - remove effect, 1-Thumb, 2-Index, 3-Middle, 4-All)
tempValue = single(0.1); % Temperature intensity (0-1)
tempActive = true; % Enable temperature effect
forceValue = single(0.6); % Force intensity (0-1)
forceActive = true; % Enable force effect
textureType = int32(5); % Texture type (0-20)
textureVolume = int32(50); % Texture volume (0-99)
textureActive = true; % Enable texture effect

% Pack data into a byte array
data = [header, handSide, actPoint, ...
    typecast(tempValue, 'uint8'), ...
    uint8(tempActive), ...
    typecast(forceValue, 'uint8'), ...
    uint8(forceActive), ...
    typecast(textureType, 'uint8'), ...
    typecast(textureVolume, 'uint8'), ...
    uint8(textureActive)];
This message structure is sent via the selected sending port to apply or remove an effect on the TouchDiver device.

Requesting Analog Data
To request analog data (temperature and force) from the device, send the following message:

Example message matlab
data = [uint8(2)];
Upon sending this message, the application will immediately receive a response on the receiving port with the analog data for each finger.

Troubleshooting
Ensure the correct UDP ports are set for both receiving and sending data.
Confirm that the middleware and device are properly connected before starting the streaming session.
If no data is received after a request, check the middleware settings and the network connection.
