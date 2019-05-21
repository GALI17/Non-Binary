%表型集成聚类
clc
clear
close all
%%
filepath='G:\KY2\p_matrix\';
for k = 1:50
    if k < 10
        input_data = load([filepath 'pm0' num2str(k)]);
    else
         input_data = load([filepath 'pm' num2str(k)]);
    end
	c=linkage(input_data,'single');
	hc=cluster(c,3);
	hc1=find(hc==1);
	hc2=find(hc==2);
	hc3=find(hc==3);
    
    if k < 10
        outpath = strcat(['G:\KY2\phc\hc0' num2str(k)]);
    else
        outpath = strcat(['G:\KY2\phc\hc' num2str(k)]);
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