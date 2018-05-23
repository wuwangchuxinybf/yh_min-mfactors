test_60 = load(strcat(add_factor_return,'factor_return_',num2str(60),'.mat'));
test_120 = load(strcat(add_factor_return,'factor_return_',num2str(120),'.mat'));
test_180 = load(strcat(add_factor_return,'factor_return_',num2str(180),'.mat'));
test_240 = load(strcat(add_factor_return,'factor_return_',num2str(240),'.mat'));

xlswrite('G:\short_period_mf\factor_return_min\factor_return_60',test_60.result);
xlswrite('G:\short_period_mf\factor_return_min\factor_return_240',test_240.result);
xlswrite('G:\short_period_mf\factor_return_min\factor_return_120',test_120.result);
xlswrite('G:\short_period_mf\factor_return_min\factor_return_180',test_180.result);
