<?php
defined('BASEPATH') OR exit('No direct script access allowed');


class LasDump
{
    protected $CI;
    protected $params;

    public function __construct($params)
    {
        $this->CI =& get_instance();
        $this->params = $params['params'];
        $this->CI->load->model('Client_model','client');
        $this->CI->load->model('Task_model','task');
        $this->CI->load->helper('string');
    }
    public function dump(){
        $param = $this->params;
        if(!empty($_FILES['LAS'])){
            $newpath = "files/private/".$param->key."/".date('Ymd',time())."/";
            if(!file_exists($newpath)){
                mkdir($newpath, 0700,true);
            }
            $file_name = random_string('md5');
            $config['upload_path'] = $newpath;
            $config['allowed_types'] = '*';
            $config['max_size'] = 0;
            $config['file_name'] = $file_name.'.gz';
            $this->CI->load->library('upload', $config);
            if($this->CI->upload->do_upload('LAS')){
                $data = $this->CI->upload->data();
                $full_path = strstr($data['full_path'],'files/private');
                $param->result->data = $full_path;
            }
        }
        $this->CI->task->updateTaskResult($param->id,$param->key,json_encode($param->result),2);
    }
}