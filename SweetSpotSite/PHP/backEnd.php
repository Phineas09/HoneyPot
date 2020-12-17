<?php
    require_once("idiorm.php");
    
	ORM::configure('mysql:host=localhost;dbname=honeyData');
	ORM::configure('username', 'honeyMonitor');
	ORM::configure('password', 'Claudiu147!$&');

    $db = ORM::get_db();

    header("Content-Type: application/json");


    // Handle POST submission

    if(isset($_POST['getAllContents'])) {

        try {
            //ORM::for_table('privileges')->where(array('user' => $this->user->id))->find_one();

            $tableContents = getAllPacketsAsTable();

            echo json_encode(
                array(
                    'statusCode' => 200,
                    'returnValue' => $tableContents
                ));
        } 
        catch (Exception $e) {
            echo json_encode(
                array(
                    'statusCode' => 420
                ));
        }
        exit;

    }

    

    if(isset($_POST['getNumberOfAttacksToday'])) {

        try {
            echo json_encode(
                array(
                    'statusCode' => 200,
                    'returnValue' => getNumberOfAttacksToday()
                ));
        } 
        catch (Exception $e) {
            echo json_encode(
                array(
                    'statusCode' => 420
                ));
        }
        exit;

    }

    function _getTableElement($packet) {

        $contents = 
            '<tr>
                <td>' . (string)$packet->Date        .  '</td>
                <td>' . (string)$packet->Source_Ip   .  '</td>
                <td>' . (string)$packet->Dest_Ip     .  '</td>
                <td>' . (string)$packet->Source_MAC  .  '</td>
                <td>' . (string)$packet->Method      .  '</td>
                <td>' . (string)$packet->Port        .  '</td>
                <td>' . (string)$packet->Path        .  '</td>
                <td>' . (string)$packet->Origin      .  '</td>
            </tr>';
        return $contents;
    }

    function getAllPacketsAsTable() {

        $packets = ORM::for_table("packets")
                ->order_by_desc("Date")
                ->find_many();
        if (empty($packets)) 
            return "";
            //contents

        $response = "";
        foreach($packets as $packet) {
            $response = $response . _getTableElement($packet);
        }

        return $response;
    }


    function getNumberOfAttacksToday() {

        $todayDate = date("Y-m-d");
        $numberOfAttacks = ORM::for_table('packets')
                ->where_raw('(Date(Date) = ?)', $todayDate)
                ->count();
        
        return $numberOfAttacks . " Packets Today" ;
    }


