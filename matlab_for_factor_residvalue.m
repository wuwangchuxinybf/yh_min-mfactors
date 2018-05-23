format compact;
% 数据文件地址
% add_data = 'G:/short_period_mf/alpha_min_stand_matlab/';
add_resid = 'G:/short_period_mf/resid_value_min_matlab/';
% 最终结果初始化
data_str = struct;
% 股票代码
stockList = readtable('stockList.csv');
data_str.stockcode = stockList.code;
% 交易日序列
day_dateList = readtable('day_dateList.csv');
data_str.trade_day = day_dateList.date';
% 交易分钟序列
min_dateList = readtable('min_dateList.csv');
data_str.trade_min = min_dateList.datetime(7:54480)'; %从2017-01-03 09:37:00开始
% 行业数据
% industry = readtable(fullfile(add_data,'industry.csv'));
industry = readtable('industry.csv');
industry_str = table2struct(industry,'ToScalar',true);
indus_fln = fieldnames(industry_str);
for fln=1:length(indus_fln)
    data_str.(indus_fln{fln}) = repmat(industry_str.(indus_fln{fln}),1,54474);
end
% 风格因子数据
factors_file = {'BP.csv','Beta.csv','EarnYield.csv','Growth.csv','Leverage.csv'...
                ,'Liquidity.csv','Momentum.csv','ResVol.csv','Size.csv'}';
for fn=1:length(factors_file)
    mid = kron(csvread(factors_file{fn}),ones(1,240));
    data_str.(factors_file{fn}(1:end-4)) =  mid(:,7:end);
end
clear day_dateList factors_file fln indus_fln industry ...
        industry_str mid stockList min_dateList fn
% alpha因子数据
% for n=1:191
%     factors_reuturn = readtable(strcat('alpha_',alpha_filename(n),'.csv'),'ReadVariableNames',true);
% %     factors_reuturn = factors_reuturn(1:end,2:end);
%     data_str.(strcat('alpha_',alpha_filename(n))) = table2array(factors_reuturn(:,2:end));
% end
fldname = fieldnames(data_str);
fldname = fldname(4:end,1);
for n=184:191
    n
    X_matrix = zeros(299,38);
    result = zeros(299,54474);
    Y = csvread(strcat('standard_alpha_',alpha_filename(n),'.csv'),1,1,[1,1,299,54474]);
    for min_len=1:length(data_str.trade_min)
        for fn=1:length(fldname)
            X_matrix(:,fn) = data_str.(fldname{fn})(:,min_len);
        end
        [~,~,r] = regress(Y(:,min_len),X_matrix);
        result(:,min_len) = r;
    end
    save(strcat(add_resid,'alpha_',alpha_filename(n),'_resid.mat'),'result');
    clear result Y X_matrix r n min_len
end