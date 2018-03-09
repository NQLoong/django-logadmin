#!/bin/bash

fig_path='./secret_fig.txt'
a=$(cat $fig_path)
arr=${a//\n/ }



auto_ssh_copy_id() {
    expect -c "set timeout -1;
        spawn ssh-copy-id $1;
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            *assword:* {send -- $2\r;exp_continue;}
            eof        {exit 0;}
        }";
}

ssh_copy_id_to_all() {
    for i in $arr
    do  
        SERVER=$(echo $i|cut -d '|' -f 1)
        PASSWORD=$(echo $i|cut -d '|' -f 2)
        echo $SERVER
        echo '=============='
        auto_ssh_copy_id $SERVER $PASSWORD
    done
}

ssh_copy_id_to_all
