<?php


class Task_model extends CI_Model
{
    public function __construct()
    {
        parent::__construct();
    }
    public function getTaskListByKey($key)
    {
        //获取任务列表
        return $this->db->where(array(
            "key" => $key,
            "status" => 0
        ))->get('tasks')->result_array();
    }

    public function updateTaskStatusByKey($key,$oldStatus,$newStatus)
    {
        //更新任务状态
        $this->db->where(array(
            "key" => $key,
            "status" => $oldStatus,
        ));

        $this->db->update('tasks', array(
            "status" => $newStatus
        ));
    }

    public function getTaskInfoById($id)
    {
        return $this->db->where('id', $id)->get('tasks')->row_array();
    }

    public function updateTaskResult($id,$key,$result,$status)
    {
        $this->db->where(array(
            "id" => $id,
            "key" => $key
        ))->update('tasks', array(
            "result" => $this->security->xss_clean($result),
            "update_time" => time(),
            "status" => $status
        ));
    }

}