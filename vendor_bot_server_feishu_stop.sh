programs=`ps -ef|grep vendor_bot_server_feishu.py|grep -v "grep"`
echo $programs
id=`echo $programs|awk '{print $2}'`
echo "---------- the target id:$id ------------"
if [ "$id" == "" ];then
  echo "no target find!"
  exit 0
fi

kill -9 $id

