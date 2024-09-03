clear

localPort = 1234;
localIP = '127.0.0.1';  % Specify your local IP address if needed, or use '0.0.0.0' for any

% Create a UDP object with specified IP settings
u = udpport("datagram", "LocalHost", localIP, "LocalPort", 1235, "EnablePortSharing", true);

% Imposta la callback per ogni datagramma ricevuto
configureCallback(u, "datagram", 1, @udpCallback);



% Define the data to send
header = uint8(1); % Example:  ( 1- Command message, 2- request of remove Effect[we should implement analogRawData request])
handSide = uint8(1); % (1-Right, 2-Left)
actPoint = uint8(0); % Example: Middle actuation point (0 - remove effect, 1-Thumb,2-Index,3-Middle,4-All)
tempValue = single(0.1); %(0-1)
tempActive = true;
forceValue = single(0.6); %(0-1)
forceActive = true;
textureType = int32(5); % Example texture type (0-20)
textureVolume = int32(50); %(0-99)
textureActive = true;

% Pack data into a byte array
data = [header, handSide, actPoint, ...
    typecast(tempValue, 'uint8'), ...
    uint8(tempActive), ...
    typecast(forceValue, 'uint8'), ...
    uint8(forceActive), ...
    typecast(textureType, 'uint8'), ...
    typecast(textureVolume, 'uint8'), ...
    uint8(textureActive)];

data2 = [uint8(2)];

% Send the data
% write(u, data, 'uint8',localIP_,localPort);
write(u, data2, 'uint8',localIP,localPort);


function udpCallback(src, ~)
% Leggi il datagramma ricevuto
   if src.NumDatagramsAvailable > 0
        % Leggi il datagramma come array di float a 32 bit
        data = read(src,1);
        disp(data)
        floats = typecast(uint8(data.Data), 'single');
        % Assicurati che i dati siano convertiti in un array di numeri prima di stamparli
        % Converti i dati in un vettore se necessario

        fprintf("Received data: [Thumb Temp: %.2f, Thumb Force: %.2f, Index Temp: %.2f, Index Force: %.2f, Middle Temp: %.2f, Middle Force: %.2f]\n", floats);
   end
end

