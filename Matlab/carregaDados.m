database = '2018-10-20_16:44:16.db';
conn = sqlite(database);

sqlquery = 'SELECT * from informacaoSala';

result = fetch(conn, sqlquery);

dateTime = result(:,1);
tempMeetingRoom = result(:,2);
humMeetingRoom = result(:,3);
tempLara = result(:,4);
tempExternal = result(:,5);
compressorSignal = result(:,8);

tempMeetingRoom = cell2mat(tempMeetingRoom);
dateTime = cell2mat(dateTime);
compressorSignal = cell2mat(compressorSignal);
compressorSignal = double(compressorSignal);

compressorSignal(compressorSignal==0) = 30;
compressorSignal(compressorSignal==1) = 14;

temp = [dateTime, tempMeetingRoom];

dateTime = datetime(dateTime, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');

% plot(dateTime, tempMeetingRoom);
% grid on
% hold on
% plot(dateTime, compressorSignal)

K = 0.36783;
tau = 13.314;
td = 0.065;

Gar = tf([K], [tau 1]);

Kp = 0.12;
Ki = 13 * Kp;