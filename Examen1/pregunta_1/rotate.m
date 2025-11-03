function x = rotate(w,k)
if isempty(w) || k== 0 || k ==length(w)
    x = w;
else
    if k> length(w)
        k = k-length(w);
    end
    
    for(i=1:k)
        letter = w(1:1);
        w(1:1) =[];
        disp('k');
        w = strcat(w,letter);
   x = w;
    
    end
end
end