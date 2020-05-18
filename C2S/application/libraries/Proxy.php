<?php
defined('BASEPATH') OR exit('No direct script access allowed');
require_once 'library/Requests.php';

class Proxy
{
    protected $CI;
    protected $params;

    public function __construct()
    {
        $this->CI =& get_instance();
    }
    public function getATunnel(){
        Requests::register_autoloader();
        $options = array(
            'auth' => array($this->CI->config->item('proxy_user'), $this->CI->config->item('proxy_pwd'))
        );
        $url = $this->CI->config->item('proxy_console_type').$this->CI->config->item('proxy_host').":".$this->CI->config->item('proxy_console_port').'/create_server';
        $request = Requests::get($url, array(), $options);
        if($request->status_code != 200){
            return false;
        }else{
            return $request->body;
        }
    }
}