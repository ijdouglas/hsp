<?php
ini_set(‘display_errors’, 1);

ini_set(‘display_startup_errors’, 1);

error_reporting(E_ALL);
$post_data = json_decode(file_get_contents('php://input'), true); 
// the directory "data" must be writable by the server
$name = "results/".$post_data['filename'].".csv"; 
$data = $post_data['filedata'];
// write the file to disk
file_put_contents($name, $data);
?>