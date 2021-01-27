<DOCTYPE html>
<?php
$conn = mysqli_connect("127.0.0.1", "root", "password", "stock_market");
$tb = mysqli_query($conn, "SELECT table_name FROM information_schema.tables WHERE table_schema = 'stock_market' ORDER BY table_name DESC;");
$table = mysqli_fetch_row($tb);
$result = mysqli_query($conn, "SELECT * FROM $table[0]");

$stocks = array();
while($row = mysqli_fetch_array($result, MYSQLI_NUM)){
    array_push($stocks, $row);
}
mysqli_close($conn);
?>

<html>
<head>
    <title>Stocks</title>
</head>
<body>
    <table border="1">
        <tr>
            <td>Symbol</td>
            <td>Name</td>
            <td>Price</td>
            <td>Change</td>
            <td>Percent Change</td>
            <td>Volume</td>
            <td>Average Volume</td>
            <td>Market Cap</td>
        </tr>
        <?php foreach($stocks as $stock): ?>
        <tr>
            <td><?php echo $stock[0]; ?></td>
            <td><?php echo $stock[1]; ?></td>
            <td><?php echo $stock[2]; ?></td>
            <td><?php echo $stock[3]; ?></td>
            <td><?php echo $stock[4]; ?></td>
            <td><?php echo $stock[5]; ?></td>
            <td><?php echo $stock[6]; ?></td>
            <td><?php echo $stock[7]; ?></td>
        </tr>
        <?php endforeach; ?>

    </table>
</body>
</html>