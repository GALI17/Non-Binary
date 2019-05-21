%表型聚类
clc
clear
close all
%%
K = 3; %cluster_number
iter = 100 % iteration
filepath='G:\KY2\p\';
num = 50
for ix = 1:num
    if ix < 10
        input_data = load([filepath 'p0' num2str(ix)]);
    else
        input_data = load([filepath 'p' num2str(ix)]);
    end
    %FCM________________________________________________________________________________
    options = [2;iter;1e-5;0]; 
    [center,U,obj_fcn] = fcm(input_data,K,options);
    maxU = max(U);
    index1 = find(U(1,:) == maxU);
    index2 = find(U(2,:) == maxU);
    index3 = find(U(3,:) == maxU);
    
    %k-means_____________________________________________________________________________
    CENTS = input_data( ceil(rand(K,1)*size(input_data,1)) ,:);             % Cluster Centers
    DAL   = zeros(size(input_data,1),K+2);                         % Distances and Labels

    for n = 1:iter
       for i = 1:size(input_data,1)
          for j = 1:K  
            DAL(i,j) = norm(input_data(i,:) - CENTS(j,:));      
          end
          [Distance CN] = min(DAL(i,1:K));                % 1:K are Distance from Cluster Centers 1:K 
          DAL(i,K+1) = CN;                                % K+1 is Cluster Label
          DAL(i,K+2) = Distance;                          % K+2 is Minimum Distance
       end
       for i = 1:K
          A = (DAL(:,K+1) == i);                          % Cluster K Points
          CENTS(i,:) = mean(input_data(A,:));                      % New Cluster Centers
          if sum(isnan(CENTS(:))) ~= 0                    % If CENTS(i,:) Is Nan Then Replace It With Random Point
             NC = find(isnan(CENTS(:,1)) == 1);           % Find Nan Centers
             for Ind = 1:size(NC,1)
             CENTS(NC(Ind),:) = input_data(randi(size(input_data,1)),:);
             end
          end
       end
    end

    idx1 =find(DAL(:,4) == 1);
    idx2 =find(DAL(:,4) == 2);
    idx3 =find(DAL(:,4) == 3); %其中值为4，是比聚类数多1，比如此时聚类数是3

    %输出_________________________________________________________________________________
    if ix < 10
        outpath = strcat(['G:\KY2\p_allCluster\hc0' num2str(ix)]);
    else
        outpath = strcat(['G:\KY2\p_allCluster\hc' num2str(ix)]);
    end
    cd(outpath);

        fid = fopen('idx1.txt','a');
        fprintf(fid,'%d\n',idx1);
        fid = fopen('idx2.txt','a');
        fprintf(fid,'%d\n',idx2);
        fid = fopen('idx3.txt','a');
        fprintf(fid,'%d\n',idx3);
        fid = fopen('index1.txt','a');
        fprintf(fid,'%d\n',index1);
        fid = fopen('index2.txt','a');
        fprintf(fid,'%d\n',index2);
        fid = fopen('index3.txt','a');
        fprintf(fid,'%d\n',index3);

        fclose(fid);
		
end