import os



file_path="train_output/logs/result_user_ori_1-2-3_rx_1_exp_ours_ca_cross_user_2024-02-27.txt"

basename=os.path.basename(file_path)
crosstype=basename.split("_")[1]

with open(file_path,"r") as f:
    res=[]

    lines=f.readlines()
    my_dict={}
    constant_pre=""
    for line in lines:
        if line.strip() == '':
            res.append(my_dict)
            my_dict = {}
            continue
        key,value=line.split(':',1)
        if key=="target_domains":
            splits=value.split("_")
            if crosstype=="loc":
                target_domain=crosstype+splits[5]
                constant="user"+splits[3]
            if crosstype=="user":
                target_domain = crosstype + splits[3]
                constant = "loc" + splits[5]
        if key=="best_acc":
            best_acc=float(value)
            if constant in my_dict.keys():
                my_dict[constant][target_domain] = best_acc
            else:
                new_dict = {}
                new_dict[target_domain] = best_acc
                my_dict[constant]=new_dict


data=dict()
for result in res:
    item=result.items()
    for key ,value in item:
        if key in data.keys():
            data[key].append(value)
        else:
            li=[]
            li.append(value)
            data[key]=li


locations = sorted(set([key for sublist in data.values() for item in sublist for key in item.keys()]))

# 打印表头
header = "User\t" + "\t".join(locations)
print(header)

# 打印每个用户的数据行
for user, values in sorted(data.items()):
    row = user + "\t"
    for location in locations:
        for item in values:
            if location in item:
                row += str(item[location])
                break
        else:
            row += "N/A"
        row += "\t"
    print(row)