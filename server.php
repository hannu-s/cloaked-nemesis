<?php

$id = $_POST['id'];
$vote = $_POST['vote'];

// validate id and vote
// id == int
// vote == "up" / "down" / "dis"
$output = array();
$command = "python3 updater.py " . $id . " " . $vote;
exec($command, $output);

echo ($output[0]);
