function num_str = alpha_filename(num)
if log10(num)<1
    num_str = strcat('00',num2str(num));
elseif log10(num)<2
    num_str = strcat('0',num2str(num));
else
    num_str = num2str(num);
end

