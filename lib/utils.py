def write_result_to_txt(args,results):
    import datetime
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    time_suffix = current_time.strftime("%Y-%m-%d")
    # file_name=args.output_dir+args.results_file
    file_name=args.out_dir / "logs" / f"result_{args.domain_type}_ori_{args.oris}_rx_{args.rxs}_exp_{args.exp_name}_{time_suffix}.txt"
    with open(file_name,"a") as file:
        file.write("time_string:"+time_string+"\n")
        file.write("output_dir:"+args.output_dir+"\n")
        file.write("source_domains:"+str(args.source_domains)+"\n")
        file.write("target_domains:"+str(args.target_domains)+"\n")
        file.write("n_train:"+str(results[0])+"\n")
        file.write("n_test:"+str(results[1])+"\n")
        file.write("best_acc:"+str(results[2])+"\n")

        file.write("\n")