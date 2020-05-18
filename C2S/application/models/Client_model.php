<?php


class Client_model extends CI_Model
{
    public function __construct()
    {
        parent::__construct();
    }

    public function add($param)
    {
        $data = array(
            'public_ip' => $param['public_ip'],
            'private_ip' => $param['private_ip'],
            'os_version' => $param['os_version'],
            'current_user' => $param['current_user'],
            'uid' => $param['uid'],
            'av' => $param['av'],
            'share_users' => '',
            'note' => $param['note'],
            'sleep' => 1,
            'pid' => $param['pid'],
            'key' => $param['key'],
            'last_time' => time(),
            'join_time' => time()
        );
        return $this->db->insert('clients', $data);
    }
    public function getOneByKey($key)
    {
        return $this->db->where('key', $key)->get('clients')->row_array();
    }
    public function updateLastTimeByKey($key)
    {
        return $this->db->where('key', $key)->update('clients', array(
            "last_time" => time()
        ));
    }

}