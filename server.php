<?php

$id = $_POST['id'];
$vote = $_POST['vote'];
$idMatch = "/^[0-9]*$/";

if (preg_match($idMatch, $id) && ($vote == "up" || $vote == "down" || $vote == "dis")) {
	$output = array();
	$command = "python3 updater.py " . $id . " " . $vote;
	exec($command, $output);
	var_dump ($output);
} else {
	echo ("Regex error.");
}




