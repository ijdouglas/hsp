 <?php
$name = "results/test.csv";
$data = "this is another test called from within saveData()";
// write the file to disk
file_put_contents($name, $data);
?>