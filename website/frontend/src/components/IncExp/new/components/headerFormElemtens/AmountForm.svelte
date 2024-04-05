<script>
    import { IncExpNewTotalBillValue } from "../../../../store";

    let currentTotalBillValue = 0;
    IncExpNewTotalBillValue.subscribe((value )=> currentTotalBillValue = parseFloat(value).toFixed(2));
</script>

<strong>
    <span>{currentTotalBillValue} PLN</span> 
</strong>
