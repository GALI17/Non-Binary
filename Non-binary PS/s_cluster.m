%位点聚类
clc
clear
close all
%%
filepath='G:\KY2\s\';
num = 50
for ix = 1:num
    if ix < 10
        input_data = load([filepath 's0' num2str(ix)]);
    else
        input_data = load([filepath 's' num2str(ix)]);
    end
	d = pdist(input_data,'hamming');
	c=linkage(d,'average');
	hc=cluster(c,3);
	hc1=find(hc==1);
	hc2=find(hc==2);
	hc3=find(hc==3);

    %输出_________________________________________________________________________________
    if ix < 10
        outpath = strcat(['G:\KY2\s_allCluster\hc0' num2str(ix)]);
    else
        outpath = strcat(['G:\KY2\s_allCluster\hc' num2str(ix)]);
    end
    cd(outpath);

	fid = fopen('hc1.txt','a');
	fprintf(fid,'%d\n',hc1);
	fid = fopen('hc2.txt','a');
	fprintf(fid,'%d\n',hc2);
    fid = fopen('hc3.txt','a');
	fprintf(fid,'%d\n',hc3);
		
    fclose(fid);	
end