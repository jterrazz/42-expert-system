#!/usr/bin/php
<?PHP

$fileList = glob('/sgoinfre/goinfre/Perso/abbensid/Projets/expert_system/examples/good_files/*');

foreach($fileList as $filename){
    if(is_file($filename)){
        echo "****************************************************************\n";
        echo end(explode("/", $filename))."\n";
        $output = shell_exec("python expert_system.py '".$filename."'");
        echo $output;
    }
}

?>