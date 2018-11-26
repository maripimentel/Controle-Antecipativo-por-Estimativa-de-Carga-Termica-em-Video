%%Codigo para Carregar Dados para as Simulacoes
%%Programa Principal
%%Autores:
%%  Alexandre Saran
%%  Mariana Pimentel

%Carregando banco de dados
database = '2018-11-23_09-51-38.db'; %Substituir pelo desejado

conn = sqlite(database);

sqlquery = 'SELECT * from informacaoSala';

result = fetch(conn, sqlquery);

%Lendo informacoes
time = result(:,1);
tempMeetingRoom = result(:,2);
tempLara = result(:,4);
tempExternal = result(:,5);
numPeople = result(:,7);
compressorSignal = result(:,8);

%Mudando a formatacao para ser possivel trabalhar no Matlab
tempExternal = cell2mat(tempExternal);
tempExternal = double(tempExternal);

tempLara = cell2mat(tempLara);
tempLara = double(tempLara);

numPeople = cell2mat(numPeople);
numPeople = double(numPeople);

tempMeetingRoom = cell2mat(tempMeetingRoom);
tempMeetingRoom = double(tempMeetingRoom);

dateTime = cell2mat(time);
dateTime = datetime(dateTime, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');

compressorSignal = cell2mat(compressorSignal);
compressorSignal = double(compressorSignal);

%Funcao de transferencia da planta identificada
K = 0.36783;
td = 5;
tau = 13.3140;

Gar = tf([K], [tau 1]);

%Ganhos do controlador PI projetado
Kp = 0.12;
Ki = 13 * Kp;

%Dados para a simulacao
%Ganhos
K = 0.01; %Ganho geral no modelo de carga termica
Kc = 2.5; %%Ganho da planta no modelo de carga termica
Ke = 1.4; %Influencia da carga termica externa
Kv = 3.3; %Influencia da carga termica das salas vizinhas
Knp = 0.1; %Influencia da carga termica de uma pessoa
Ktp = 36.5; %Temperatura média de uma pessoa
Kpwm = 20; %Ganho para normalizacao do PWM
Qp = (Ktp-23)*Knp; %Carga térmica estimada

%Constantes de tempo das perturbacoes
ae = 5.4867; %Atraso da influencia da temperatura externa
av = 6.9028; %Atraso da influencia da temperatura das salas vizinhas
anp = 16.5; %Atraso da influência do nº de pessoas

%Montando estruturas para a simulacao
rangeData = size(tempMeetingRoom);

time = 1:rangeData;

tempExternalStruct.time = time;
tempExternalStruct.signals.values = tempExternal;
tempExternalStruct.signals.dimensions = 1;
temperaturaExterna = tempExternalStruct;

tempLaraStruct.time = time;
tempLaraStruct.signals.values = tempLara;
tempLaraStruct.signals.dimensions = 1;
temperaturaSalaVizinha = tempLaraStruct;

compressorSignalStruct.time = time;
compressorSignalStruct.signals.values = compressorSignal;
compressorSignalStruct.signals.dimensions = 1;
sinalCompressor = compressorSignalStruct;

tempMeetingRoomStruct.time = time;
tempMeetingRoomStruct.signals.values = tempMeetingRoom;
tempMeetingRoomStruct.signals.dimensions = 1;
temperaturaSalaReuniao = tempMeetingRoomStruct;

numPeopleStruct.time = time;
numPeopleStruct.signals.values = numPeople;
numPeopleStruct.signals.dimensions = 1;
numeroPessoas = numPeopleStruct;
numeroPessoasReal = numeroPessoas;
numeroPessoasDetectadas = numeroPessoas;

%Simulacoes (Descomentar o desejado)
%sim('simulink_ma') %Malha Aberta
%sim('simulink_ld') %Liga-Desliga
%sim('simulink_pi') %PI
%sim('simulink_antecipativo') %Antecipativo

%Plots

%Referência
ref = zeros(rangeData,1);
for i = 1:rangeData
    ref(i) = 23;
end
ref = double(ref);

subplot(211);
plot(ref, 'r')
grid on;
hold on;
plot(ScopeData.time,ScopeData.signals.values, 'b');

%Descomentar o desejado
%title('Malha Aberta');
%title('Controlador Liga-Desliga');
%title('Controlador PI');
%title('Controlador Antecipativo');

%Media movel da temperatura da sala de reuniao
mean = movmean(ScopeData.signals.values, 50);

plot(mean, 'k')
plot(tempLara, 'm'); 
plot(tempExternal, 'g');
axis([0 rangeData 19 32]); %Ajustar para ficar visivel
xlabel('Tempo (min)');
ylabel('Temperatura (ºC)');
legend('Referência', 'Temperatura da Sala de Reunião Simulada', 'Média Móvel da Temperatura', 'Temperatura da Sala Vizinha', 'Temperatura Externa');

%No caso de Malha Aberta, comentar esta parte abaixo e a linha 117
subplot(212);
plot(numeroPessoas.time, numeroPessoas.signals.values);
grid on;
title('Contagem de Pessoas');
axis([0 rangeData 0 9]); %Ajustar para ficar visivel
xlabel('Tempo (min)');
ylabel('Nº de Pessoas');