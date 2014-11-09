<?php
ini_set('memory_limit', '-1');
$i="codeList_old.tsv";
$ed="codeList.tsv";
$row = 1;
    $fc = explode("\n",file_get_contents($i));
    $f=fopen($ed,'a');
    foreach($fc as $l)
    {
        $fields=explode("\t",$l);
        if(count($fields)<10) continue;
        if($fields[2]==="") continue;
        fputs($f,$l."\n");
    }
?>
