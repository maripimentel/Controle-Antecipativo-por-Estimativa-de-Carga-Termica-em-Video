%% CARREGAR OS DADOS
clc;
A = 6.112
m = 17.62;
Tn = 243.12;
C = 2.1674;
f= 1.0047;
T1 = '2016-09-15 20:13:04.0';
T2 = '2016-09-15 21:02:00.0';

%getmysql;
load('dados_sala');
s_time=1/60;

index1 = find(strcmp({t_externa.Time{:}}, T1)==1);
index2 = find(strcmp({t_externa.Time{:}}, T2)==1);
t_externa1.signals.values = t_externa.Value(index1:index2);
t_externa1.time=(1:length(t_externa1.signals.values));
t_externa1.signals.dimensions=1;

index1 = find(strcmp({u_externa.Time{:}}, T1)==1);
index2 = find(strcmp({u_externa.Time{:}}, T2)==1);
u_externa1.signals.values= u_externa.Value(index1:index2);
u_externa1.time = (1:length(u_externa1.signals.values));
u_externa1.signals.dimensions=1;

index1 = find(strcmp({t_lara.Time{:}}, T1)==1);
index2 = find(strcmp({t_lara.Time{:}}, T2)==1);
t_vizinhanca.signals.values = t_lara.Value(index1:index2);
t_vizinhanca.time = (1:length(t_vizinhanca.signals.values));
t_vizinhanca.signals.dimensions = 1;

index1 = find(strcmp({u_lara.Time{:}}, T1)==1);
index2 = find(strcmp({u_lara.Time{:}}, T2)==1);
u_vizinhanca.signals.values = u_lara.Value(index1:index2);
u_vizinhanca.time =  (1:length(u_vizinhanca.signals.values));
u_vizinhanca.signals.dimensions=1;

index1 = find(strcmp({bomba.Time{:}}, T1)==1);
index2 = find(strcmp({bomba.Time{:}}, T2)==1);
t_bomba.signals.values = bomba.Value(index1:index2);
t_bomba.time = (1:length(t_bomba.signals.values));
t_bomba.signals.dimensions = 1;

index1 = find(strcmp({condensador.Time{:}}, T1)==1);
index2 = find(strcmp({condensador.Time{:}}, T2)==1);
t_condensador.signals.values = condensador.Value(index1:index2);
t_condensador.time = (1:length(t_condensador.signals.values));
t_condensador.signals.dimensions = 1;

index1 = find(strcmp({t_interna.Time{:}}, T1)==1);
index2 = find(strcmp({t_interna.Time{:}}, T2)==1);
t_sala.signals.values = t_interna.Value(index1:index2);
t_sala.time = (1:length(t_sala.signals.values));
t_sala.signals.dimensions = 1;

index1 = find(strcmp({u_interna.Time{:}}, T1)==1);
index2 = find(strcmp({u_interna.Time{:}}, T2)==1);
u_sala.signals.values = u_interna.Value(index1:index2);
u_sala.time = (1:length(u_sala.signals.values));
u_sala.signals.dimensions = 1;

%% Ganhos do modelo
fator = 60;

K = 0.000222 * fator;  % SALA
Kr = 0.016835* fator;
Kv = 0.75959 * fator; % LAVSI1
Ke = 0.395   * fator;

Kc = 1       * fator;
Kv = 0.647   * fator;

%Constantes de tempo
%ao = 1;
ar = 1489   / fator;
al = 574.81 / fator;
av = 414.17 / fator;
ae = 329.2  / fator;
ac = 370.96 / fator; 

%Constantes entre malhas
Kut = 0;
Ktu = 0.03;

%% parametros estimados pelo idgrey
aue = 80.8223  / fator;
aum = 171.6923 / fator;
Kue = 0.1513;
Kum = -3.0134e-3;

au = 168.5014  / fator;
auv = 164.9597 / fator;
Ku = 2.1905;
Ks = 2.9186e-2; 
Kuv = 3.7757;
Kut = 0;
Ktu = 0.03;

% sim('sala3')
%% plotar resultados
% close all;
% plot(T_est.time*s_time,t_est.signals(1).values(:,1));
% hold on;
% plot(T_est.time*s_time,t_est.signals(1).values(:,2));
% xlabel 'Tempo (h)';ylabel 'Temperatura (^oC)'; legend ('Estimado','Real'); title 'Simula????o';
% 
% figure(2)
% plot(u_est.time*s_time,u_est.signals(1).values(:,1));
% hold on;
% plot(u_est.time*s_time,u_est.signals(1).values(:,2));
% xlabel 'Tempo (h)';ylabel 'Umidade Relativa (%)'; legend ('Estimado','Real'); title 'Simula????o';
% axis([0 50 -20 100])



