clear;
clc;
close all;


root_dir = 'E:\wifi\Widar3.0\CSI\20181211';

out_dir="E:\wifi\WiSR\Widar3\CSI\matfile";
if ~isfolder(out_dir)
    mkdir(out_dir);
end
users = ["user3","user7","user8", "user9"];
room=3
ges_ids=["Push&Pull","Sweep","Clap","Slide","Draw-O(Horizontal)","Draw-Zigzag(Horizontal)"]
% traverseFolder(root_dir);

for m = 1:numel(users)
    user = users(m);
    disp(user);
    subfolder = fullfile(root_dir,user);
    
    
    files = dir(subfolder);
    for j = 1:numel(files)
        if files(j).name(1) == '.'
            % 忽略当前目录和上级目录的文件夹
            continue;
        end

        if files(j).isdir
            % 如果是文件夹，则递归遍历子文件夹
            continue;
        else
            % 如果是文件，则执行相应操作    'room_3_user_3_ges_Push&Pull_loc_1_ori_1_rx_1_csi.mat'
           file_path = fullfile(subfolder, files(j).name);
           info = strsplit(files(j).name, '-');
           ges=str2num(info{2});
           loc=info{3};
           ori=info{4};
           rep=info{5};
           rx=info{6}(2);
           %
           try
               disp(file_path);
               [csi_data, ~] = csi_get_all(file_path);
               out_filename = ['room_', room, '_user_', user{1}(5), '_ges_',ges_ids(ges) , '_loc_', loc, '_ori_', ori, '_rx_', rx, '_rep_', rep,'_csi.mat'];
               out_filename_str = join(out_filename, '');
               out_path=fullfile(out_dir,out_filename_str);
               save(out_path,'csi_data');
           catch exception
               warning('An error occurred while processing the data:\n%s', exception.message);
           end
        end
    end
       
end



