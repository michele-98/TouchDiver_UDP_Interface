% Define the parameters
remoteIP = '192.168.125.50'; % Replace with the remote address
localPort = 61557;         % The local port to listen on

% Create the UDP object
udpReceiver = udpport('LocalPort', localPort);

% Optional: Display UDP object properties
disp(udpReceiver);
% Read data from the remote UDP server
disp('Waiting to receive data...');
while true
    % Receive UDP data and read it as a string
    data = readline(udpReceiver); % Readline automatically reads the string data
    if ~isempty(data)
        disp('Received UDP data:');
        disp(data);  % Display the received string
    end
end
% Close and clean up
clear udpReceiver;
