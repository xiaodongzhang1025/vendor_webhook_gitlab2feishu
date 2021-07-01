script_path=`cd $(dirname $0); pwd`
cd $script_path
nohup python -u ./vendor_bot_server_feishu.py 2>&1 |tee ./vendor_bot_server_feishu.log &
