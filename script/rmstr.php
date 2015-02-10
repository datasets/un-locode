<?php
ini_set('memory_limit', '-1');
$i=$argv[1];
$ed="codeList.csv";
$row = 1;
    $fc = explode("\n",file_get_contents($i));
    $f=fopen($ed,'a');
    foreach($fc as $l)
    {
        $fields=str_getcsv($l);
        if(count($fields)<10) continue;
        if($fields[2]==="") continue;
        fputs($f,$l."\n");
    }
?>
