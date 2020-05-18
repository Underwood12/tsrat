<?php
defined('BASEPATH') OR exit('No direct script access allowed');


class UploadFile
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

    public function up(){
        $param = $this->params;
        if(!empty($_FILES['file'])){
            $newpath = "files/private/".$param->key."/".date('Ymd',time())."/";
            if(!file_exists($newpath)){
                mkdir($newpath, 0700,true);
            }
            $file_name = random_string('md5');
            $config['upload_path'] = $newpath;
            $config['allowed_types'] = '*';
            $config['max_size'] = 0;
            $config['file_name'] = $file_name.'.zip';
            $this->CI->load->library('upload', $config);
            if($this->CI->upload->do_upload('file')){
                $data = $this->CI->upload->data();
                $full_path = strstr($data['full_path'],'files/private');
                $result = json_encode(array(
                    "full_path" => $full_path,
                    "save_name" => $param->save_name,
                    "file_size" => $data['file_size'],
                    "status" => TRUE
                ));
            }else{
                $result = json_encode(array(
                    "full_path" => "",
                    "save_name" => "",
                    "file_size" => "",
                    "status" => FALSE
                ));
            }
            $this->CI->task->updateTaskResult($param->id,$param->key,$result,2);
        }else{
            $result = json_encode(array(
                "full_path" => "",
                "save_name" => "",
                "file_size" => "",
                "status" => FALSE
            ));
            $this->CI->task->updateTaskResult($param->id,$param->key,$result,2);
        }

    }
}