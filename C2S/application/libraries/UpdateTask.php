<?php
defined('BASEPATH') OR exit('No direct script access allowed');


class UpdateTask
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

    public function ut(){
        //更新任务
        $param = $this->params;
        $current_task = $this->CI->task->getTaskInfoById($param->id);
        if($current_task['type'] == "screenshot"){
            //处理文件上传
            if(!empty($_FILES['file'])){
                $new_file_path = "up/".$param->key . "/" . date('Ymd',time()) . "/";
                if(!file_exists($new_file_path)){
                    //检查是否有该文件夹，如果没有就创建，并给予最高权限
                    mkdir($new_file_path, 0700,true);
                }
                $config['upload_path'] = $new_file_path;
                $config['allowed_types'] = '*';
                $config['max_size'] = 0;
                $config['file_name'] = time() . ".png";
                $this->CI->load->library('upload', $config);
                if($this->CI->upload->do_upload('file')){
                    $data = $this->CI->upload->data();
                    $full_path = $new_file_path.$config['file_name'];
                    $file_size = $data['file_size'];
                    $param->result = $full_path."|".$file_size;
                }else{
                    $param->result = "/up/error.png"."|0";
                }
            }else{
                $param->result = "/up/warning.png"."|0";
            }
        }
        //更新任务日志
        $this->CI->task->updateTaskResult($param->id,$param->key,$param->result,2);
    }
}